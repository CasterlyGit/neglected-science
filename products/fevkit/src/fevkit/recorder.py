from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class RunRecorder:
    """Agent-neutral SDK for emitting a FEVKit declaration."""

    def __init__(self, bundle: str | Path, *, run_id: str, title: str, objective: str, domain: str, system_name: str, system_version: str, profile: str = "generic", contains_personal_data: bool = False) -> None:
        self.bundle = Path(bundle).resolve(); self.bundle.mkdir(parents=True, exist_ok=True)
        self.document: dict[str, Any] = {"spec_version": "0.1", "run": {"id": run_id, "title": title, "objective": objective, "domain": domain, "started_at": _now(), "completed_at": _now(), "status": "running", "system": {"name": system_name, "version": system_version}, "inputs": [], "artifacts": [], "steps": [], "evidence": [], "claims": [], "human_checkpoints": [], "environment": {"runtimes": {}}, "replay": {"command": [], "expected_artifacts": []}, "validation": {"profile": profile, "claimed_stage": "V0", "evaluations": [], "prospective": False}, "privacy": {"contains_personal_data": contains_personal_data, "classification": "unspecified"}}}

    @property
    def run(self) -> dict[str, Any]: return self.document["run"]

    def _record_file(self, collection: str, *, identifier: str, path: str, **metadata: Any) -> dict[str, Any]:
        target = (self.bundle / path).resolve(); target.relative_to(self.bundle)
        if not target.is_file(): raise FileNotFoundError(target)
        record = {"id": identifier, "path": path, "sha256": _sha256(target), **metadata}; self.run[collection].append(record); return record

    def add_input(self, identifier: str, path: str, *, input_type: str = "dataset", sensitive: bool = False, **metadata: Any) -> dict[str, Any]: return self._record_file("inputs", identifier=identifier, path=path, type=input_type, sensitive=sensitive, **metadata)
    def add_artifact(self, identifier: str, path: str, *, generated_by: str | None = None, **metadata: Any) -> dict[str, Any]:
        if generated_by is not None: metadata["generated_by"] = generated_by
        return self._record_file("artifacts", identifier=identifier, path=path, **metadata)
    def add_step(self, *, identifier: str, function: str, action: str, inputs: list[str], outputs: list[str], tool: dict[str, Any] | None = None, status: str = "completed") -> dict[str, Any]:
        record = {"id": identifier, "sequence": len(self.run["steps"]) + 1, "function": function, "action": action, "inputs": inputs, "outputs": outputs, "status": status, "started_at": _now(), "completed_at": _now()}
        if tool is not None: record["tool"] = tool
        self.run["steps"].append(record); return record
    def add_evidence(self, *, identifier: str, klass: str, source: dict[str, Any], artifact_ids: list[str] | None = None) -> dict[str, Any]:
        record = {"id": identifier, "class": klass, "retrieved_at": _now(), "source": source, "artifact_ids": artifact_ids or []}; self.run["evidence"].append(record); return record
    def add_claim(self, *, identifier: str, text: str, kind: str, risk: str, support: list[dict[str, str]], uncertainty: str, limitations: str, step_ids: list[str] | None = None, rationale: str | None = None) -> dict[str, Any]:
        record = {"id": identifier, "text": text, "kind": kind, "risk": risk, "support": support, "uncertainty": uncertainty, "limitations": limitations, "step_ids": step_ids or []}
        if rationale: record["rationale"] = rationale
        self.run["claims"].append(record); return record
    def add_checkpoint(self, *, identifier: str, role: str, decision: str, status: str = "approved") -> dict[str, Any]:
        record = {"id": identifier, "role": role, "decision": decision, "status": status, "recorded_at": _now()}; self.run["human_checkpoints"].append(record); return record
    def set_environment(self, *, runtimes: dict[str, str], lockfiles: list[dict[str, Any]] | None = None, container: dict[str, Any] | None = None) -> None:
        value: dict[str, Any] = {"runtimes": runtimes}
        if lockfiles is not None: value["lockfiles"] = lockfiles
        if container is not None: value["container"] = container
        self.run["environment"] = value
    def set_replay(self, command: list[str], expected_artifacts: list[str], *, timeout_seconds: int = 300, network: str = "unspecified") -> None: self.run["replay"] = {"command": command, "expected_artifacts": expected_artifacts, "timeout_seconds": timeout_seconds, "network": network}
    def add_evaluation(self, evaluation: dict[str, Any]) -> None: self.run["validation"]["evaluations"].append(evaluation)
    def finish(self, *, claimed_stage: str, status: str = "completed") -> Path:
        self.run["status"] = status; self.run["completed_at"] = _now(); self.run["validation"]["claimed_stage"] = claimed_stage; return self.write()
    def write(self) -> Path:
        target = self.bundle / "run.json"; target.write_text(json.dumps(self.document, indent=2, sort_keys=True) + "\n", encoding="utf-8"); return target
