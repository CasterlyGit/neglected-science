#!/usr/bin/env python3
"""Render a plain-language cross-domain comparison report from conservative graph edges."""
import json
from pathlib import Path

try:
    from scripts.build_research_graph import build, read_jsonl
except ModuleNotFoundError:  # direct script invocation
    from build_research_graph import build, read_jsonl

ROOT = Path(__file__).resolve().parents[1]
CELLS = ROOT / "corpus" / "research-cells.jsonl"
REPORT = ROOT / "reports" / "research-comparison-atlas.md"


def main():
    cells = read_jsonl(CELLS)
    by_id = {cell["cell_id"]: cell for cell in cells}
    graph = build(cells)
    lines = ["# Research comparison atlas", "", "## Final verdict", "", "**STRUCTURAL VERDICT: LIMITED SUPPORT — NO ACTIONABLE CROSS-DOMAIN LEAD.**", "", "The seed contains a small number of evidence-backed structural connections. Each connection retains a material mismatch, so none establishes a shared scientific mechanism or creates a new target by itself. The strategic-lead screen must still pass source, data, novelty, consequence, and self-contained-interpretation gates.", "", "## Qualified comparisons", ""]
    if not graph["edges"]:
        lines.append("No pair shares two required structural roles while retaining a material mismatch.")
    for edge in graph["edges"]:
        left, right = by_id[edge["from"]], by_id[edge["to"]]
        lines += [f"### {left['title']} ↔ {right['title']}", "", f"- Shared structural roles: {', '.join(edge['shared_roles'])}.", f"- Material mismatch retained: {', '.join(edge['material_mismatch'])}.", f"- Plain meaning: both studies expose a named way evidence can become unavailable or non-independent, but they make different kinds of claims about different units.", f"- Not established: a common scientific mechanism or a transferable scientific conclusion.", ""]
    lines += ["## Cells that do not connect yet", ""]
    connected = {edge["from"] for edge in graph["edges"]} | {edge["to"] for edge in graph["edges"]}
    for cell in cells:
        if cell["cell_id"] not in connected:
            lines.append(f"- **{cell['title']}**: retained as `{cell['decision']['role']}`; it needs a more specific compatible comparison before it can support an atlas conclusion.")
    lines += ["", "## Next permitted action", "", "Acquire and audit public files for a named gated cell, then recompute this report. Do not add a connection merely to make the map denser."]
    REPORT.write_text("\n".join(lines) + "\n")
    print(json.dumps({"cells": len(cells), "qualified_comparisons": len(graph["edges"])}))


if __name__ == "__main__":
    main()
