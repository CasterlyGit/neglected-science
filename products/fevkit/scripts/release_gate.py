from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = os.environ.copy()
ENV["PYTHONPATH"] = str(ROOT / "src")
(ROOT / "build").mkdir(exist_ok=True)


def run(name: str, command: list[str], expected: set[int] = {0}) -> dict[str, object]:
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=ROOT, env=ENV, capture_output=True, text=True, check=False)
    return {
        "name": name,
        "command": command,
        "returncode": completed.returncode,
        "expected_returncodes": sorted(expected),
        "passed": completed.returncode in expected,
        "duration_seconds": round(time.perf_counter() - started, 3),
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
    }


checks = [
    run("compile", [sys.executable, "-m", "compileall", "-q", "src", "tests", "scripts"]),
    run("unit-tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
    run("complete-audit", [sys.executable, "-m", "fevkit", "audit", "examples/complete", "--strict"]),
    run("broken-rejection", [sys.executable, "-m", "fevkit", "audit", "examples/incomplete"], {2}),
    run("sarif", [sys.executable, "-m", "fevkit", "audit", "examples/incomplete", "--format", "sarif", "--output", "build/fevkit.sarif"], {2}),
    run("replay-preflight", [sys.executable, "-m", "fevkit", "replay", "examples/complete", "--output", "build/replay-preflight.json"]),
    run("replay-execution", [sys.executable, "-m", "fevkit", "replay", "examples/complete", "--execute", "--output", "build/replay.json"]),
    run("ro-crate", [sys.executable, "-m", "fevkit", "export-rocrate", "examples/complete", "--output", "build/ro-crate-metadata.json"]),
]
web = ROOT / "web" / "index.html"
summary = {
    "release": "FEVKit 0.1.0",
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "all_required_passed": all(check["passed"] for check in checks),
    "checks": checks,
    "source_file_count": sum(path.is_file() for path in ROOT.rglob("*") if ".git" not in path.parts and "__pycache__" not in path.parts),
    "web_index_sha256": hashlib.sha256(web.read_bytes()).hexdigest() if web.is_file() else None,
    "scientific_boundary": "Passing FEVKit establishes declared trajectory integrity and captured assurance evidence; it does not establish biological truth, clinical utility, safety, or regulatory compliance."
}
(ROOT / "VERIFICATION.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"all_required_passed": summary["all_required_passed"], "checks": len(checks)}, indent=2))
raise SystemExit(0 if summary["all_required_passed"] else 1)
