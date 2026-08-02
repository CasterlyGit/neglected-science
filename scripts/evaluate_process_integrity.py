#!/usr/bin/env python3
"""Evaluate whether the local loop is moving toward a verified method verdict."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
try:
    from scripts.system_guards import check_transaction
except ModuleNotFoundError:
    from system_guards import check_transaction


def read(path):
    return json.loads((ROOT / path).read_text())


def read_jsonl(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def latest_batch():
    second = ROOT / "verification/system-one-batch-2.json"
    return read("verification/system-one-batch-2.json") if second.exists() else read("verification/system-one-batch-1.json")


def evaluate(now=None):
    improvement = read("verification/improvement-cycle-1.json")
    cycle = read("verification/cycle-result.json")
    screen = read_jsonl("verification/strategic-lead-screen-v1.jsonl")
    intake = read_jsonl("verification/source-intake-screen.jsonl")
    atlas = read("verification/structural-atlas-verdict.json")
    batch = latest_batch()
    active_cycle = read("verification/system-one-cycle.json")
    seed_screen = read("verification/system-one-seed-pre-admission-2.json")
    seed_audit = read("verification/system-one-seed-full-audit-1.json")
    seed_packet = read("verification/system-one-seed-candidate-packet-1.json")
    seed_packet_two = read("verification/system-one-seed-candidate-packet-2.json")
    seed_packet_three = read("verification/system-one-seed-candidate-packet-3.json")
    current_ready = sum(row["eligible_for_candidate_generation"] for row in screen)
    execution = improvement["integrity_gates"]["execution_integrity"]
    transaction_valid = check_transaction()["transaction"] == "pass"
    evidence = {
        "real_investigation_retained": transaction_valid,
        "investigation_transaction_valid": transaction_valid,
        "negative_evidence_retained": any(not row["eligible_for_candidate_generation"] for row in screen),
        "construction_gate_enforced": cycle["milestone_6_complete"],
        "primary_and_reserve_required": bool(cycle["primary_id"] and cycle["reserve_id"]),
        "execution_integrity": execution,
        "current_ready_targets": current_ready,
    }
    ready = current_ready >= 3 and execution == "pass"
    verdict = "ready-for-selection" if ready else "continue-bounded-cycle"
    return {
        "verdict_id": "process-integrity-cycle-2",
        "evaluated_at": now or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "reward_target": "verified-final-method-verdict",
        "verdict": verdict,
        "evidence": evidence,
        "systems": {
            "system_one": {
                "source_feasible_records": 0,
                "candidate_generation_permitted": False,
                "verdict": "no-justified-trio",
            },
            "system_two": {
                "structural_verdict": atlas["verdict"],
                "investigation_verdict_ready": False,
            },
        },
        "anti_gaming": [
            "Do not reward candidate count, candidate survival, or positive findings.",
            "Do not convert metadata, a score, or an analogy into a research target.",
            "Do not select without exactly three ready targets and a primary plus reserve.",
            "Do not treat a missing acquisition, checksum, or specialist gap as a pass.",
            "Retain rejected, blocked, null, and uncertain results as evidence.",
        ],
        "next_permitted_action": "Retain the execution-readiness failures; construct an explicitly versioned reconstruction and a separately certified reserve before reopening selection, with no final-outcome execution or System-2 promotion.",
    }


def main():
    result = evaluate()
    out = ROOT / "verification" / "process-integrity-verdict.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"verdict": result["verdict"], "ready_targets": result["evidence"]["current_ready_targets"]}))


if __name__ == "__main__":
    main()
