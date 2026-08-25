"""Portable SKILL.md discovery and relevance loading."""
from __future__ import annotations
from pathlib import Path

PACKAGE_ROOT=Path(__file__).resolve().parents[2]
BUILTIN_ROOT=Path(__file__).resolve().parent/"builtin_skills"
SKILL_ROOTS=[BUILTIN_ROOT,PACKAGE_ROOT/"skills",Path(".openbyte/skills"),Path(".agent/skills"),Path("skills"),Path.home()/".openbyte"/"skills"]

def discover()->list[Path]:
    found=[]; seen=set()
    for root in SKILL_ROOTS:
        if not root.exists(): continue
        for f in root.rglob("SKILL.md"):
            key=str(f.resolve())
            if key not in seen: found.append(f); seen.add(key)
    return sorted(found)

def load_relevant(prompt:str,limit:int=5)->str:
    words={w.lower() for w in prompt.split() if len(w)>3}; blocks=[]
    for path in discover():
        text=path.read_text(errors="ignore")
        score=sum(w in text.lower() or w in path.parent.name.lower() for w in words)
        if score: blocks.append((score,text))
    blocks.sort(reverse=True,key=lambda x:x[0])
    return "\n\n--- SKILL ---\n\n".join(t[:12000] for _,t in blocks[:limit])

def list_skills()->list[str]: return [str(p.parent) for p in discover()]
