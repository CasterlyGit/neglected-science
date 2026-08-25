from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from fevkit.audit import audit_bundle
from fevkit.io import canonical_json
from fevkit.recorder import RunRecorder
from fevkit.replay import replay_bundle
from fevkit.rocrate import PROCESS_RUN_PROFILE, export_rocrate

ROOT = Path(__file__).resolve().parents[1]
COMPLETE = ROOT / "examples" / "complete"
INCOMPLETE = ROOT / "examples" / "incomplete"


def clone_bundle(source: Path, destination: Path) -> Path:
    shutil.copytree(source, destination)
    return destination


class FEVKitTests(unittest.TestCase):
    def test_01_complete_bundle_passes(self):
        self.assertEqual(audit_bundle(COMPLETE).status, "PASS")

    def test_02_complete_bundle_reaches_v3(self):
        report = audit_bundle(COMPLETE)
        self.assertEqual(report.computed_stage, "V3")
        self.assertEqual(report.qualifiers, ["B", "H", "S", "R"])

    def test_03_incomplete_bundle_fails(self):
        report = audit_bundle(INCOMPLETE)
        self.assertEqual(report.status, "FAIL")
        self.assertGreater(report.counts["error"], 10)

    def test_04_hash_mismatch_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            bundle = clone_bundle(COMPLETE, Path(temp) / "bundle")
            (bundle / "artifacts" / "input.txt").write_text("tampered")
            codes = {item.code for item in audit_bundle(bundle).findings}
            self.assertIn("INPUT.HASH_MISMATCH", codes)

    def test_05_missing_file_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            bundle = clone_bundle(COMPLETE, Path(temp) / "bundle")
            (bundle / "artifacts" / "trace.json").unlink()
            codes = {item.code for item in audit_bundle(bundle).findings}
            self.assertIn("ARTIFACT.MISSING_FILE", codes)

    def test_06_unresolved_reference_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            bundle = clone_bundle(COMPLETE, Path(temp) / "bundle")
            document = json.loads((bundle / "run.json").read_text())
            document["run"]["steps"][0]["inputs"].append("does-not-exist")
            (bundle / "run.json").write_text(canonical_json(document))
            codes = {item.code for item in audit_bundle(bundle).findings}
            self.assertIn("REF.STEP_INPUT", codes)

    def test_07_unsupported_claim_is_detected(self):
        codes = {item.code for item in audit_bundle(INCOMPLETE).findings}
        self.assertIn("CLAIM.UNSUPPORTED", codes)

    def test_08_clinical_boundary_is_reported(self):
        codes = {item.code for item in audit_bundle(INCOMPLETE).findings}
        self.assertIn("CLAIM.CLINICAL_BOUNDARY", codes)

    def test_09_overclaim_is_detected(self):
        codes = {item.code for item in audit_bundle(INCOMPLETE).findings}
        self.assertIn("VALIDATION.OVERCLAIM", codes)

    def test_10_sarif_is_well_formed(self):
        sarif = audit_bundle(INCOMPLETE).to_sarif()
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertTrue(sarif["runs"][0]["results"])

    def test_11_replay_preflight_does_not_execute(self):
        result = replay_bundle(COMPLETE)
        self.assertEqual(result.status, "PREFLIGHT")
        self.assertFalse(result.executed)

    def test_12_replay_regenerates_expected_hash(self):
        result = replay_bundle(COMPLETE, execute=True)
        self.assertEqual(result.status, "PASS")
        self.assertTrue(all(item["match"] for item in result.artifact_results))

    def test_13_rocrate_uses_process_run_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            output = export_rocrate(COMPLETE, Path(temp) / "crate")
            metadata = json.loads((output / "ro-crate-metadata.json").read_text())
            root = next(item for item in metadata["@graph"] if item["@id"] == "./")
            self.assertIn(PROCESS_RUN_PROFILE, {item["@id"] for item in root["conformsTo"]})

    def test_14_recorder_writes_content_addressed_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "input.txt").write_text("synthetic")
            recorder = RunRecorder(root, run_id="recorded-run", title="Recorded run", objective="Exercise the SDK", system_version="1.0.0")
            item = recorder.add_input(item_id="input-one", path="input.txt", media_type="text/plain", sensitive=False)
            recorder.finish()
            self.assertEqual(len(item["sha256"]), 64)
            self.assertTrue((root / "run.json").is_file())


if __name__ == "__main__":
    unittest.main()
