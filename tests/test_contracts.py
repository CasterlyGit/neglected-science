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
        self.assertEqual(6, record["systems"]["system_one"]["source_feasible_records"])
        self.assertEqual("no-justified-trio", record["systems"]["system_one"]["verdict"])
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

    def test_system_one_quality_benchmark_is_predeclared_and_blinded(self):
        schema = json.loads((ROOT / "schemas" / "system-one-quality-benchmark.schema.json").read_text())
        record = json.loads((ROOT / "verification" / "system-one-quality-benchmark.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(record)))
        self.assertEqual("predeclared-not-run", record["status"])

    def test_system_one_selector_v2_is_versioned_against_the_repeated_bottleneck(self):
        record = json.loads((ROOT / "verification" / "system-one-improvement-1.json").read_text())
        self.assertEqual("system-one-selector-v2", record["improvement_id"])
        self.assertEqual(["system-one-batch-1", "system-one-batch-2"], record["based_on_batches"])


if __name__ == "__main__":
    unittest.main()
