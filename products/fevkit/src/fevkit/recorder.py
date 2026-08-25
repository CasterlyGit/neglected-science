from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import atomic_write, canonical_json, sha256_file


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class RunRecorder:
    """Construct a FEVKit bundle without coupling to an agent framework."""

    def __init__(self, directory: str | Path, *, run_id: str, title: str, objective: str, domain: str = "scientific-research", system_name: str = "custom-workflow", system_version: str = "unversioned") -> None:
        self.root = Path(directory).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.document: dict[str, Any] = {
            "spec_version": "0.1",
            "run": {
                "id": run_id, "title": title, "objective": objective, "domain": domain,
                "started_at": _now(), "completed_at": _now(), "status": "running",
                "system": {"name": system_name, "version": system_version},
                "privacy": {"contains_personal_data": False, "classification": "public"},
                "environment": {"runtimes": {}, "lockfiles": []},
                "inputs": [], "artifacts": [], "steps": [], "evidence": [], "claims": [], "human_checkpoints": [],
                "validation": {"profile": "generic", "claimed_stage": "V0", "evaluations": [], "prospective": False, "closed_loop": False},
                "replay": {"command": [], "expected_artifacts": [], "timeout_seconds": 120, "network": "unknown"},
            },
        }
        self.flush()

    @property
    def run(self) -> dict[str, Any]:
        return self.document["run"]

    def add_file(self, *, item_id: str, path: str, collection: str, media_type: str = "application/octet-stream", **metadata: Any) -> dict[str, Any]:
        target = (self.root / path).resolve()
        target.relative_to(self.root)
        if not target.is_file():
            raise FileNotFoundError(target)
        item = {"id": item_id, "path": path, "sha256": sha256_file(target), "media_type": media_type, **metadata}
        self.run[collection].append(item)
        self.flush()
        return item

    def add_input(self, **kwargs: Any) -> dict[str, Any]:
        return self.add_file(collection="inputs", **kwargs)

    def add_artifact(self, **kwargs: Any) -> dict[str, Any]:
        return self.add_file(collection="artifacts", **kwargs)

    def record_step(self, **step: Any) -> dict[str, Any]:
        step.setdefault("sequence", len(self.run["steps"]) + 1)
        step.setdefault("status", "completed")
        step.setdefault("started_at", _now())
        step.setdefault("completed_at", _now())
        self.run["steps"].append(step)
        self.flush()
        return step

    def add_evidence(self, **evidence: Any) -> dict[str, Any]:
        evidence.setdefault("retrieved_at", _now())
        self.run["evidence"].append(evidence)
        self.flush()
        return evidence

    def add_claim(self, **claim: Any) -> dict[str, Any]:
        self.run["claims"].append(claim)
        self.flush()
        return claim

    def add_checkpoint(self, **checkpoint: Any) -> dict[str, Any]:
        checkpoint.setdefault("recorded_at", _now())
        self.run["human_checkpoints"].append(checkpoint)
        self.flush()
        return checkpoint

    def finish(self, *, status: str = "completed") -> Path:
        self.run["status"] = status
        self.run["completed_at"] = _now()
        self.flush()
        return self.root / "run.json"

    def flush(self) -> None:
        atomic_write(self.root / "run.json", canonical_json(self.document))
