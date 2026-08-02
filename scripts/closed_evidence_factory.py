#!/usr/bin/env python3
"""Emit interview candidates only when machine-readable evidence clears every gate."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_jsonl(path):
    return [json.loads(x) for x in (ROOT/path).read_text().splitlines() if x.strip()]

def evaluate(candidate):
    uncertainty=" ".join(candidate.get("uncertainties",[])).lower()
    evidence=candidate.get("public_evidence",[])
    row_level="row-level" in uncertainty or "row level" in uncertainty
    return {
        "source_candidate_id":candidate["candidate_id"],
        "question":candidate["question"],
        "construction":bool(evidence) and candidate.get("unresolved") is not None,
        "actual_data":row_level and "abstract-level" not in uncertainty,
        "self_contained":row_level and "specialist" not in uncertainty,
        "verdict":"interview-ready" if bool(evidence) and row_level and "abstract-level" not in uncertainty and "specialist" not in uncertainty else "rejected-before-interview",
        "reasons":[] if bool(evidence) and row_level and "abstract-level" not in uncertainty and "specialist" not in uncertainty else ["requires row-level, non-abstract, self-contained evidence"]
    }

def run(input_path="opportunities/candidates.jsonl"):
    return [evaluate(row) for row in read_jsonl(input_path)]

if __name__=="__main__":
    rows=run(); out=ROOT/"verification"/"factory-cycle-2.jsonl"
    out.write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in rows))
    print(json.dumps({"emitted":len(rows),"interview_ready":sum(x["verdict"]=="interview-ready" for x in rows)}))
