#!/usr/bin/env python3
"""Build a conservative graph of research cells from explicit structural roles."""
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELLS = ROOT / "corpus" / "research-cells.jsonl"
OUT = ROOT / "verification" / "research-cell-graph.json"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def role_signature(cell):
    return {
        "unit": cell["design"]["unit_role"],
        "claim": cell["inference"]["claim_type"],
        "validation": cell["validation"]["validation_role"],
        "fragility": cell["fragility"]["pattern"],
    }


def build(cells=None):
    cells = read_jsonl(CELLS) if cells is None else cells
    nodes = [{"id": cell["cell_id"], "domain": cell["domain"], "roles": role_signature(cell), "decision": cell["decision"]["role"]} for cell in cells]
    edges = []
    for left, right in combinations(cells, 2):
        a, b = role_signature(left), role_signature(right)
        shared = [role for role in a if a[role] == b[role]]
        material_mismatch = [role for role in a if a[role] != b[role]]
        if len(shared) >= 2 and ("fragility" in shared or "validation" in shared) and material_mismatch:
            edges.append({"from": left["cell_id"], "to": right["cell_id"], "shared_roles": shared, "material_mismatch": material_mismatch})
    return {"nodes": nodes, "edges": edges, "rule": "An edge requires two shared roles, including fragility or validation; every edge retains its material mismatches."}


def main():
    graph = build()
    OUT.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"cells": len(graph["nodes"]), "edges": len(graph["edges"])}))


if __name__ == "__main__":
    main()
