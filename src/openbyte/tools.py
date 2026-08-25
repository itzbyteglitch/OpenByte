"""Safe, provider-neutral coding tools exposed to the agent."""
from __future__ import annotations
import json, os, subprocess
from pathlib import Path
from typing import Callable

ROOT = Path.cwd().resolve()

def safe_path(raw: str) -> Path:
    p = (ROOT / raw).resolve()
    if p != ROOT and ROOT not in p.parents: raise ValueError("Path escapes the project root")
    return p

def read_file(path: str, max_bytes: int = 1_000_000) -> str:
    p=safe_path(path); data=p.read_bytes()
    if len(data)>max_bytes: raise ValueError("File exceeds configured size limit")
    return data.decode("utf-8", errors="replace")

def write_file(path: str, content: str) -> str:
    p=safe_path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content); return f"Wrote {path}"

def list_files(path: str = ".") -> str:
    p=safe_path(path); items=[]
    for x in sorted(p.iterdir(), key=lambda x:(x.is_file(), x.name.lower())):
        if x.name in {".git", ".venv", "__pycache__", "node_modules"}: continue
        items.append(("file" if x.is_file() else "dir")+" "+str(x.relative_to(ROOT)))
    return "\n".join(items[:500]) or "(empty)"

def search_text(query: str, path: str = ".") -> str:
    p=safe_path(path); out=[]
    for f in p.rglob("*"):
        if not f.is_file() or any(part in {".git",".venv","node_modules","__pycache__"} for part in f.parts): continue
        try: text=f.read_text(errors="ignore")
        except OSError: continue
        for i,line in enumerate(text.splitlines(),1):
            if query.lower() in line.lower(): out.append(f"{f.relative_to(ROOT)}:{i}: {line[:300]}")
            if len(out)>=200: return "\n".join(out)
    return "\n".join(out) or "No matches."

def run_shell(command: str, timeout: int = 120) -> str:
    result=subprocess.run(command, cwd=ROOT, shell=True, text=True, capture_output=True, timeout=min(timeout,300), env=os.environ.copy())
    text=(result.stdout+result.stderr).strip()
    if result.returncode: raise RuntimeError(f"Command exited {result.returncode}:\n{text}")
    return text or "(command completed successfully)"

def git_status() -> str: return run_shell("git status --short")

def tool_schemas() -> list[dict]:
    return [
      {"type":"function","function":{"name":"read_file","description":"Read a UTF-8 text file inside the project.","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}}},
      {"type":"function","function":{"name":"write_file","description":"Create or replace a UTF-8 file inside the project.","parameters":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}}},
      {"type":"function","function":{"name":"list_files","description":"List project files and directories.","parameters":{"type":"object","properties":{"path":{"type":"string"}}}}},
      {"type":"function","function":{"name":"search_text","description":"Search text recursively in project files.","parameters":{"type":"object","properties":{"query":{"type":"string"},"path":{"type":"string"}},"required":["query"]}}},
      {"type":"function","function":{"name":"run_shell","description":"Run a shell command in the project. Requires approval unless auto approval is enabled.","parameters":{"type":"object","properties":{"command":{"type":"string"},"timeout":{"type":"integer"}},"required":["command"]}}},
      {"type":"function","function":{"name":"git_status","description":"Show git working tree status.","parameters":{"type":"object","properties":{}}}},
    ]

FUNCTIONS: dict[str, Callable] = {"read_file":read_file,"write_file":write_file,"list_files":list_files,"search_text":search_text,"run_shell":run_shell,"git_status":git_status}

def execute(name: str, args: dict, approval_mode: str = "ask") -> str:
    if name not in FUNCTIONS: raise ValueError(f"Unknown tool: {name}")
    if name in {"write_file","run_shell"} and approval_mode == "ask":
        print(f"\nOpenByte wants to run {name} with {json.dumps(args)[:500]}\nAllow? [y/N] ", end="", flush=True)
        if input().strip().lower() not in {"y","yes"}: return "Tool denied by user."
    return str(FUNCTIONS[name](**args))
