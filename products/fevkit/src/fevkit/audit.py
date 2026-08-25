from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime
from importlib.resources import files
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .constants import EVIDENCE, FUNCTIONS, QUALIFIERS, SECRET_PATTERNS, STAGE_ORDER, STAGES, SUPPORT_RELATIONS, TEXT_EXTENSIONS
from .io import BundleError, bundle_root, load_document, safe_path, sha256_file


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    path: str = "$"
    remediation: str | None = None
    dimension: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass
class DimensionState:
    id: str
    name: str
    present: bool = False
    complete: bool = False
    count: int = 0
    finding_codes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AuditReport:
    status: str
    run_id: str | None
    profile: str
    claimed_stage: str | None
    computed_stage: str
    computed_stage_name: str
    qualifiers: list[str]
    findings: list[Finding]
    functions: dict[str, DimensionState]
    evidence: dict[str, DimensionState]
    integrity: dict[str, Any]
    metrics: dict[str, Any]
    metadata: dict[str, Any]

    @property
    def counts(self) -> dict[str, int]:
        counter = Counter(item.severity for item in self.findings)
        return {key: counter.get(key, 0) for key in ("error", "warning", "info")}

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "run_id": self.run_id,
            "profile": self.profile,
            "claimed_stage": self.claimed_stage,
            "computed_stage": self.computed_stage,
            "computed_stage_name": self.computed_stage_name,
            "qualifiers": self.qualifiers,
            "counts": self.counts,
            "findings": [item.to_dict() for item in self.findings],
            "functions": {key: value.to_dict() for key, value in self.functions.items()},
            "evidence": {key: value.to_dict() for key, value in self.evidence.items()},
            "integrity": self.integrity,
            "metrics": self.metrics,
            "metadata": self.metadata,
        }

    def to_text(self) -> str:
        lines = [
            f"FEVKit {self.status}",
            f"Run: {self.run_id or 'unknown'}",
            f"Profile: {self.profile}",
            f"Validation: {self.computed_stage} ({self.computed_stage_name})",
            f"Qualifiers: {''.join(self.qualifiers) or 'none'}",
            f"Integrity: {self.integrity['verified_files']}/{self.integrity['declared_files']} declared files verified",
            f"Claim support: {self.metrics['claims_with_support']}/{self.metrics['claims_total']} claims",
            f"Findings: {self.counts['error']} error(s), {self.counts['warning']} warning(s), {self.counts['info']} info",
        ]
        if self.metrics["next_stage_blockers"]:
            lines.append("Next-stage blockers:")
            lines.extend(f"  - {item}" for item in self.metrics["next_stage_blockers"])
        if self.findings:
            lines.append("Findings:")
            for item in self.findings:
                lines.append(f"  {item.severity.upper()} {item.code} [{item.path}]: {item.message}")
        return "\n".join(lines)

    def to_sarif(self) -> dict[str, Any]:
        rules: dict[str, dict[str, Any]] = {}
        results = []
        for item in self.findings:
            rules.setdefault(item.code, {"id": item.code, "shortDescription": {"text": item.message}})
            result = {"ruleId": item.code, "level": {"error": "error", "warning": "warning"}.get(item.severity, "note"), "message": {"text": item.message}, "properties": {"jsonPath": item.path}}
            if item.remediation:
                result["fixes"] = [{"description": {"text": item.remediation}}]
            results.append(result)
        return {"$schema": "https://json.schemastore.org/sarif-2.1.0.json", "version": "2.1.0", "runs": [{"tool": {"driver": {"name": "FEVKit", "semanticVersion": "0.1.0", "informationUri": "https://fevkit.vercel.app", "rules": list(rules.values())}}, "results": results}]}


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _time(value: Any) -> datetime | None:
    if not _text(value):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _add(findings: list[Finding], code: str, severity: str, message: str, path: str = "$", remediation: str | None = None, dimension: str | None = None) -> None:
    findings.append(Finding(code, severity, message, path, remediation, dimension))


def _load_profile(name: str) -> dict[str, Any]:
    resource = files("fevkit.data.profiles").joinpath(f"{name}.json")
    if not resource.is_file():
        resource = files("fevkit.data.profiles").joinpath("generic.json")
    return json.loads(resource.read_text(encoding="utf-8"))


