#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, pathlib
from typing import Iterable
METRICS={"stream_gap_ms":("assistant_stream_delta","streamGapMs"),"chat_switch_to_paint_ms":("chat_switch_to_paint","durationMs"),"long_animation_frame_ms":("long_animation_frame","durationMs"),"long_task_ms":("long_task","durationMs")}
def percentile(values:list[float],q:float)->float|None:
    if not values:return None
    xs=sorted(values)
    if len(xs)==1:return xs[0]
    pos=(len(xs)-1)*q; lo=math.floor(pos); hi=math.ceil(pos)
    if lo==hi:return xs[lo]
    return xs[lo]*(hi-pos)+xs[hi]*(pos-lo)
def summarize(events:Iterable[dict])->dict:
    events=list(events); out={"schemaVersion":1,"contentCapture":"metadata_only","eventCount":len(events),"metrics":{}}
    for metric,(etype,field) in METRICS.items():
        values=[float(e[field]) for e in events if e.get("type")==etype and isinstance(e.get(field),(int,float))]
        out["metrics"][metric]={"count":len(values),"p50":percentile(values,.5),"p95":percentile(values,.95),"max":max(values) if values else None}
    gaps=out["metrics"]["stream_gap_ms"]; switches=out["metrics"]["chat_switch_to_paint_ms"]; loaf=out["metrics"]["long_animation_frame_ms"]
    out["diagnosticSignals"]={"stream_stall_suspected":bool(gaps["p95"] is not None and gaps["p95"]>=1000),"chat_switch_render_stall_suspected":bool(switches["p95"] is not None and switches["p95"]>=500),"main_thread_jank_suspected":bool(loaf["count"]>=3 and loaf["p95"] is not None and loaf["p95"]>=200)}
    return out
def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("input"); ap.add_argument("--output"); args=ap.parse_args(); data=json.loads(pathlib.Path(args.input).read_text(encoding="utf-8"))
    if data.get("contentCapture")!="metadata_only" or not isinstance(data.get("events"),list): raise SystemExit("invalid metadata-only flight-recorder export")
    result=summarize(data["events"]); text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:pathlib.Path(args.output).write_text(text,encoding="utf-8")
    print(text,end=""); return 0
if __name__=="__main__":raise SystemExit(main())
