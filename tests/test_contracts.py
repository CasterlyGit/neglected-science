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


if __name__ == "__main__":
    unittest.main()
