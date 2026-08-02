import json
import unittest
from pathlib import Path

from scripts import pipeline


ROOT = Path(__file__).resolve().parents[1]


def jsonl(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


class DeterministicPipelineTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
