#!/usr/bin/env python3
"""Heterogeneous v6 lane validator. Lane PASS is scoped evidence, never global COMPLETE."""
from __future__ import annotations
import argparse,json,os,pathlib,re,subprocess,sys
from typing import Callable
ROOT=pathlib.Path(__file__).resolve().parents[2];BASELINE="6a46c5d31fadf8c1a49685d8e4cd8f8be151342c";LANE_RE=re.compile(r"^v6-(a\d{2})-")
GOAL=ROOT/"control-plane/ai-system/configs/ordinary-chat-v6-goal-contract.json";OBS=ROOT/"control-plane/ai-system/configs/ordinary-chat-v6-observability.json";MCP_COMPAT=ROOT/"control-plane/ai-system/configs/ordinary-chat-v6-mcp-compatibility.json";UPSTREAM=ROOT/"research/ordinary-chat-v6/2026-08-v6-upstream-matrix.json";CLOSURE=ROOT/"research/ordinary-chat-v6/closure-state.json";EVIDENCE_DIR=ROOT/"research/ordinary-chat-v6/lanes"
class Failure(RuntimeError):pass
def require(ok,msg):
 if not ok:raise Failure(msg)
def load(path):return json.loads(path.read_text(encoding="utf-8"))
def run(argv,cwd=ROOT,timeout=600):
 cp=subprocess.run(argv,cwd=cwd,text=True,capture_output=True,timeout=timeout,check=False)
 if cp.returncode:raise Failure(f"command_failed:{argv}:{cp.returncode}:{cp.stdout[-1500:]}:{cp.stderr[-1500:]}")
 return cp.stdout
def baseline_ancestor():
 require(subprocess.run(["git","merge-base","--is-ancestor",BASELINE,"HEAD"],cwd=ROOT,check=False).returncode==0,"baseline_not_ancestor")
def evidence(lane):
 path=EVIDENCE_DIR/f"{lane}.json";require(path.is_file(),f"lane_evidence_missing:{lane}");item=load(path);require(item.get("lane")==lane,"lane_evidence_identity");require(item.get("baselineSha")==BASELINE,"lane_evidence_baseline");require(item.get("scopeResult")=="PASS","lane_scope_not_pass");require(isinstance(item.get("evidence"),list) and len(item["evidence"])>=2,"lane_evidence_too_thin");return item

def a01():
 c=load(GOAL);require(c["ordinaryChatFirst"] is True,"ordinary_chat_not_primary");require(c["preserveExistingCapabilities"] is True,"preservation_not_required");require(c["deepReasoningAndResponsivenessAreSeparate"] is True,"reasoning_speed_conflated");require([x["id"] for x in c["goalConfirmations"]]==[f"G{i:02d}" for i in range(1,11)],"ten_goal_confirmations_missing");anti=set(c["antiFake"])
 for token in ["repository_proof_is_not_live_chat_proof","self_test_is_not_user_task_completion","do_not_trade_reasoning_quality_for_speed","do_not_delete_history_as_primary_performance_fix"]:require(token in anti,f"anti_fake_missing:{token}")
 evidence("A01");return ["10_goal_confirmations","ordinary_chat_first","preserve_verified_core","reasoning_responsiveness_separated"]
def a02():
 d=ROOT/"control-plane/browser/chatgpt-flight-recorder";m=load(d/"manifest.json");require(m.get("manifest_version")==3,"not_mv3");require(m.get("permissions")==["storage"],"flight_recorder_permissions_too_broad");require(m.get("host_permissions")==["https://chatgpt.com/*"],"flight_recorder_host_scope");js=(d/"content.js").read_text(encoding="utf-8")
 for forbidden in ["fetch(","XMLHttpRequest","WebSocket(","sendBeacon("]:require(forbidden not in js,f"network_exfiltration_surface:{forbidden}")
 require("long-animation-frame" in js and "streamGapMs" in js and "chat_switch_to_paint" in js,"ux_metrics_missing");run([sys.executable,"control-plane/tests/test_chat_ux_report.py"]);evidence("A02");return ["metadata_only_flight_recorder","loaf_longtask","stream_gap","chat_switch_to_paint","synthetic_report_tests"]
def a03():
 cloud=load(ROOT/"control-plane/ai-system/configs/ordinary-chat-routing.json")["cloudTask"];require(cloud["resumeMustExecuteZeroSteps"] is True and cloud["resumeMustProduceZeroNewDiff"] is True,"durable_resume_contract_regressed");run([sys.executable,"-m","unittest","control-plane/tests/test_ordinary_chat_task_runtime.py","-v"]);item=evidence("A03");require(item.get("replacementDecision") in {"preserve-and-harden","hybrid"},"verified_runtime_replaced_without_migration");return ["verified_task_runtime_regression","zero_reexecution_resume","replacement_requires_migration_e2e"]
def a04():
 src=(ROOT/"control-plane/scripts/ordinary_chat_coordination.py").read_text(encoding="utf-8")
 for token in ["task_ref","event_hash","parent_event_hash","HANDOFF","split_brain"]:require(token in src,f"coordination_token_missing:{token}")
 require("time.time" not in src and "expires" not in src,"ownership_must_not_use_time_expiry");run([sys.executable,"control-plane/tests/test_ordinary_chat_coordination.py"]);evidence("A04");return ["append_only_hash_chain","explicit_handoff","split_brain_veto","stale_writer_veto"]
