from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .audit import audit_bundle
from .io import canonical_json
from .replay import ReplayError, replay_bundle
from .rocrate import export_rocrate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fevkit", description="Audit and replay scientific-agent trajectories.")
    parser.add_argument("--version", action="version", version=f"FEVKit {__version__}")
    subcommands = parser.add_subparsers(dest="command", required=True)

    audit = subcommands.add_parser("audit", help="Audit a FEVKit bundle.")
    audit.add_argument("bundle", type=Path)
    audit.add_argument("--profile")
    audit.add_argument("--format", choices=("text", "json", "sarif"), default="text")
    audit.add_argument("--output", type=Path)

    replay = subcommands.add_parser("replay", help="Preflight or execute declared replay.")
    replay.add_argument("bundle", type=Path)
    replay.add_argument("--execute", action="store_true")
    replay.add_argument("--output", type=Path)

    crate = subcommands.add_parser("export-rocrate", help="Export a Process Run RO-Crate.")
    crate.add_argument("bundle", type=Path)
    crate.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "audit":
            report = audit_bundle(args.bundle, profile=args.profile)
            if args.format == "text":
                content = report.to_text() + "\n"
            elif args.format == "json":
                content = canonical_json(report.to_dict())
            else:
                content = canonical_json(report.to_sarif())
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(content, encoding="utf-8")
            else:
                sys.stdout.write(content)
            return 2 if report.status == "FAIL" else 0

        if args.command == "replay":
            result = replay_bundle(args.bundle, execute=args.execute)
            content = canonical_json(result.to_dict())
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(content, encoding="utf-8")
            else:
                sys.stdout.write(content)
            return 0 if result.status in {"PASS", "PREFLIGHT"} else 3

        if args.command == "export-rocrate":
            print(export_rocrate(args.bundle, args.output))
            return 0
    except (ValueError, OSError, ReplayError) as exc:
        print(f"FEVKit error: {exc}", file=sys.stderr)
        return 4
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
