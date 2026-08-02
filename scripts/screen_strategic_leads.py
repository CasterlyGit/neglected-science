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
ATTEMPTS = ROOT / "verification" / "atlas-acquisition-attempts.jsonl"


def screen(cell, attempts_by_cell=None, upgrades_by_cell=None):
    reasons = []
    has_upgrade = upgrades_by_cell and upgrades_by_cell.get(cell["cell_id"], {}).get("result") == "checksum-verified"
    if cell["provenance"]["acquisition_status"] != "checksum-verified" and not has_upgrade:
        reasons.append("official source files are not checksum-verified")
    if attempts_by_cell and attempts_by_cell.get(cell["cell_id"], {}).get("result") == "access-blocked":
        reasons.append("fresh official-file retrieval is access-blocked")
    if cell["measurement"]["data_granularity"] != "row-level":
        reasons.append("public evidence is not row-level")
    if cell["decision"]["role"] != "gated":
        reasons.append("cell is not an unresolved gated lead")
    if "specialist" in " ".join(cell["decision"]["limitations"]).lower():
        reasons.append("self-contained interpretation is not established")
    if not cell.get("candidate_clearance"):
        reasons.append("adversarial novelty and consequence clearance is absent")
    return {"cell_id": cell["cell_id"], "eligible_for_candidate_generation": not reasons, "reasons": reasons or ["eligible only for adversarial source and novelty review"]}


def main():
    attempts_by_cell = {row["cell_id"]: row for row in read_jsonl(ATTEMPTS)}
    upgrades = ROOT / "verification" / "atlas-provenance-upgrades.jsonl"
    upgrades_by_cell = {row["cell_id"]: row for row in read_jsonl(upgrades)}
    rows = [screen(cell, attempts_by_cell, upgrades_by_cell) for cell in read_jsonl(CELLS)]
    OUT.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    print(json.dumps({"screened": len(rows), "eligible": sum(row["eligible_for_candidate_generation"] for row in rows)}))


if __name__ == "__main__":
    main()
