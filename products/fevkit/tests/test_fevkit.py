from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from fevkit import RunRecorder, audit_bundle, export_ro_crate, replay_bundle, sarif_document
from fevkit.core import FEVKitError

HERE = Path(__file__).resolve().parents[1]
COMPLETE = HERE / "examples" / "complete"
INCOMPLETE = HERE / "examples" / "incomplete"


class FEVKitTests(unittest.TestCase):
    def test_01_complete_bundle_passes(self): self.assertEqual(audit_bundle(COMPLETE).status, "PASS")
    def test_02_complete_bundle_reaches_v3(self): self.assertEqual(audit_bundle(COMPLETE).computed_stage, "V3")
    def test_03_complete_integrity_is_verified(self): self.assertTrue(audit_bundle(COMPLETE).integrity["all_declared_files_verified"])
    def test_04_broken_bundle_fails(self): self.assertEqual(audit_bundle(INCOMPLETE).status, "FAIL")
    def test_05_overclaim_is_detected(self): self.assertIn("VALIDATION.OVERCLAIM", {x.code for x in audit_bundle(INCOMPLETE).findings})
    def test_06_clinical_boundary_is_preserved(self): self.assertIn("CLAIM.CLINICAL_BOUNDARY", {x.code for x in audit_bundle(INCOMPLETE).findings})
    def test_07_replay_preflight_does_not_execute(self): self.assertFalse(replay_bundle(COMPLETE)["executed"])
    def test_08_replay_executes_and_matches(self): self.assertTrue(replay_bundle(COMPLETE, execute=True)["matched"])
    def test_09_replay_allowlist_is_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "bundle"; shutil.copytree(COMPLETE, target)
            manifest = json.loads((target / "run.json").read_text()); manifest["run"]["replay"]["command"] = ["sh", "-c", "true"]
            (target / "run.json").write_text(json.dumps(manifest))
            with self.assertRaises(FEVKitError): replay_bundle(target, execute=True)
    def test_10_sarif_is_well_formed(self): self.assertEqual(sarif_document(audit_bundle(INCOMPLETE))["version"], "2.1.0")
    def test_11_rocrate_has_process_run_profile(self):
        crate = export_ro_crate(COMPLETE); root = next(x for x in crate["@graph"] if x["@id"] == "./")
        self.assertIn("https://w3id.org/ro/wfrun/process/0.5", {x["@id"] for x in root["conformsTo"]})
    def test_12_unsafe_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "bundle"; shutil.copytree(COMPLETE, target)
            manifest = json.loads((target / "run.json").read_text()); manifest["run"]["inputs"][0]["path"] = "../escape.bin"
            (target / "run.json").write_text(json.dumps(manifest))
            self.assertIn("ARTIFACT.UNSAFE_PATH", {x.code for x in audit_bundle(target).findings})
    def test_13_claim_support_is_counted(self):
        metrics = audit_bundle(COMPLETE).metrics; self.assertEqual(metrics["claims_with_support"], metrics["claims_total"])
    def test_14_recorder_hashes_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / "data.txt").write_text("hello\n")
            recorder = RunRecorder(root, run_id="recorded", title="Recorded", objective="Test.", domain="test", system_name="test", system_version="1")
            self.assertEqual(len(recorder.add_input("data", "data.txt")["sha256"]), 64)

if __name__ == "__main__": unittest.main()