def _schema_findings(document: dict[str, Any]) -> list[Finding]:
    schema = json.loads(files("fevkit.data.schemas").joinpath("run.schema.json").read_text(encoding="utf-8"))
    output = []
    for error in sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: list(item.path)):
        path = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.path)
        _add(output, "SCHEMA.INVALID", "error", error.message, path)
    return output


def _ids(items: list[Any], label: str, base: str, findings: list[Finding]) -> set[str]:
    seen: set[str] = set()
    for index, raw in enumerate(items):
        item_id = _dict(raw).get("id")
        if not _text(item_id):
            continue
        if item_id in seen:
            _add(findings, "STRUCTURE.DUPLICATE_ID", "error", f"Duplicate {label} id: {item_id}", f"{base}[{index}].id")
        seen.add(item_id)
    return seen


def audit_bundle(path: str | Path, profile: str | None = None) -> AuditReport:
    root = bundle_root(path)
    document = load_document(root)
    run = _dict(document.get("run"))
    findings = _schema_findings(document)
    profile_data = _load_profile(profile or _dict(run.get("validation")).get("profile") or "generic")
    profile_id = profile_data["id"]

    functions = {key: DimensionState(key, name) for key, name in FUNCTIONS.items()}
    evidence_states = {key: DimensionState(key, name) for key, name in EVIDENCE.items()}
    steps, inputs, artifacts = _list(run.get("steps")), _list(run.get("inputs")), _list(run.get("artifacts"))
    evidence, claims = _list(run.get("evidence")), _list(run.get("claims"))
    checkpoints = _list(run.get("human_checkpoints"))
    validation = _dict(run.get("validation"))
    evaluations = _list(validation.get("evaluations"))

    input_ids = _ids(inputs, "input", "$.run.inputs", findings)
    artifact_ids = _ids(artifacts, "artifact", "$.run.artifacts", findings)
    step_ids = _ids(steps, "step", "$.run.steps", findings)
    evidence_ids = _ids(evidence, "evidence", "$.run.evidence", findings)
    _ids(claims, "claim", "$.run.claims", findings)

    started, completed = _time(run.get("started_at")), _time(run.get("completed_at"))
    if started and completed and completed < started:
        _add(findings, "STRUCTURE.TIME_ORDER", "error", "completed_at precedes started_at.", "$.run.completed_at")

    for index, raw in enumerate(steps):
        step, base = _dict(raw), f"$.run.steps[{index}]"
        dimension = step.get("function")
        if dimension not in functions:
            _add(findings, "FUNCTION.UNKNOWN", "error", f"Unknown function dimension: {dimension!r}", f"{base}.function")
            continue
        state = functions[dimension]
        state.present, state.count, state.complete = True, state.count + 1, True
        if not _text(step.get("action")):
            _add(findings, "STEP.ACTION", "error", "Step action is required.", f"{base}.action", dimension=dimension); state.complete = False
        if step.get("status") != "completed":
            _add(findings, "STEP.STATUS", "warning", "Step is not marked completed.", f"{base}.status", dimension=dimension); state.complete = False
        if not _time(step.get("started_at")):
            _add(findings, "STEP.START_TIME", "warning", "Step start time is absent or invalid.", f"{base}.started_at", dimension=dimension)
        if not _time(step.get("completed_at")):
            _add(findings, "STEP.END_TIME", "warning", "Step completion time is absent or invalid.", f"{base}.completed_at", dimension=dimension)
        for ref_index, reference in enumerate(_list(step.get("inputs"))):
            if reference not in input_ids and reference not in artifact_ids:
                _add(findings, "REF.STEP_INPUT", "error", f"Step input reference does not resolve: {reference}", f"{base}.inputs[{ref_index}]", dimension=dimension); state.complete = False
        for ref_index, reference in enumerate(_list(step.get("outputs"))):
            if reference not in artifact_ids:
                _add(findings, "REF.STEP_OUTPUT", "error", f"Step output does not resolve: {reference}", f"{base}.outputs[{ref_index}]", dimension=dimension); state.complete = False
        if dimension == "F3":
            tool = _dict(step.get("tool"))
            if not _text(tool.get("name")):
                _add(findings, "TOOL.NAME", "error", "Tool name is required.", f"{base}.tool.name", dimension=dimension); state.complete = False
            if not _text(tool.get("version")):
                _add(findings, "TOOL.VERSION", "error", "Tool version must be pinned.", f"{base}.tool.version", dimension=dimension); state.complete = False
            if not isinstance(tool.get("parameters"), dict):
                _add(findings, "TOOL.PARAMETERS", "error", "Tool parameters must be an object.", f"{base}.tool.parameters", dimension=dimension); state.complete = False

    requirements = {
        "E1": (("doi", "pmid", "url", "citation"), "one-of"),
        "E2": (("database", "version", "query", "selection"), "all"),
        "E3": (("dataset_id", "version", "selection"), "all"),
        "E4": (("software", "version", "parameters"), "all"),
        "E5": (("model", "version", "parameters"), "all"),
        "E6": (("protocol", "observation_type", "site"), "all"),
    }
    for index, raw in enumerate(evidence):
        item, base = _dict(raw), f"$.run.evidence[{index}]"
        dimension = item.get("class")
        if dimension not in evidence_states:
            _add(findings, "EVIDENCE.UNKNOWN_CLASS", "error", f"Unknown evidence class: {dimension!r}", f"{base}.class"); continue
        state = evidence_states[dimension]
        state.present, state.count, state.complete = True, state.count + 1, True
        source = _dict(item.get("source"))
        if not _text(source.get("title")):
            _add(findings, "EVIDENCE.TITLE", "error", "Evidence title is required.", f"{base}.source.title", dimension=dimension); state.complete = False
        if not _time(item.get("retrieved_at")):
            _add(findings, "EVIDENCE.RETRIEVED_AT", "error", "Evidence requires an ISO-8601 retrieval timestamp.", f"{base}.retrieved_at", dimension=dimension); state.complete = False
        keys, mode = requirements[dimension]
        if mode == "one-of":
            if not any(_text(source.get(key)) for key in keys):
                _add(findings, f"{dimension}.CITATION", "error", "Literature evidence requires DOI, PMID, URL, or citation.", f"{base}.source", dimension=dimension); state.complete = False
        else:
            for key in keys:
                valid = isinstance(source.get(key), dict) if key == "parameters" else _text(source.get(key))
                if not valid:
                    _add(findings, f"{dimension}.{key.upper()}", "error", f"{EVIDENCE[dimension]} requires source.{key}.", f"{base}.source.{key}", dimension=dimension); state.complete = False
        for ref_index, reference in enumerate(_list(item.get("artifact_ids"))):
            if reference not in artifact_ids and reference not in input_ids:
                _add(findings, "REF.EVIDENCE_ARTIFACT", "error", f"Evidence artifact does not resolve: {reference}", f"{base}.artifact_ids[{ref_index}]", dimension=dimension); state.complete = False

    declared = checked = verified = missing = mismatched = unhashed = secret_hits = scanned = 0
    for collection_name, collection in (("inputs", inputs), ("artifacts", artifacts)):
        for index, raw in enumerate(collection):
            item, base = _dict(raw), f"$.run.{collection_name}[{index}]"
            declared += 1
            try:
                target = safe_path(root, item.get("path"))
            except BundleError as exc:
                _add(findings, "FILE.UNSAFE_PATH", "error", str(exc), f"{base}.path"); missing += 1; continue
            if not target.is_file():
                _add(findings, "ARTIFACT.MISSING_FILE", "error", f"Declared file does not exist: {item.get('path')}", f"{base}.path"); missing += 1; continue
            checked += 1
            digest = item.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                _add(findings, "FILE.SHA256", "error", "A lowercase SHA-256 digest is required.", f"{base}.sha256"); unhashed += 1
            elif sha256_file(target) != digest:
                code = f"{collection_name[:-1].upper()}.HASH_MISMATCH"
                _add(findings, code, "error", f"Hash mismatch for {item.get('path')}.", f"{base}.sha256", "Regenerate the file or update the manifest only after reviewing the change."); mismatched += 1
            else:
                verified += 1
            if target.suffix.lower() in TEXT_EXTENSIONS and target.stat().st_size <= 1_000_000:
                scanned += 1
                content = target.read_text(encoding="utf-8", errors="ignore")
                for label, token in SECRET_PATTERNS.items():
                    if token in content:
                        _add(findings, "PRIVACY.SECRET_PATTERN", "error", f"Possible {label} token found in {item.get('path')}.", f"{base}.path", "Remove and rotate the secret before sharing."); secret_hits += 1

    privacy = _dict(run.get("privacy"))
    personal_data = privacy.get("contains_personal_data")
    sensitive = [item for item in inputs if _dict(item).get("sensitive") is True]
    if not isinstance(personal_data, bool):
        _add(findings, "PRIVACY.ATTESTATION", "error", "Declare privacy.contains_personal_data as true or false.", "$.run.privacy.contains_personal_data")
    if sensitive and personal_data is not True:
        _add(findings, "PRIVACY.CONTRADICTION", "error", "Sensitive inputs require privacy.contains_personal_data=true and documented controls.", "$.run.inputs")
    if personal_data is True and not _text(privacy.get("controls")):
        _add(findings, "PRIVACY.CONTROLS", "error", "Personal-data runs require documented controls.", "$.run.privacy.controls")

    supported = qualified = high_risk = 0
    relations = Counter()
    for index, raw in enumerate(claims):
        claim, base = _dict(raw), f"$.run.claims[{index}]"
        valid_support = 0
        support = _list(claim.get("support"))
        if not support:
            _add(findings, "CLAIM.UNSUPPORTED", "error", "Claim has no evidence support edges.", f"{base}.support")
        for edge_index, raw_edge in enumerate(support):
            edge = _dict(raw_edge); evidence_id, relation = edge.get("evidence_id"), edge.get("relation")
            if evidence_id not in evidence_ids:
                _add(findings, "REF.CLAIM_EVIDENCE", "error", f"Claim evidence does not resolve: {evidence_id}", f"{base}.support[{edge_index}].evidence_id")
            if relation not in SUPPORT_RELATIONS:
                _add(findings, "CLAIM.RELATION", "error", f"Unknown support relation: {relation!r}", f"{base}.support[{edge_index}].relation")
            else:
                relations[relation] += 1
                if evidence_id in evidence_ids and relation != "contradicted_by": valid_support += 1
        if valid_support: supported += 1
        has_uncertainty, has_limits = _text(claim.get("uncertainty")), _text(claim.get("limitations"))
        if has_uncertainty and has_limits: qualified += 1
        if not has_uncertainty: _add(findings, "CLAIM.UNCERTAINTY", "error", "Claim requires an uncertainty statement.", f"{base}.uncertainty")
        if not has_limits: _add(findings, "CLAIM.LIMITATIONS", "error", "Claim requires a limitations statement.", f"{base}.limitations")
        if claim.get("kind") in {"inference", "causal_hypothesis", "speculation"} and not _text(claim.get("rationale")):
            _add(findings, "CLAIM.RATIONALE", "error", "Inferential claims require an inspectable rationale.", f"{base}.rationale")
        for ref_index, reference in enumerate(_list(claim.get("step_ids"))):
            if reference not in step_ids: _add(findings, "REF.CLAIM_STEP", "error", f"Claim step does not resolve: {reference}", f"{base}.step_ids[{ref_index}]")
        if claim.get("risk") in {"high", "clinical"}:
            high_risk += 1
            _add(findings, "CLAIM.CLINICAL_BOUNDARY", "warning", "High or clinical-risk claim detected. FEVKit audits provenance, not medical validity or safety.", base, "Require appropriate clinical governance outside FEVKit.")

    environment = _dict(run.get("environment")); runtimes = _dict(environment.get("runtimes")); lockfiles = _list(environment.get("lockfiles")); container = _dict(environment.get("container"))
    runtime_pinned = bool(runtimes) and all(_text(value) for value in runtimes.values())
    lock_pinned = bool(lockfiles) and all(_text(_dict(item).get("path")) and re.fullmatch(r"[0-9a-f]{64}", str(_dict(item).get("sha256", ""))) for item in lockfiles)
    container_pinned = _text(container.get("image")) and "@sha256:" in container.get("image", "")
    replay = _dict(run.get("replay")); command = replay.get("command"); expected = _list(replay.get("expected_artifacts"))
    replay_declared = isinstance(command, list) and bool(command) and all(_text(item) for item in command)
    replay_expected = bool(expected) and all(item in artifact_ids for item in expected)
    if command is not None and not replay_declared: _add(findings, "REPLAY.COMMAND", "error", "replay.command must be a non-empty argument array; shell strings are rejected.", "$.run.replay.command")
    if not runtime_pinned: _add(findings, "ENV.RUNTIME", "error", "Declare exact runtime versions.", "$.run.environment.runtimes")
    if not (lock_pinned or container_pinned): _add(findings, "ENV.NO_LOCK_OR_CONTAINER", "error", "Replayability requires a hashed lockfile or digest-pinned container.", "$.run.environment")

    flags = {
        "baseline": any(bool(_dict(item).get("baseline") or _dict(item).get("control")) for item in evaluations),
        "statistics": any(bool(_list(_dict(item).get("metrics"))) for item in evaluations),
        "uncertainty": any(bool(_dict(_dict(item).get("uncertainty")).get("method")) for item in evaluations),
        "robustness": any(bool(_dict(item).get("robustness") or _dict(item).get("failure_analysis")) for item in evaluations),
        "multiple_testing": any(_text(_dict(item).get("multiple_testing")) for item in evaluations),
        "external": any(_dict(item).get("independent") is True or _text(_dict(item).get("external_site")) for item in evaluations),
        "prospective": validation.get("prospective") is True or any(_dict(item).get("prospective") is True for item in evaluations),
        "closed_loop": validation.get("closed_loop") is True or any(_dict(item).get("closed_loop") is True for item in evaluations),
    }
    approved_human = any(_dict(item).get("status") == "approved" and _text(_dict(item).get("role")) and _text(_dict(item).get("decision")) for item in checkpoints)

    for dimension in profile_data.get("required_functions", []):
        if not functions[dimension].complete: _add(findings, "PROFILE.FUNCTION", "error", f"Profile '{profile_id}' requires {dimension}: {FUNCTIONS[dimension]}.", "$.run.steps", dimension=dimension)
    for dimension in profile_data.get("required_evidence", []):
        if not evidence_states[dimension].complete: _add(findings, "PROFILE.EVIDENCE", "error", f"Profile '{profile_id}' requires {dimension}: {EVIDENCE[dimension]}.", "$.run.evidence", dimension=dimension)
    profile_checks = {
        "requires_human_review": (approved_human, "PROFILE.HUMAN_REVIEW", "This profile requires an approved human checkpoint."),
        "requires_statistics": (flags["statistics"], "PROFILE.STATISTICS", "This profile requires statistical metrics."),
        "requires_uncertainty": (flags["uncertainty"], "PROFILE.UNCERTAINTY", "This profile requires uncertainty characterization."),
        "requires_robustness": (flags["robustness"], "PROFILE.ROBUSTNESS", "This profile requires robustness or failure analysis."),
        "requires_multiple_testing": (flags["multiple_testing"], "PROFILE.MULTIPLE_TESTING", "This profile requires a multiple-testing declaration."),
    }
    for flag, (satisfied, code, message) in profile_checks.items():
        if profile_data.get(flag) and not satisfied: _add(findings, code, "error", message, "$.run.validation")

    critical = tuple(("SCHEMA.", "STRUCTURE.", "REF.", "FUNCTION.", "STEP.", "TOOL.", "FILE.", "INPUT.", "ARTIFACT."))
    demonstrated = bool(steps) and bool(artifacts) and all(_dict(item).get("status") == "completed" for item in steps) and not any(item.severity == "error" and item.code.startswith(critical) for item in findings)
    stage = "V1" if demonstrated else "V0"
    all_verified = declared > 0 and verified == declared and missing == mismatched == unhashed == 0
    if stage == "V1" and all_verified and runtime_pinned and (lock_pinned or container_pinned) and replay_declared and replay_expected: stage = "V2"
    v3 = stage == "V2" and bool(evaluations) and flags["baseline"] and flags["statistics"] and flags["uncertainty"] and flags["robustness"] and supported == len(claims) and qualified == len(claims)
    if profile_data.get("requires_multiple_testing"): v3 = v3 and flags["multiple_testing"]
    if profile_data.get("requires_human_review"): v3 = v3 and approved_human
    if v3: stage = "V3"
    if stage == "V3" and flags["prospective"] and flags["external"] and evidence_states["E6"].complete: stage = "V4"

    minimum = profile_data.get("minimum_stage", "V0")
    if STAGE_ORDER[stage] < STAGE_ORDER[minimum]: _add(findings, "PROFILE.MINIMUM_STAGE", "error", f"Profile '{profile_id}' requires at least {minimum}; this bundle supports {stage}.", "$.run.validation")
    claimed = validation.get("claimed_stage")
    if claimed in STAGE_ORDER and STAGE_ORDER[claimed] > STAGE_ORDER[stage]: _add(findings, "VALIDATION.OVERCLAIM", "error", f"Run claims {claimed}, but captured evidence supports at most {stage}.", "$.run.validation.claimed_stage", "Resolve blockers or lower the claimed stage.")

    for state in list(functions.values()) + list(evidence_states.values()):
        state.finding_codes = sorted({item.code for item in findings if item.dimension == state.id})
        if any(item.severity == "error" and item.dimension == state.id for item in findings): state.complete = False

    qualifiers = []
    if flags["baseline"]: qualifiers.append("B")
    if approved_human: qualifiers.append("H")
    if flags["statistics"] and flags["uncertainty"]: qualifiers.append("S")
    if flags["robustness"]: qualifiers.append("R")
    if flags["external"]: qualifiers.append("X")
    if flags["prospective"]: qualifiers.append("P")
    if flags["closed_loop"]: qualifiers.append("C")

    blockers = {"V0": "capture an ordered completed trajectory with declared artifacts", "V1": "verify files and pin a replayable environment and command", "V2": "add baseline-aware evaluation, uncertainty, robustness, and supported claims", "V3": "complete prospective independent evaluation with E6 observations", "V4": "maintain monitoring and governance"}
    status = "FAIL" if any(item.severity == "error" for item in findings) else ("WARN" if any(item.severity == "warning" for item in findings) else "PASS")
    integrity = {"declared_files": declared, "checked_files": checked, "verified_files": verified, "missing_files": missing, "hash_mismatches": mismatched, "unhashed_files": unhashed, "all_declared_files_verified": all_verified}
    metrics = {
        "steps_total": len(steps), "artifacts_total": len(artifacts), "evidence_total": len(evidence), "claims_total": len(claims), "claims_with_support": supported, "claims_fully_qualified": qualified,
        "claim_support_coverage": supported / len(claims) if claims else 1.0, "claim_qualification_coverage": qualified / len(claims) if claims else 1.0,
        "function_coverage": sum(state.present for state in functions.values()) / len(functions), "evidence_class_coverage": sum(state.present for state in evidence_states.values()) / len(evidence_states),
        "high_or_clinical_risk_claims": high_risk, "support_relations": dict(relations),
        "environment": {"runtime_pinned": runtime_pinned, "lockfiles_pinned": lock_pinned, "container_pinned": container_pinned, "replay_declared": replay_declared, "replay_expected_artifacts": replay_expected},
        "evaluation": flags, "privacy": {"declared_personal_data": personal_data, "declared_sensitive_inputs": len(sensitive), "scanned_text_files": scanned, "secret_pattern_hits": secret_hits, "scan_limit_bytes": 1_000_000},
        "next_stage_blockers": [blockers[stage]],
    }
    metadata = {"manifest": str(root / "run.json"), "profile_title": profile_data.get("title", profile_id), "profile_description": profile_data.get("description", ""), "minimum_stage": minimum, "validation_stage_name": STAGES[stage], "qualifier_definitions": {key: QUALIFIERS[key] for key in qualifiers}}
    return AuditReport(status, run.get("id"), profile_id, claimed, stage, STAGES[stage], qualifiers, findings, functions, evidence_states, integrity, metrics, metadata)
