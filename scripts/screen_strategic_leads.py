#!/usr/bin/env python3
"""Screen research cells before any candidate-generation or interview step."""
import json
from pathlib import Path

try:
    from scripts.build_research_graph import read_jsonl
except ModuleNotFoundError:  # direct script invocation
    from build_research_graph import read_jsonl

ROOT = Path(__file__).resolve().parents[1]
CELLS = ROOT / "corpus" / "research-cells.jsonl"
OUT = ROOT / "verification" / "strategic-lead-screen-v1.jsonl"


def screen(cell):
    reasons = []
    if cell["provenance"]["acquisition_status"] != "checksum-verified":
        reasons.append("official source files are not checksum-verified")
    if cell["measurement"]["data_granularity"] != "row-level":
        reasons.append("public evidence is not row-level")
    if cell["decision"]["role"] != "gated":
        reasons.append("cell is not an unresolved gated lead")
    if "specialist" in " ".join(cell["decision"]["limitations"]).lower():
        reasons.append("self-contained interpretation is not established")
    return {"cell_id": cell["cell_id"], "eligible_for_candidate_generation": not reasons, "reasons": reasons or ["eligible only for adversarial source and novelty review"]}


def main():
    rows = [screen(cell) for cell in read_jsonl(CELLS)]
    OUT.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    print(json.dumps({"screened": len(rows), "eligible": sum(row["eligible_for_candidate_generation"] for row in rows)}))


if __name__ == "__main__":
    main()
