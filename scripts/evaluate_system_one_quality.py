#!/usr/bin/env python3
"""Blinded structural audit for the frozen System-1 v2 held-out corpus."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRITERIA = [
    "primary claim and location", "official data and acquisition evidence", "system mapping",
    "unit mapping", "measurement and baseline mapping", "inference and validation-gap mapping",
    "fragility and alternative explanation", "independent check or explicit infeasibility",
    "material mismatch and correct gate disposition",
    "future System-2 verdict is discriminating, claim-bounded, and action-specific",
]


def load_json(path):
    return json.loads((ROOT / path).read_text())


def blinded_contract_score(cell, audit):
    """Score the redacted structural fields; historical decision is intentionally unused."""
    source = cell["source"]
    design = cell["design"]
    measurement = cell["measurement"]
    inference = cell["inference"]
    validation = cell["validation"]
    fragility = cell["fragility"]
    provenance = cell["provenance"]
    outcomes = audit["outcomes"]
    checks = [
        bool(source["primary_url"] and source["claim_location"] and source["evidence_statement"]),
        bool(provenance["data_url"] and provenance["data_location"] and provenance["acquisition_status"]),
        bool(cell["system"]["phenomenon"] and cell["system"]["scope_boundary"]),
        bool(design["unit_description"] and design["unit_role"]),
        bool(measurement["measurement_rule"] and inference["published_claim"] and validation["published_baseline"]),
        bool(inference["scope_boundary"] and validation["independent_check"]),
        bool(fragility["pattern"] and fragility["alternative_explanation"]),
        bool(validation["independent_check"] or validation["validation_role"] == "unavailable"),
        bool(audit["v2_disposition"] and audit["named_gap"]),
        all(outcomes[key] for key in ("positive", "null", "contrary")),
    ]
    return dict(zip(CRITERIA, checks))


def evaluate():
    heldout = load_json("verification/system-one-quality-heldout-1.json")
    cells = {row["cell_id"]: row for row in (json.loads(line) for line in (ROOT / "corpus/research-cells.jsonl").read_text().splitlines())}
    results = []
    for audit in heldout["records"]:
        # Deliberately do not pass cells[cell_id]["decision"] to the scorer.
        score = blinded_contract_score(cells[audit["cell_id"]], audit)
        results.append({"cell_id": audit["cell_id"], "all_criteria_pass": all(score.values()), "criteria": score,
                        "v2_disposition": audit["v2_disposition"]})
    pass_rate = sum(row["all_criteria_pass"] for row in results) / len(results)
    eligible = [r["cell_id"] for r in results if r["v2_disposition"] == "eligible-for-full-audit"]
    leniency_path = ROOT / "verification/system-one-quality-leniency-audit-1.json"
    leniency_complete = leniency_path.exists() and load_json("verification/system-one-quality-leniency-audit-1.json")["verdict"] == "source-assertions-retained-no-promotion"
    return {
        "benchmark_id": heldout["benchmark_id"], "status": "evaluated", "record_count": len(results),
        "blinded": True, "frozen_corpus_revision": heldout["frozen_corpus_revision"],
        "criteria": CRITERIA, "pass_rate": pass_rate, "target_pass_rate": {"minimum": 0.8, "maximum": 0.9},
        "records": results, "v2_eligible_for_full_audit": eligible,
        "quality_verdict": "leniency-audit-required" if pass_rate > 0.9 and not leniency_complete else "leniency-audit-complete-no-reliability-claim" if pass_rate > 0.9 else "within-target" if pass_rate >= 0.8 else "process-improvement-required",
        "selection_verdict": "no-justified-trio" if len(eligible) < 3 else "full-audit-trio-required",
        "leniency_audit_complete": leniency_complete,
        "limitation": "This is a blinded mechanical contract audit, not an independent scientific-source audit; it establishes record completeness and disposition traceability only.",
        "next_permitted_action": "Generate one contrasting three-record V2 batch from source-specific unresolved gaps; do not promote the two provisional records or start System-2 selection." if leniency_complete else "Run a source-level leniency audit on a predeclared subset; do not promote the two provisional records or start System-2 selection.",
    }


def main():
    result = evaluate()
    (ROOT / "verification/system-one-quality-benchmark.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pass_rate": result["pass_rate"], "selection": result["selection_verdict"], "quality": result["quality_verdict"]}))


if __name__ == "__main__":
    main()