def a05():
 caps=load(ROOT/"control-plane/ai-system/configs/ordinary-chat-capabilities.json");cap={x["id"]:x for x in caps["capabilities"]}["remote-desktop-commander"];require(cap["status"]=="device_dependent","local_backend_must_remain_device_dependent");run([sys.executable,"control-plane/tests/test_ordinary_chat_bridge.py"]);item=evidence("A05");require(item.get("liveDeviceRequired") is True and item.get("currentLiveDeviceState")=="BLOCKED","offline_device_faked_ready");return ["bridge_fail_closed","device_dependent_truth","live_device_blocker_explicit"]
def a06():
 ordinary=(ROOT/"control-plane/scripts/bootstrap_ordinary_chat_stack.sh").read_text(encoding="utf-8");browser=(ROOT/"control-plane/scripts/bootstrap_browser_use.sh").read_text(encoding="utf-8");require("@playwright/cli@0.1.18" in ordinary,"playwright_cli_not_pinned");require("@playwright/mcp@0.0.79" in ordinary,"playwright_mcp_not_pinned");require("browser-use==0.13.8" in browser,"browser_use_not_pinned");run(["bash","-n","control-plane/scripts/bootstrap_ordinary_chat_stack.sh"]);run(["bash","-n","control-plane/scripts/bootstrap_browser_use.sh"]);item=evidence("A06");require(item.get("liveBrowserRequired") is True and item.get("currentLiveBrowserState")=="BLOCKED","live_browser_truth_hidden");return ["pinned_browser_inputs","bootstrap_syntax","live_browser_blocker_explicit"]
def a07():
 c=load(MCP_COMPAT);require(c["targetSpec"]=="2026-07-28","mcp_spec_not_current_target");require(c["nativeTasksEnablement"]=="compatibility_gated","native_tasks_overclaimed");require(len(c["knownSdkIssues"])>=2,"sdk_extension_risks_missing");pkg=load(ROOT/"control-plane/ai-system/mcp/package.json");require(pkg["dependencies"]["@modelcontextprotocol/server"]=="2.0.0","verified_mcp_line_drifted");run(["npm","ci","--no-audit","--no-fund"],ROOT/"control-plane/ai-system/mcp");run(["npm","run","check"],ROOT/"control-plane/ai-system/mcp");evidence("A07");return ["mcp_2026_07_28","tasks_compatibility_gate","real_mcp_build_and_client_tests"]
def a08():
 c=load(UPSTREAM).get("candidates",[]);require(len(c)>=8,"upstream_matrix_too_small");require(all(x.get("source","").startswith("https://") for x in c),"unverifiable_upstream_source");require(all(x.get("decision") in {"adopt","adapt","defer","reject","evaluate"} for x in c),"invalid_upstream_decision");require({"protocol","browser","durable_runtime","cloud_agent","chat_ui"}.issubset({x["kind"] for x in c}),"upstream_domains_incomplete");evidence("A08");return ["june_aug_2026_matrix","protocol_browser_runtime_cloud_chat_ui","adopt_adapt_defer_decisions"]
def a09():
 c=load(OBS);require(c["contentCapture"]=="metadata_only","observability_content_scope");require({"task_ref","run_id","chat_actor_id","branch","head_sha","trace_id"}.issubset(set(c["requiredCorrelationFields"])),"correlation_fields_missing");rules=c["evidenceRules"];require(rules["noPromptOrResponseText"] is True and rules["receiptHashesRequiredForMutation"] is True,"evidence_privacy_or_integrity_missing");evidence("A09");return ["cross_surface_trace_correlation","metadata_only","receipt_hashes","ux_runtime_correlation"]
def a10():
 run([sys.executable,"control-plane/tests/test_ordinary_chat_release_gate.py"]);parsed=json.loads(run([sys.executable,"control-plane/scripts/ordinary_chat_release_gate.py",str(CLOSURE.relative_to(ROOT)),"--expect-blocked"]));require(parsed["result"]=="BLOCKED" and parsed["complete"] is False,"closure_must_fail_closed_while_live_e2e_missing");item=evidence("A10");require(item.get("requiredChecksEnforced") is False and item.get("liveE2EComplete") is False,"closure_truth_mismatch");return ["release_gate_fail_closed","required_checks_gap_explicit","live_e2e_gap_explicit"]
LANES={"A01":a01,"A02":a02,"A03":a03,"A04":a04,"A05":a05,"A06":a06,"A07":a07,"A08":a08,"A09":a09,"A10":a10}
def infer_lane(branch):
 m=LANE_RE.match(branch)
 if not m:raise Failure(f"cannot_infer_lane:{branch}")
 return m.group(1).upper()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--lane",choices=sorted(LANES));ap.add_argument("--branch",default=os.environ.get("GITHUB_REF_NAME",""));ap.add_argument("--all",action="store_true");ap.add_argument("--output");args=ap.parse_args();result={"schemaVersion":1,"baselineSha":BASELINE,"result":"FAIL","lanes":{}}
 try:
  baseline_ancestor();targets=sorted(LANES) if args.all else [args.lane or infer_lane(args.branch)]
  for lane in targets:result["lanes"][lane]={"result":"PASS","checks":LANES[lane]()}
  result["result"]="PASS"
 except Exception as exc:result["error"]=f"{type(exc).__name__}:{exc}"
 text=json.dumps(result,indent=2,sort_keys=True)+"\n";print(text,end="")
 if args.output:
  path=pathlib.Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding="utf-8")
 return 0 if result["result"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())
