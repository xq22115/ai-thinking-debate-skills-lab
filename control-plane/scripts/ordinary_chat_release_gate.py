#!/usr/bin/env python3
"""Fail-closed v6 release closure gate."""
from __future__ import annotations
import argparse, json, pathlib, re
from typing import Any

SHA_RE=re.compile(r"^[0-9a-f]{40}$")
EXPECTED=[f"A{i:02d}" for i in range(1,11)]

def evaluate(data: dict[str,Any]) -> dict[str,Any]:
    reasons=[]
    integration_sha=str(data.get("integration_sha") or "")
    if not SHA_RE.fullmatch(integration_sha): reasons.append("invalid_integration_sha")
    lanes=data.get("lanes")
    if not isinstance(lanes,dict) or sorted(lanes) != EXPECTED:
        reasons.append("lane_set_mismatch")
    else:
        for lane in EXPECTED:
            item=lanes[lane]
            if not isinstance(item,dict) or item.get("result")!="PASS": reasons.append(f"lane_not_pass:{lane}")
            if isinstance(item,dict) and item.get("integration_sha") != integration_sha: reasons.append(f"lane_sha_mismatch:{lane}")
    requirements={
      "required_checks_enforced": data.get("required_checks_enforced") is True,
      "ordinary_chat_live_e2e": data.get("ordinary_chat_live_e2e") is True,
      "local_device_live_e2e": data.get("local_device_live_e2e") is True,
      "browser_live_e2e": data.get("browser_live_e2e") is True,
      "ux_flight_recorder_live_evidence": data.get("ux_flight_recorder_live_evidence") is True,
      "no_unresolved_blockers": data.get("unresolved_blockers")==[],
    }
    for key,ok in requirements.items():
        if not ok: reasons.append(key)
    return {"schemaVersion":1,"result":"PASS" if not reasons else "BLOCKED","complete":not reasons,"integration_sha":integration_sha or None,"reasons":reasons,"requirements":requirements}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("state"); ap.add_argument("--expect-blocked",action="store_true"); args=ap.parse_args()
    data=json.loads(pathlib.Path(args.state).read_text(encoding="utf-8")); result=evaluate(data); print(json.dumps(result,indent=2,sort_keys=True))
    if args.expect_blocked: return 0 if result["result"]=="BLOCKED" else 3
    return 0 if result["result"]=="PASS" else 2

if __name__=="__main__": raise SystemExit(main())
