#!/usr/bin/env python3
import importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2];P=ROOT/"control-plane/scripts/chat_ux_report.py";s=importlib.util.spec_from_file_location("ux",P);ux=importlib.util.module_from_spec(s);s.loader.exec_module(ux)
class ReportTests(unittest.TestCase):
 def test_percentiles_and_diagnostics(self):
  events=[{"type":"assistant_stream_delta","streamGapMs":100},{"type":"assistant_stream_delta","streamGapMs":2000},{"type":"chat_switch_to_paint","durationMs":700},{"type":"long_animation_frame","durationMs":250},{"type":"long_animation_frame","durationMs":300},{"type":"long_animation_frame","durationMs":400}];r=ux.summarize(events);self.assertEqual(r["contentCapture"],"metadata_only");self.assertTrue(r["diagnosticSignals"]["stream_stall_suspected"]);self.assertTrue(r["diagnosticSignals"]["chat_switch_render_stall_suspected"]);self.assertTrue(r["diagnosticSignals"]["main_thread_jank_suspected"])
 def test_no_data_does_not_invent_pass(self):
  r=ux.summarize([]);self.assertIsNone(r["metrics"]["stream_gap_ms"]["p95"]);self.assertFalse(any(r["diagnosticSignals"].values()))
if __name__=="__main__":unittest.main()
