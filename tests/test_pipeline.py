import json
import unittest
from pathlib import Path

from scripts import pipeline
from scripts import ecoli_analysis
from scripts import system_guards
from scripts import closed_evidence_factory


ROOT = Path(__file__).resolve().parents[1]


def jsonl(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


class DeterministicPipelineTests(unittest.TestCase):
    def test_closed_evidence_factory_refuses_abstract_only_leads(self):
        rows = closed_evidence_factory.run()
        self.assertGreater(len(rows), 0)
        self.assertTrue(all(row["verdict"] == "rejected-before-interview" for row in rows))
    def test_closed_evidence_benchmark_rejects_any_failed_gate(self):
        result = system_guards.check_benchmark()
        self.assertEqual("pass", result["benchmark"])
        self.assertEqual(5, result["cases"])

    def test_ecoli_transaction_verifies_durable_inputs_and_result(self):
        self.assertEqual("pass", system_guards.check_transaction()["transaction"])

    def test_synthetic_shared_measurement_artifact_is_detected(self):
        result = system_guards.synthetic_artifact_check()
        self.assertTrue(result["pass"])
        self.assertEqual(-1.0, result["naive"])
        self.assertFalse(system_guards.promotion_allowed({"selection_quality":"partial", "execution_integrity":"partial"}))
    def test_ecoli_pearson_and_fisher_summary(self):
        self.assertAlmostEqual(1.0, ecoli_analysis.pearson([(1, 2), (2, 4), (3, 6)]))
        self.assertIsNone(ecoli_analysis.pearson([(1, 1), (1, 2), (1, 3)]))
        self.assertAlmostEqual(0.0, ecoli_analysis.fisher_mean([-0.5, 0.5]))

    def test_ecoli_partition_definitions_are_disjoint_from_final_outcomes(self):
        self.assertNotIn("4", ecoli_analysis.PARTITIONS["exploration"][0])
        self.assertNotIn("4", ecoli_analysis.PARTITIONS["validation"][0])
        self.assertIn("4", ecoli_analysis.PARTITIONS["final"][0])

    def test_ecoli_bootstrap_interval_is_deterministic(self):
        self.assertEqual(
            ecoli_analysis.bootstrap_interval([-0.8, -0.2, 0.1], iterations=100, seed=5),
            ecoli_analysis.bootstrap_interval([-0.8, -0.2, 0.1], iterations=100, seed=5),
        )
    def test_normalization_and_concept_detection(self):
        self.assertEqual("tree cooling", pipeline.normalize_title("Tree—Cooling!"))
        self.assertIn("memory-path-dependence", pipeline.concepts_for("history-dependent battery response"))
        self.assertEqual("negative", pipeline.polarity_for("trees reduced surface temperature"))

    def test_corpus_bounds_and_source_mix(self):
        sources = jsonl("corpus/sources.jsonl")
        self.assertGreaterEqual(len(sources), 40)
        self.assertLessEqual(len(sources), 80)
        domains = {row["domain"] for row in sources}
        self.assertEqual(4, len(domains))
        for domain in domains:
            domain_rows = [row for row in sources if row["domain"] == domain]
            self.assertTrue(any(row["source_type"] == "dataset-documentation" for row in domain_rows))
            self.assertTrue(any(row["source_type"] != "dataset-documentation" for row in domain_rows))

    def test_all_discovery_engines_produce_candidates(self):
        candidates = jsonl("opportunities/candidates.jsonl")
        self.assertEqual({"explicit", "contradiction", "translation", "data-use"}, {row["gap_type"] for row in candidates})
        self.assertEqual(len(candidates), len({row["candidate_id"] for row in candidates}))

    def test_dossiers_and_finalists(self):
        dossiers = jsonl("opportunities/dossiers.jsonl")
        self.assertGreaterEqual(len(dossiers), 10)
        self.assertLessEqual(len(dossiers), 20)
        self.assertEqual(3, sum(row["status"] == "finalist" for row in dossiers))
        rankings = json.loads((ROOT / "opportunities" / "rankings.json").read_text())
        self.assertEqual({"balanced", "rigor_first", "impact_first"}, set(rankings["profiles"]))
        self.assertEqual(3, len(rankings["scientific_review_finalists"]))

    def test_milestone_6_challenges_cover_finalists(self):
        dossiers = jsonl("opportunities/dossiers.jsonl")
        finalists = {row["id"] for row in dossiers if row["status"] == "finalist"}
        challenges = jsonl("verification/novelty-challenges.jsonl")
        searches = jsonl("verification/novelty-searches.jsonl")
        audits = jsonl("verification/dataset-audits.jsonl")
        self.assertEqual(finalists, {row["finalist_id"] for row in challenges})
        self.assertEqual(3, len(challenges))
        self.assertTrue(all(row["disposition"] in {"rejected", "reframed", "gated", "surviving"} for row in challenges))
        self.assertTrue(all(row["missing_expertise"] for row in challenges))
        search_ids = {row["search_id"] for row in searches}
        audit_ids = {row["audit_id"] for row in audits}
        for challenge in challenges:
            self.assertTrue(set(challenge["search_ids"]) <= search_ids)
            self.assertTrue(set(challenge["dataset_audit_ids"]) <= audit_ids)

    def test_revised_candidate_factory_rejects_known_pilot_failures(self):
        admissions = jsonl("verification/candidate-admissions.jsonl")
        replay = jsonl("verification/gauntlet-replays.jsonl")[0]
        self.assertEqual(3, len(admissions))
        self.assertTrue(all(row["retrospective"] for row in admissions))
        self.assertTrue(all(row["emission_verdict"] == "excluded-raw-lead" for row in admissions))
        for row in admissions:
            self.assertTrue(any(check["status"] == "fail" for check in row["construction_checks"].values()))
        self.assertEqual([], replay["interview_ready_ids"])
        self.assertFalse(replay["trio_created"])
        self.assertFalse(replay["broad_pipeline_authorized"])
        self.assertFalse(replay["would_reach_confirmation_milestone_6"])

    def test_trio_contract_requires_three_ready_targets_and_two_survivors(self):
        self.assertEqual(3, pipeline.TRIO_SIZE)
        self.assertEqual(2, pipeline.MINIMUM_INTERVIEW_SURVIVORS)

    def test_manual_priority_cycle_reaches_confirmation_with_primary_and_reserve(self):
        leads = jsonl("opportunities/candidate-priority-list.jsonl")
        reviews = jsonl("verification/target-reviews.jsonl")
        result = json.loads((ROOT / "verification" / "cycle-result.json").read_text())
        selected = {row["lead_id"] for row in leads if row["selection_status"] == "selected"}
        self.assertEqual(3, len(selected))
        self.assertEqual(selected, {row["lead_id"] for row in reviews})
        self.assertTrue(all(all(check["status"] == "pass" for check in row["construction_checks"].values()) for row in reviews))
        self.assertTrue(all(row["first_interview"]["verdict"] == "admitted" for row in reviews))
        self.assertEqual(2, sum(row["confirmation_challenge"]["disposition"] == "surviving" for row in reviews))
        self.assertTrue(result["milestone_6_complete"])
        self.assertIn(result["primary_id"], result["milestone_7_eligible_ids"])
        self.assertIn(result["reserve_id"], result["milestone_7_eligible_ids"])
        self.assertTrue(result["selection_deferred"])


if __name__ == "__main__":
    unittest.main()
