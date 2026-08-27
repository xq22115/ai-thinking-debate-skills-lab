#!/usr/bin/env python3
import importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2];P=ROOT/"control-plane/scripts/ordinary_chat_release_gate.py";s=importlib.util.spec_from_file_location("gate",P);gate=importlib.util.module_from_spec(s);s.loader.exec_module(gate)
def state(ok=True):
 sha="a"*40;return {"integration_sha":sha,"lanes":{f"A{i:02d}":{"result":"PASS","integration_sha":sha} for i in range(1,11)},"required_checks_enforced":ok,"ordinary_chat_live_e2e":ok,"local_device_live_e2e":ok,"browser_live_e2e":ok,"ux_flight_recorder_live_evidence":ok,"unresolved_blockers":[] if ok else ["device_offline"]}
class GateTests(unittest.TestCase):
 def test_complete_requires_every_gate(self):self.assertTrue(gate.evaluate(state(True))["complete"])
 def test_ci_lanes_alone_cannot_claim_complete(self):
  r=gate.evaluate(state(False));self.assertEqual(r["result"],"BLOCKED");self.assertIn("required_checks_enforced",r["reasons"]);self.assertIn("ordinary_chat_live_e2e",r["reasons"])
 def test_single_lane_sha_drift_blocks(self):
  x=state(True);x["lanes"]["A07"]["integration_sha"]="b"*40;self.assertIn("lane_sha_mismatch:A07",gate.evaluate(x)["reasons"])
if __name__=="__main__":unittest.main()
