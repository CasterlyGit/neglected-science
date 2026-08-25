from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .audit import audit_bundle
from .io import bundle_root, load_document, safe_path, sha256_file


@dataclass
class ReplayResult:
    status: str
    executed: bool
    command: list[str]
    exit_code: int | None
    stdout: str
    stderr: str
    artifact_results: list[dict[str, Any]]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ReplayError(RuntimeError):
    pass


def _command(document: dict[str, Any]) -> list[str]:
    command = document.get("run", {}).get("replay", {}).get("command")
    if not isinstance(command, list) or not command or not all(isinstance(item, str) and item.strip() for item in command):
        raise ReplayError("replay.command must be a non-empty argument array")
    return command


def replay_bundle(path: str | Path, execute: bool = False) -> ReplayResult:
    root = bundle_root(path)
    document = load_document(root)
    report = audit_bundle(root)
    command = _command(document)
    run = document.get("run", {})
    replay = run.get("replay", {})
    expected_ids = replay.get("expected_artifacts", [])
    artifacts = {item.get("id"): item for item in run.get("artifacts", []) if isinstance(item, dict) and item.get("id")}
    if not expected_ids:
        raise ReplayError("replay.expected_artifacts must declare at least one artifact")
    for artifact_id in expected_ids:
        if artifact_id not in artifacts:
            raise ReplayError(f"Replay artifact does not resolve: {artifact_id}")

    warnings = []
    if replay.get("network") == "disabled":
        warnings.append("Manifest requests network-disabled replay; FEVKit cannot enforce network isolation without an external sandbox.")
    if report.computed_stage not in {"V2", "V3", "V4"}:
        warnings.append(f"Bundle currently audits at {report.computed_stage}; replay prerequisites may be incomplete.")

    if not execute:
        return ReplayResult("PREFLIGHT", False, command, None, "", "", [], warnings)

    timeout = replay.get("timeout_seconds", 120)
    if not isinstance(timeout, int) or timeout < 1 or timeout > 3600:
        raise ReplayError("timeout_seconds must be an integer from 1 to 3600")

    with tempfile.TemporaryDirectory(prefix="fevkit-replay-") as temporary:
        work = Path(temporary) / "bundle"
        shutil.copytree(root, work)
        for artifact_id in expected_ids:
            target = safe_path(work, artifacts[artifact_id]["path"])
            if target.exists():
                target.unlink()

        environment = {
            "PATH": os.environ.get("PATH", ""),
            "HOME": str(Path(temporary) / "home"),
            "TMPDIR": str(Path(temporary) / "tmp"),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PYTHONHASHSEED": "0",
            "FEVKIT_NETWORK": str(replay.get("network", "unknown")),
        }
        Path(environment["HOME"]).mkdir(parents=True, exist_ok=True)
        Path(environment["TMPDIR"]).mkdir(parents=True, exist_ok=True)
        try:
            completed = subprocess.run(command, cwd=work, env=environment, shell=False, text=True, capture_output=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired as exc:
            raise ReplayError(f"Replay exceeded {timeout} seconds") from exc
        except OSError as exc:
            raise ReplayError(f"Replay command could not start: {exc}") from exc

        results = []
        all_match = completed.returncode == 0
        for artifact_id in expected_ids:
            declaration = artifacts[artifact_id]
            target = safe_path(work, declaration["path"])
            actual = sha256_file(target) if target.is_file() else None
            expected = declaration.get("sha256")
            match = actual == expected
            results.append({"artifact_id": artifact_id, "path": declaration["path"], "expected_sha256": expected, "actual_sha256": actual, "match": match})
            all_match = all_match and match

        return ReplayResult("PASS" if all_match else "FAIL", True, command, completed.returncode, completed.stdout, completed.stderr, results, warnings)
