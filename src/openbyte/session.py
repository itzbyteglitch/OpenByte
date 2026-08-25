"""Lightweight resumable JSONL session storage."""
from __future__ import annotations
import json, time, uuid
from pathlib import Path

ROOT=Path.home()/".openbyte"/"sessions"

def create() -> str:
    ROOT.mkdir(parents=True, exist_ok=True); sid=uuid.uuid4().hex[:12]; (ROOT/f"{sid}.jsonl").touch(); return sid

def append(sid: str, role: str, content: str) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    with (ROOT/f"{sid}.jsonl").open("a") as f: f.write(json.dumps({"ts":time.time(),"role":role,"content":content})+"\n")

def load(sid: str) -> list[dict]:
    p=ROOT/f"{sid}.jsonl"
    if not p.exists(): raise FileNotFoundError(sid)
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]

def list_sessions() -> list[str]: return sorted((p.stem for p in ROOT.glob("*.jsonl")), reverse=True) if ROOT.exists() else []
