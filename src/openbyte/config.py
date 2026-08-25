"""Persistent OpenByte configuration and project discovery."""
from __future__ import annotations
import json
import os
from pathlib import Path

APP_DIR = Path(os.getenv("OPENBYTE_HOME", Path.home() / ".openbyte"))
CONFIG_FILE = APP_DIR / "config.json"
PROJECT_FILE = Path(".openbyte.json")
DEFAULTS = {"provider":"openai","model":"gpt-5.6","max_iterations":50,"approval_mode":"ask","max_file_bytes":1_000_000,"context_files":["AGENTS.md","CLAUDE.md",".openbyte/AGENTS.md"]}

def _read(path: Path) -> dict:
    try: return json.loads(path.read_text()) if path.exists() else {}
    except (OSError, json.JSONDecodeError): return {}

def load() -> dict:
    data = dict(DEFAULTS); data.update(_read(CONFIG_FILE)); data.update(_read(PROJECT_FILE)); return data

def save(data: dict) -> Path:
    APP_DIR.mkdir(parents=True, exist_ok=True); CONFIG_FILE.write_text(json.dumps(data, indent=2) + "\n"); return CONFIG_FILE

def init_project() -> Path:
    if not PROJECT_FILE.exists(): PROJECT_FILE.write_text(json.dumps(DEFAULTS, indent=2) + "\n")
    Path(".openbyte").mkdir(exist_ok=True)
    return PROJECT_FILE
