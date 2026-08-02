#!/usr/bin/env python3
"""Create a bounded, plain-language verdict from structural case records."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "corpus" / "structural-cases.jsonl"
VERDICT = ROOT / "verification" / "structural-atlas-verdict.json"
REPORT = ROOT / "reports" / "structural-atlas.md"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def build(cases=None):
    cases = read_jsonl(CASES) if cases is None else cases
    patterns = Counter(pattern for case in cases for pattern in case["structural_patterns"])
    counts = Counter(case["candidate_status"] for case in cases)
    result = {
        "verdict": "LIMITED SUPPORT — NO NEW TARGET TRIO",
        "plain_language": "Different fields in this seed set share recurring research-design failures: reused measurements, mismatched units, shifting calibration, evidence-table reconciliation, and missing usable data. This does not show that the fields share a scientific mechanism, and it does not yet produce three new interview-ready targets.",
        "case_count": len(cases),
        "domain_count": len({case["domain"] for case in cases}),
        "patterns": dict(sorted(patterns.items())),
        "candidate_status_counts": dict(sorted(counts.items())),
        "next_required_action": "Add only new checksum-acquirable paper–data cases that can fill a documented structural gap; then rerun the closed-evidence factory. Do not promote a case merely because it resembles another domain.",
        "claim_boundary": "The atlas describes evidence-supported similarities in research design, not a universal theory or a shared mechanism across domains."
    }
    return result


def render(cases, result):
    lines = ["# Structural Atlas", "", "## Final verdict", "", f"**{result['verdict']}**", "", result["plain_language"], "", "## Case map", "", "| Domain | Structural pattern | Plain-language finding | Status |", "| --- | --- | --- | --- |"]
    for case in cases:
        lines.append(f"| {case['domain']} | {', '.join(case['structural_patterns'])} | {case['plain_language_verdict']} | {case['candidate_status']} |")
    lines += ["", "## What this does and does not mean", "", f"- {result['claim_boundary']}", f"- Next gate: {result['next_required_action']}", "", "## Evidence locations", ""]
    for case in cases:
        lines.append(f"- `{case['case_id']}`: " + "; ".join(f"{item['url']} ({item['location']})" for item in case['source_evidence']) + f"; data: {case['data_evidence']['url']} ({case['data_evidence']['location']}).")
    return "\n".join(lines) + "\n"


def main():
    cases = read_jsonl(CASES)
    result = build(cases)
    VERDICT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    REPORT.write_text(render(cases, result))
    print(json.dumps({"cases": result["case_count"], "verdict": result["verdict"]}))


if __name__ == "__main__":
    main()
