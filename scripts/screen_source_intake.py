#!/usr/bin/env python3
"""Keep source-feasible records separate from evidence-grounded research cells."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "corpus" / "source-feasibility-intake.jsonl"
OUT = ROOT / "verification" / "source-intake-screen.jsonl"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def screen(row):
    return {"intake_id": row["intake_id"], "eligible_for_cell_construction": row["retrieval"]["result"] == "checksum-verified" and all(file["checksum_match"] for file in row["files"]), "prohibited_next_step": "candidate generation", "required_next_step": "attach primary-paper claim and complete structural-fragility audit"}


def main():
    rows = [screen(row) for row in read_jsonl(INTAKE)]
    OUT.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    print(json.dumps({"intake": len(rows), "cell_construction_eligible": sum(row["eligible_for_cell_construction"] for row in rows)}))


if __name__ == "__main__":
    main()
