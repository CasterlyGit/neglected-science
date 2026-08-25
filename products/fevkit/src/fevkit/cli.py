from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .core import FEVKitError, STAGES, audit_bundle, export_ro_crate, replay_bundle, sarif_document


def _write(value: Any, output: str | None) -> None:
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if output: Path(output).write_text(rendered, encoding="utf-8")
    else: sys.stdout.write(rendered)


def _text(result: Any) -> str:
    data=result.as_dict(); counts=data["counts"]; integrity=data["integrity"]
    lines=[f"FEVKit {data['status']}", f"Run: {data['run_id'] or 'unknown'}", f"Profile: {data['profile']}", f"Validation: {data['computed_stage']} ({STAGES[data['computed_stage']]})", f"Qualifiers: {''.join(data['qualifiers']) or 'none'}", f"Integrity: {integrity['verified_files']}/{integrity['declared_files']} declared files verified", f"Findings: {counts['errors']} error(s), {counts['warnings']} warning(s), {counts['info']} info"]
    for finding in data["findings"]:
        lines.append(f"[{finding['severity'].upper()}] {finding['code']} {finding['path']}: {finding['message']}")
        if finding.get("remediation"): lines.append(f"  fix: {finding['remediation']}")
    return "\n".join(lines)+"\n"


def build_parser() -> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(prog="fevkit",description="Audit the trajectory behind scientific-agent results."); parser.add_argument("--version",action="version",version=f"FEVKit {__version__}"); sub=parser.add_subparsers(dest="command",required=True)
    audit=sub.add_parser("audit"); audit.add_argument("bundle"); audit.add_argument("--profile"); audit.add_argument("--format",choices=("text","json","sarif"),default="text"); audit.add_argument("--output"); audit.add_argument("--strict",action="store_true")
    replay=sub.add_parser("replay"); replay.add_argument("bundle"); replay.add_argument("--execute",action="store_true"); replay.add_argument("--timeout",type=int); replay.add_argument("--allow-executable",action="append",default=[]); replay.add_argument("--output")
    crate=sub.add_parser("export-rocrate"); crate.add_argument("bundle"); crate.add_argument("--output",default="ro-crate-metadata.json")
    init=sub.add_parser("init"); init.add_argument("directory"); init.add_argument("--force",action="store_true")
    return parser


def main(argv: list[str] | None=None) -> int:
    args=build_parser().parse_args(argv)
    try:
        if args.command=="audit":
            result=audit_bundle(args.bundle,profile=args.profile)
            if args.format=="text":
                rendered=_text(result); Path(args.output).write_text(rendered,encoding="utf-8") if args.output else sys.stdout.write(rendered)
            elif args.format=="json": _write(result.as_dict(),args.output)
            else: _write(sarif_document(result),args.output)
            return 2 if result.status=="FAIL" or (args.strict and result.status=="WARN") else 0
        if args.command=="replay":
            result=replay_bundle(args.bundle,execute=args.execute,timeout=args.timeout,allowed_executables=None if not args.allow_executable else args.allow_executable); _write(result,args.output); return 0 if result.get("matched") is not False else 3
        if args.command=="export-rocrate": _write(export_ro_crate(args.bundle),args.output); return 0
        if args.command=="init":
            root=Path(args.directory); root.mkdir(parents=True,exist_ok=True); target=root/"run.json"
            if target.exists() and not args.force: raise FEVKitError(f"{target} exists; use --force")
            target.write_text(json.dumps({"spec_version":"0.1","run":{"id":"replace-me","title":"Replace me","objective":"Bound the question.","domain":"research/replace-me","started_at":"2026-01-01T00:00:00Z","completed_at":"2026-01-01T00:00:00Z","status":"completed","system":{"name":"replace-me","version":"replace-me"},"inputs":[],"artifacts":[],"steps":[],"evidence":[],"claims":[],"human_checkpoints":[],"environment":{"runtimes":{},"lockfiles":[]},"replay":{"command":[],"expected_artifacts":[]},"validation":{"profile":"generic","claimed_stage":"V0","evaluations":[],"prospective":False},"privacy":{"contains_personal_data":False}}},indent=2)+"\n"); print(target); return 0
    except (FEVKitError,OSError,json.JSONDecodeError,subprocess.SubprocessError) as error:
        print(f"fevkit: {error}",file=sys.stderr); return 2
    return 2
