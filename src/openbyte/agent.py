"""OpenByte autonomous tool-using coding agent."""
from __future__ import annotations
import json, os
from openai import OpenAI
from .catalog import ModelDefinition
from .config import load
from .skills import load_relevant
from .tools import tool_schemas, execute
from . import session

SYSTEM = """You are OpenByte, an autonomous software-engineering agent. Work carefully inside the user's project. Inspect before editing, make minimal correct changes, run relevant tests when possible, and explain what changed. Never claim a tool action succeeded unless the tool returned success. Respect user approval and project instructions."""

class Agent:
    def __init__(self, model: ModelDefinition, max_iterations: int | None = None, approval_mode: str | None = None, session_id: str | None = None):
        key=os.getenv(model.env_key)
        if not key: raise RuntimeError(f"{model.env_key} is not set. Add it to your environment before running OpenByte.")
        headers={"HTTP-Referer":"https://github.com/itzbyteglitch/OpenByte","X-Title":"OpenByte"} if model.provider=="openrouter" else None
        self.model=model; self.client=OpenAI(api_key=key,base_url=model.base_url,default_headers=headers)
        cfg=load(); self.max_iterations=max_iterations or int(cfg["max_iterations"]); self.approval_mode=approval_mode or cfg["approval_mode"]
        self.session_id=session_id or session.create()

    def run(self,prompt: str)->None:
        skills=load_relevant(prompt)
        system=SYSTEM + ("\n\nRelevant Skills:\n"+skills if skills else "")
        messages=[{"role":"system","content":system},{"role":"user","content":prompt}]
        session.append(self.session_id,"user",prompt)
        for _ in range(self.max_iterations):
            response=self.client.chat.completions.create(model=self.model.id,messages=messages,tools=tool_schemas(),tool_choice="auto")
            msg=response.choices[0].message
            if msg.content: print(msg.content,end="\n",flush=True); session.append(self.session_id,"assistant",msg.content)
            if not msg.tool_calls: return
            messages.append(msg)
            for call in msg.tool_calls:
                try: args=json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError: args={}
                try: result=execute(call.function.name,args,self.approval_mode)
                except Exception as exc: result=f"ERROR: {exc}"
                messages.append({"role":"tool","tool_call_id":call.id,"content":result})
                session.append(self.session_id,"tool",f"{call.function.name}: {result[:4000]}")
        raise RuntimeError(f"Agent reached the {self.max_iterations}-iteration safety limit. Session: {self.session_id}")
