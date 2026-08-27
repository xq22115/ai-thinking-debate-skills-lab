#!/usr/bin/env python3
"""Append-only ordinary-chat coordination log above existing immutable claim/snapshot controls."""
from __future__ import annotations
import argparse, contextlib, hashlib, json, os, pathlib, re, tempfile
from typing import Any, Iterator

TOKEN_RE=re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,239}$")
EVENT_TYPES={"REGISTER","CLAIM","CHECKPOINT","HANDOFF","RELEASE"}
class CoordinationError(RuntimeError): pass

def _canonical(value:dict[str,Any])->bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def _without_hash(event:dict[str,Any])->dict[str,Any]: return {k:v for k,v in event.items() if k!="event_hash"}
def event_hash(event:dict[str,Any])->str: return hashlib.sha256(_canonical(_without_hash(event))).hexdigest()
def _valid_token(name:str,value:Any)->str:
    text=str(value or "")
    if not TOKEN_RE.fullmatch(text) or ".." in text: raise CoordinationError(f"invalid_{name}")
    return text

def make_event(*,task_ref:str,actor_id:str,branch:str,base_sha:str,head_sha:str,event_type:str,seq:int,parent_event_hash:str|None,run_id:str,trace_id:str,handoff_to:str|None=None)->dict[str,Any]:
    if event_type not in EVENT_TYPES: raise CoordinationError("invalid_event_type")
    if seq<1: raise CoordinationError("invalid_seq")
    event={"schemaVersion":1,"task_ref":_valid_token("task_ref",task_ref),"actor_id":_valid_token("actor_id",actor_id),"branch":_valid_token("branch",branch),"base_sha":_valid_token("base_sha",base_sha),"head_sha":_valid_token("head_sha",head_sha),"run_id":_valid_token("run_id",run_id),"trace_id":_valid_token("trace_id",trace_id),"event_type":event_type,"seq":seq,"parent_event_hash":parent_event_hash}
    if handoff_to is not None: event["handoff_to"]=_valid_token("handoff_to",handoff_to)
    event["event_hash"]=event_hash(event); return event

def replay(events:list[dict[str,Any]])->dict[str,Any]:
    task_ref=None; owner=None; last_hash=None; last_head=None; seen=set()
    for index,event in enumerate(events,start=1):
        if event.get("schemaVersion")!=1: raise CoordinationError(f"schema_mismatch:{index}")
        if event.get("seq")!=index: raise CoordinationError(f"sequence_gap:{index}")
        if event.get("parent_event_hash")!=last_hash: raise CoordinationError(f"parent_hash_mismatch:{index}")
        claimed=str(event.get("event_hash") or "")
        if claimed!=event_hash(event): raise CoordinationError(f"event_hash_mismatch:{index}")
        if claimed in seen: raise CoordinationError(f"duplicate_event_hash:{index}")
        seen.add(claimed)
        this_task=_valid_token("task_ref",event.get("task_ref")); actor=_valid_token("actor_id",event.get("actor_id"))
        _valid_token("branch",event.get("branch")); _valid_token("base_sha",event.get("base_sha")); last_head=_valid_token("head_sha",event.get("head_sha")); _valid_token("run_id",event.get("run_id")); _valid_token("trace_id",event.get("trace_id"))
        kind=event.get("event_type")
        if kind not in EVENT_TYPES: raise CoordinationError(f"invalid_event_type:{index}")
        if task_ref is None: task_ref=this_task
        elif this_task!=task_ref: raise CoordinationError(f"task_ref_changed:{index}")
        if kind=="REGISTER": pass
        elif kind=="CLAIM":
            if owner is not None: raise CoordinationError(f"split_brain_claim:{index}")
            owner=actor
        elif kind=="CHECKPOINT":
            if owner!=actor: raise CoordinationError(f"checkpoint_by_non_owner:{index}")
        elif kind=="HANDOFF":
            if owner!=actor: raise CoordinationError(f"handoff_by_non_owner:{index}")
            target=_valid_token("handoff_to",event.get("handoff_to"))
            if target==actor: raise CoordinationError(f"self_handoff:{index}")
            owner=target
        elif kind=="RELEASE":
            if owner!=actor: raise CoordinationError(f"release_by_non_owner:{index}")
            owner=None
        last_hash=claimed
    return {"schemaVersion":1,"task_ref":task_ref,"event_count":len(events),"current_owner":owner,"last_event_hash":last_hash,"last_head_sha":last_head,"result":"PASS"}

def load_events(path:pathlib.Path)->list[dict[str,Any]]:
    if not path.exists(): return []
    events=[]
    for line_no,line in enumerate(path.read_text(encoding="utf-8").splitlines(),start=1):
        if not line.strip(): continue
        try: value=json.loads(line)
        except json.JSONDecodeError as exc: raise CoordinationError(f"invalid_json_line:{line_no}") from exc
        if not isinstance(value,dict): raise CoordinationError(f"event_not_object:{line_no}")
        events.append(value)
    return events

@contextlib.contextmanager
def _exclusive_lock(lock_path:pathlib.Path)->Iterator[None]:
    lock_path.parent.mkdir(parents=True,exist_ok=True); handle=lock_path.open("a+",encoding="utf-8")
    try:
        try: import fcntl
        except ImportError as exc: raise CoordinationError("fcntl_required_for_coordination_lock") from exc
        fcntl.flock(handle.fileno(),fcntl.LOCK_EX); yield
    finally:
        try:
            import fcntl; fcntl.flock(handle.fileno(),fcntl.LOCK_UN)
        except Exception: pass
        handle.close()

def append_event(path:pathlib.Path,event:dict[str,Any])->dict[str,Any]:
    path=path.expanduser().resolve()
    with _exclusive_lock(path.with_suffix(path.suffix+".lock")):
        events=load_events(path); current=replay(events) if events else {"event_count":0,"last_event_hash":None,"task_ref":None}
        if event.get("seq")!=int(current["event_count"])+1: raise CoordinationError("append_seq_mismatch")
        if event.get("parent_event_hash")!=current.get("last_event_hash"): raise CoordinationError("append_parent_mismatch")
        if current.get("task_ref") and event.get("task_ref")!=current["task_ref"]: raise CoordinationError("append_task_ref_mismatch")
        new_state=replay(events+[event]); path.parent.mkdir(parents=True,exist_ok=True); existing=path.read_text(encoding="utf-8") if path.exists() else ""; body=existing+json.dumps(event,sort_keys=True,ensure_ascii=False)+"\n"
        fd,tmp_name=tempfile.mkstemp(prefix=path.name+".",dir=path.parent)
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as fh: fh.write(body); fh.flush(); os.fsync(fh.fileno())
            os.replace(tmp_name,path)
        finally:
            if os.path.exists(tmp_name): os.unlink(tmp_name)
        return new_state

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--log",required=True); parser.add_argument("--inspect",action="store_true"); parser.add_argument("--event-json"); args=parser.parse_args(); path=pathlib.Path(args.log)
    try:
        if args.inspect: result=replay(load_events(path))
        else:
            if not args.event_json: raise CoordinationError("event_json_required")
            event=json.loads(args.event_json)
            if not isinstance(event,dict): raise CoordinationError("event_not_object")
            result=append_event(path,event)
        print(json.dumps(result,indent=2,sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"result":"VETO","error":f"{type(exc).__name__}:{exc}"},sort_keys=True)); return 2
if __name__=="__main__": raise SystemExit(main())
