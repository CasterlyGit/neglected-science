#!/usr/bin/env python3
"""Non-promoting System-2 shadow review for a fixed System-1 proof program."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / name).read_text())


def review():
    batches = [read("verification/system-one-batch-1.json"), read("verification/system-one-batch-2.json")]
    if any(batch["verdict"] != "no-justified-trio" or len(batch["audits"]) != 3 for batch in batches):
        raise ValueError("fixed proof batches are incomplete")
    return {
        "review_id": "system-two-shadow-proof-1",
        "batches": [batch["batch_id"] for batch in batches],
        "system_two_ready_records": 0,
        "candidate_packets": 0,
        "verdict": "LIMITED SUPPORT — NO TARGET TRIO",
        "plain_language": "Across two fixed, diverse System-1 batches, every record had a traceable failed gate before structural promotion. There is no mapped record with a distinct domain consequence for System 2 to compare, so no target trio exists.",
        "next_permitted_action": "Stop further intake under this proof program and redesign System-1 selection around pre-specified artifact and consequence signals before any new batch.",
    }


def main():
    result = review()
    (ROOT / "verification/system-two-shadow-review.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"verdict": result["verdict"], "ready": result["system_two_ready_records"]}))


if __name__ == "__main__":
    main()
