#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,pathlib,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]; PATH=ROOT/"control-plane/scripts/ordinary_chat_coordination.py"; spec=importlib.util.spec_from_file_location("coord",PATH); coord=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(coord)
def ev(kind,seq,parent,actor="chat-a",handoff=None):
 return coord.make_event(task_ref="ordinary-chat-v6",actor_id=actor,branch=f"lane/{actor}",base_sha="a"*40,head_sha=("b" if actor=="chat-a" else "c")*40,event_type=kind,seq=seq,parent_event_hash=parent,run_id="run-1",trace_id="trace-1",handoff_to=handoff)
class CoordinationTests(unittest.TestCase):
 def test_explicit_handoff_prevents_stale_writer(self):
  e1=ev("REGISTER",1,None);e2=ev("CLAIM",2,e1["event_hash"]);e3=ev("HANDOFF",3,e2["event_hash"],handoff="chat-b");e4=ev("CHECKPOINT",4,e3["event_hash"],actor="chat-b");self.assertEqual(coord.replay([e1,e2,e3,e4])["current_owner"],"chat-b");stale=ev("CHECKPOINT",5,e4["event_hash"],actor="chat-a")
  with self.assertRaisesRegex(coord.CoordinationError,"checkpoint_by_non_owner"):coord.replay([e1,e2,e3,e4,stale])
 def test_second_claim_is_split_brain_veto(self):
  e1=ev("CLAIM",1,None);e2=ev("CLAIM",2,e1["event_hash"],actor="chat-b")
  with self.assertRaisesRegex(coord.CoordinationError,"split_brain_claim"):coord.replay([e1,e2])
 def test_tamper_breaks_hash_chain(self):
  e1=ev("REGISTER",1,None);e1["branch"]="tampered"
  with self.assertRaisesRegex(coord.CoordinationError,"event_hash_mismatch"):coord.replay([e1])
 def test_append_persists_and_replays(self):
  with tempfile.TemporaryDirectory() as td:
   path=pathlib.Path(td)/"events.jsonl";e1=ev("CLAIM",1,None);self.assertEqual(coord.append_event(path,e1)["current_owner"],"chat-a");e2=ev("RELEASE",2,e1["event_hash"]);self.assertIsNone(coord.append_event(path,e2)["current_owner"]);self.assertEqual(coord.replay(coord.load_events(path))["event_count"],2)
if __name__=="__main__":unittest.main()
