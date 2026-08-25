"""Minimal MCP configuration discovery; protocol execution is isolated for future expansion."""
from __future__ import annotations
import json
from pathlib import Path

FILES=[Path(".mcp.json"),Path(".openbyte/mcp.json"),Path.home()/".openbyte"/"mcp.json"]

def load() -> dict:
    for p in FILES:
        if p.exists():
            try: return json.loads(p.read_text())
            except json.JSONDecodeError: return {}
    return {}

def servers() -> dict: return load().get("mcpServers", {})
