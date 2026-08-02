import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class OpportunityDossierContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(
            (ROOT / "schemas" / "opportunity-dossier.schema.json").read_text()
        )
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def load_fixture(self, name):
        return json.loads((ROOT / "tests" / "fixtures" / name).read_text())

    def test_representative_dossier_is_valid(self):
        errors = list(
            self.validator.iter_errors(self.load_fixture("valid-opportunity.json"))
        )
        self.assertEqual([], errors)

    def test_incomplete_and_overconfident_dossier_is_rejected(self):
        errors = list(
            self.validator.iter_errors(self.load_fixture("invalid-opportunity.json"))
        )
        self.assertGreaterEqual(len(errors), 5)

    def test_ecoli_preregistration_is_valid_and_frozen(self):
        schema = json.loads((ROOT / "schemas" / "preregistration.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        for name in ("preregistration-v1.json", "preregistration-v2.json"):
            record = json.loads((ROOT / "experiments" / "ecoli-regression" / name).read_text())
            self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
            self.assertEqual("frozen-before-final-holdout-access", record["status"])

    def test_ecoli_final_result_is_governed(self):
        schema = json.loads((ROOT / "schemas" / "investigation-result.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "ecoli-final-result.json").read_text())
        Draft202012Validator.check_schema(schema)
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))

    def test_future_executable_preregistration_contract_is_valid(self):
        schema = json.loads((ROOT / "schemas" / "executable-preregistration.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        example = {"base_preregistration": "experiments/example/preregistration-v1.json", "algorithm_revision": "abcdef1", "uncertainty_procedure": "Fixed bootstrap calculation with a declared seed.", "robustness_procedures": ["Leave one comparison out."], "final_invocation": "python analysis.py --partition final", "durable_result_receipt": "verification/example-final-result.json"}
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(example)))

    def test_first_improvement_cycle_is_governed(self):
        schema = json.loads((ROOT / "schemas" / "improvement-cycle.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "improvement-cycle-1.json").read_text())
        Draft202012Validator.check_schema(schema)
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual(1, record["proposal"]["level"])

    def test_process_integrity_verdict_rewards_only_a_verified_method_verdict(self):
        from scripts import evaluate_process_integrity
        schema = json.loads((ROOT / "schemas" / "process-integrity-verdict.schema.json").read_text())
        record = evaluate_process_integrity.evaluate("2026-08-02T16:00:00Z")
        Draft202012Validator.check_schema(schema)
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual("verified-final-method-verdict", record["reward_target"])
        self.assertEqual("continue-bounded-cycle", record["verdict"])
        self.assertTrue(record["evidence"]["investigation_transaction_valid"])
        self.assertEqual(0, record["evidence"]["current_ready_targets"])
        self.assertEqual(1, record["systems"]["system_one"]["source_feasible_records"])
        self.assertEqual("form-target-trio", record["systems"]["system_one"]["verdict"])
        self.assertFalse(record["systems"]["system_two"]["investigation_verdict_ready"])

    def test_system_one_batch_retains_a_three_record_defeat(self):
        schema = json.loads((ROOT / "schemas" / "system-one-batch.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-batch-1.json").read_text())
        Draft202012Validator.check_schema(schema)
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual("no-justified-trio", record["verdict"])

    def test_system_one_cycle_keeps_the_next_batch_separate_from_a_defeat(self):
        schema = json.loads((ROOT / "schemas" / "system-one-cycle.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-cycle.json").read_text())
        Draft202012Validator.check_schema(schema)
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))

    def test_second_system_one_batch_is_a_three_record_defeat(self):
        schema = json.loads((ROOT / "schemas" / "system-one-batch.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-batch-2.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))

    def test_system_two_shadow_review_is_non_promoting(self):
        from scripts import review_system_two_shadow
        schema = json.loads((ROOT / "schemas" / "system-two-shadow-review.schema.json").read_text())
        record = review_system_two_shadow.review()
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual(0, record["system_two_ready_records"])
        self.assertEqual(0, record["candidate_packets"])

    def test_system_one_quality_benchmark_is_blinded_and_rejects_false_success(self):
        from scripts import evaluate_system_one_quality
        schema = json.loads((ROOT / "schemas" / "system-one-quality-benchmark.schema.json").read_text())
        record = evaluate_system_one_quality.evaluate()
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual("evaluated", record["status"])
        self.assertTrue(record["blinded"])
        self.assertEqual(10, record["record_count"])
        self.assertEqual("leniency-audit-complete-no-reliability-claim", record["quality_verdict"])
        self.assertTrue(record["leniency_audit_complete"])
        self.assertEqual("no-justified-trio", record["selection_verdict"])

    def test_system_one_selector_v2_is_versioned_against_the_repeated_bottleneck(self):
        record = json.loads((ROOT / "verification" / "system-one-improvement-1.json").read_text())
        self.assertEqual("system-one-selector-v2", record["improvement_id"])
        self.assertEqual(["system-one-batch-1", "system-one-batch-2"], record["based_on_batches"])

    def test_system_one_v2_preaudit_retains_a_fresh_nonpromoting_trio(self):
        schema = json.loads((ROOT / "schemas" / "system-one-v2-preaudit.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-v2-preaudit-1.json").read_text())
        errors = list(Draft202012Validator(schema).iter_errors(record))
        self.assertEqual([], errors)
        self.assertEqual("no-justified-trio", record["verdict"])
        self.assertEqual(0, sum(item["disposition"] == "eligible-for-full-audit" for item in record["records"]))
        self.assertTrue(all(item["failed_gate"] == "actual-data-fit" for item in record["records"]))

    def test_system_one_selector_v3_requires_real_content_before_screening(self):
        record = json.loads((ROOT / "verification" / "system-one-improvement-2.json").read_text())
        self.assertEqual("system-one-selector-v3", record["improvement_id"])
        self.assertEqual(["system-one-v2-preaudit-1"], record["based_on_batches"])
        self.assertIn("real official-file retrieval", record["change"])

    def test_system_one_v3_source_batch_preserves_checksum_failures(self):
        schema = json.loads((ROOT / "schemas" / "system-one-v3-source-batch.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-v3-source-batch-1.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual("source-verified-await-v2", record["verdict"])
        self.assertEqual(3, sum(item["disposition"] == "content-verified-eligible-for-v2" for item in record["records"]))
        rejected = json.loads((ROOT / "verification" / "system-one-v3-source-rejections-1.jsonl").read_text())
        self.assertFalse(rejected["retrieved_checksum"] == rejected["provider_checksum"])

    def test_system_one_v3_v2_audit_does_not_promote_a_near_trio(self):
        schema = json.loads((ROOT / "schemas" / "system-one-v3-v2-audit.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-v3-v2-audit-1.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual("no-justified-trio", record["verdict"])
        self.assertEqual(0, sum(item["disposition"] == "eligible-for-full-audit" for item in record["records"]))
        self.assertTrue(all(item["failed_gate"] == "actual-data-fit" or item["failed_gate"] == "nontrivial-consequence" for item in record["records"]))

    def test_system_one_seed_library_is_contract_first(self):
        schema = json.loads((ROOT / "schemas" / "system-one-seed-library-phase.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-seed-library-phase.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual(7, len(record["pre_admission_conditions"]))
        self.assertEqual(5, len(record["seed_patterns"]))

    def test_system_one_seed_queue_cannot_skip_pre_admission(self):
        schema = json.loads((ROOT / "schemas" / "system-one-seed-queue.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-seed-queue-1.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual(5, len(record["records"]))
        self.assertTrue(all(item["pre_admission_status"] == "evidence-pending-not-full-audit" for item in record["records"]))

    def test_seed_pre_admission_preserves_rejections_and_blocks_promotion(self):
        schema = json.loads((ROOT / "schemas" / "system-one-seed-pre-admission.schema.json").read_text())
        receipt = json.loads((ROOT / "verification" / "system-one-seed-pre-admission-1.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(receipt)))
        self.assertEqual(5, receipt["summary"]["records_screened"])
        self.assertEqual(1, receipt["summary"]["pre_admitted_count"])
        self.assertEqual(4, receipt["summary"]["rejected_count"])
        admitted = [row for row in receipt["records"] if row["disposition"] == "pre-admitted-seed"]
        self.assertEqual(["seed-home-range-calibration"], [row["seed_id"] for row in admitted])
        self.assertTrue(all(all(condition["status"] == "pass" for condition in row["conditions"]) for row in admitted))

    def test_seed_full_audit_is_a_non_promoting_prior_art_receipt(self):
        schema = json.loads((ROOT / "schemas" / "system-one-seed-full-audit.schema.json").read_text())
        receipt = json.loads((ROOT / "verification" / "system-one-seed-full-audit-1.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(receipt)))
        self.assertEqual("failed-gate-rejection-receipt", receipt["disposition"])
        self.assertEqual("prior-art-nontriviality", receipt["failed_gate"])

    def test_second_seed_screen_requires_nontriviality_preview(self):
        schema = json.loads((ROOT / "schemas" / "system-one-seed-pre-admission-v2.schema.json").read_text())
        receipt = json.loads((ROOT / "verification" / "system-one-seed-pre-admission-2.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(receipt)))
        self.assertEqual(1, receipt["summary"]["pre_admitted_count"])
        admitted = [row for row in receipt["records"] if row["disposition"] == "pre-admitted-seed"]
        self.assertEqual(["seed-stream-biofilm-compartment-contrast"], [row["seed_id"] for row in admitted])
        self.assertEqual("pass", admitted[0]["nontriviality_preview"]["status"])

    def test_seed_candidate_packet_keeps_trio_gate_closed(self):
        schema = json.loads((ROOT / "schemas" / "system-one-seed-candidate-packet.schema.json").read_text())
        packet = json.loads((ROOT / "verification" / "system-one-seed-candidate-packet-1.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(packet)))
        self.assertEqual("interview-ready-domain-specific-candidate-packet", packet["disposition"])
        self.assertIn("exactly-three candidate trio", packet["plain_language_verdict"])

    def test_pattern_search_preserves_local_and_prior_art_rejections(self):
        schema = json.loads((ROOT / "schemas" / "system-one-pattern-search.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-pattern-search-2.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual(1, sum(row["disposition"] == "eligible-for-seven-condition-pre-admission" for row in record["records"]))


if __name__ == "__main__":
    unittest.main()
