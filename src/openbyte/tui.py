from __future__ import annotations
import os, time
from pathlib import Path
from textual.app import App
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Static, Button, Label, Input, Markdown
from textual.screen import Screen
from . import __version__
from .catalog import MODEL_CATALOG
from .config import load
from .mcp import servers
from .session import list_sessions, ROOT as SESSION_ROOT
from .skills import list_skills

class SideBar(Static):
    def compose(self):
        yield Static("OPENBYTE", id="brand")
        for label, key in [("Dashboard","d"),("Chat","c"),("Models","m"),("Sessions","s"),("MCP Servers","p"),("Skills","k"),("Usage","u"),("Stats","t"),("Config","g"),("Doctor","o"),("Help","h")]:
            yield Button(f"{label}  [{key}]", id=f"nav-{key}", classes="nav")

class BaseScreen(Screen):
    def screen_title(self): return "OpenByte"
    def body(self): return []
    def compose(self):
        yield Header(show_clock=True)
        with Horizontal(id="shell"):
            yield SideBar()
            with Vertical(id="content"):
                yield Label(self.screen_title(), id="screen-title")
                yield VerticalScroll(*self.body(), id="screen-body")
        yield Footer()

class Dashboard(BaseScreen):
    def screen_title(self): return "Dashboard"
    def body(self):
        cfg=load(); ss=list_sessions(); ms=MODEL_CATALOG; mc=servers(); sk=list_skills()
        return [Static(f"Welcome to OpenByte v{__version__}\n\nYour autonomous coding workspace.", classes="hero"), Static(f"MODEL\n{cfg['provider']} / {cfg['model']}", classes="card"), Static(f"SESSIONS\n{len(ss)} resumable sessions", classes="card"), Static(f"MODELS\n{len(ms)} models across {len(set(m.provider for m in ms))} providers", classes="card"), Static(f"MCP\n{len(mc)} configured servers", classes="card"), Static(f"SKILLS\n{len(sk)} discovered Skills", classes="card"), Static("SHORTCUTS\n[d] Dashboard   [c] Chat   [m] Models   [s] Sessions   [p] MCP\n[k] Skills   [u] Usage   [t] Stats   [g] Config   [o] Doctor   [h] Help", classes="card")]

class ChatScreen(BaseScreen):
    def screen_title(self): return "Chat / Agent"
    def body(self): return [Static("Interactive agent workspace", classes="hero"), Markdown("**Ready.** Type a task below.\n\nThe TUI is the control surface; execution remains handled by OpenByte's agent runtime."), Input(placeholder="Ask OpenByte to build, debug, refactor, test...", id="prompt"), Button("Run task", id="run-task")]

class ModelsScreen(BaseScreen):
    def screen_title(self): return "Models"
    def body(self):
        rows=[f"{m.provider:<16} {m.id:<34} {m.name}" for m in MODEL_CATALOG]
        return [Static("PROVIDER / MODEL / NAME", classes="section"), Static("\n".join(rows) or "No models configured.", classes="mono"), Static("\nUse `openbyte model` for the interactive picker or `openbyte model --provider NAME` to filter.", classes="muted")]

class SessionsScreen(BaseScreen):
    def screen_title(self): return "Sessions"
    def body(self):
        ss=list_sessions(); rows=[]
        for sid in ss:
            p=SESSION_ROOT/f"{sid}.jsonl"; rows.append(f"{sid:<16} {p.stat().st_size:>8} bytes   {time.ctime(p.stat().st_mtime)}")
        return [Static("SESSION ID         SIZE       LAST UPDATED", classes="section"), Static("\n".join(rows) or "No resumable sessions yet.", classes="mono")]

class MCPscreen(BaseScreen):
    def screen_title(self): return "MCP Servers"
    def body(self):
        data=servers(); rows=[f"{k}: {v}" for k,v in data.items()]
        return [Static(f"{len(data)} configured MCP servers", classes="hero"), Static("\n".join(rows) or "No MCP servers configured.\n\nConfig locations: .mcp.json, .openbyte/mcp.json, ~/.openbyte/mcp.json", classes="mono")]

class SkillsScreen(BaseScreen):
    def screen_title(self): return "Skills"
    def body(self):
        sk=list_skills(); return [Static(f"{len(sk)} Skills discovered", classes="hero"), Static("\n".join(sk) or "No Skills found. Add .openbyte/skills/<name>/SKILL.md", classes="mono")]

class UsageScreen(BaseScreen):
    def screen_title(self): return "Usage"
    def body(self):
        files=list(SESSION_ROOT.glob("*.jsonl")) if SESSION_ROOT.exists() else []; total=sum(p.stat().st_size for p in files); messages=0
        for p in files:
            try: messages += sum(1 for line in p.read_text().splitlines() if line.strip())
            except OSError: pass
        return [Static("USAGE OVERVIEW", classes="section"), Static(f"Sessions      {len(files)}\nMessages      {messages}\nStored data   {total:,} bytes\n\nToken/cost telemetry will appear here when provider usage metadata is persisted by the runtime.", classes="card")]

class StatsScreen(BaseScreen):
    def screen_title(self): return "Stats"
    def body(self):
        cfg=load(); providers={m.provider for m in MODEL_CATALOG}; return [Static("RUNTIME STATISTICS", classes="section"), Static(f"OpenByte version   {__version__}\nPython             {os.sys.version.split()[0]}\nWorking directory  {Path.cwd()}\nProviders           {len(providers)}\nModels              {len(MODEL_CATALOG)}\nConfigured provider {cfg['provider']}\nConfigured model    {cfg['model']}\nMax iterations     {cfg['max_iterations']}", classes="card")]

class ConfigScreen(BaseScreen):
    def screen_title(self): return "Configuration"
    def body(self):
        cfg=load(); return [Static("EFFECTIVE CONFIGURATION", classes="section"), Static("\n".join(f"{k}: {v}" for k,v in cfg.items()), classes="mono")]

class DoctorScreen(BaseScreen):
    def screen_title(self): return "Doctor"
    def body(self):
        cfg=load(); env=next((m.env_key for m in MODEL_CATALOG if m.provider==cfg['provider']),None); auth=bool(os.getenv(env)) if env else False
        return [Static("SYSTEM HEALTH", classes="section"), Static(f"✓ Python {os.sys.version.split()[0]}\n✓ OpenByte {__version__}\n✓ Project directory accessible\n{'✓' if auth else '⚠'} API key for {cfg['provider']}: {'configured' if auth else 'missing'}\n✓ Configuration readable\n✓ Session store: {SESSION_ROOT}", classes="card")]

class HelpScreen(BaseScreen):
    def screen_title(self): return "Help"
    def body(self): return [Static("KEYBOARD SHORTCUTS", classes="section"), Static("d Dashboard\nc Chat\nm Models\ns Sessions\np MCP Servers\nk Skills\nu Usage\nt Stats\ng Config\no Doctor\nh Help\nq Quit", classes="mono"), Static("\nCLI remains available for automation: openbyte run, init, model, skills, agents, mcp, config, sessions, doctor.", classes="muted")]

SCREENS={"d":Dashboard,"c":ChatScreen,"m":ModelsScreen,"s":SessionsScreen,"p":MCPscreen,"k":SkillsScreen,"u":UsageScreen,"t":StatsScreen,"g":ConfigScreen,"o":DoctorScreen,"h":HelpScreen}

class OpenByteTUI(App):
    CSS="""
    Screen { background: #080b10; color: #e6edf3; }
    #shell { height: 1fr; }
    #sidebar { width: 25; padding: 1; border-right: solid #263241; }
    #brand { text-style: bold; color: #7dd3fc; padding: 1 0 2 1; }
    .nav { width: 100%; margin: 0 0 1 0; background: transparent; border: none; color: #aab6c5; content-align: left middle; }
    .nav:hover, .nav:focus { color: #fff; background: #182231; }
    #content { width: 1fr; padding: 1 2; }
    #screen-title { text-style: bold; color: #fff; padding: 0 0 1 0; }
    #screen-body { height: 1fr; }
    .hero { padding: 2; margin: 0 0 1 0; background: #101722; border: solid #263241; }
    .card { padding: 1; margin: 0 0 1 0; background: #0d131c; border: solid #263241; }
    .section { padding: 1; color: #7dd3fc; text-style: bold; }
    .mono { padding: 1; color: #d5dde7; }
    .muted { color: #8290a0; padding: 1; }
    Input { margin: 1 0; border: solid #334155; }
    #run-task { width: 20; }
    Footer { background: #0d131c; }
    """
    TITLE="OpenByte"
    BINDINGS=[("q","quit","Quit"),("d","dashboard","Dashboard"),("c","chat","Chat"),("m","models","Models"),("s","sessions","Sessions"),("p","mcp","MCP"),("k","skills","Skills"),("u","usage","Usage"),("t","stats","Stats"),("g","config","Config"),("o","doctor","Doctor"),("h","help","Help")]
    def on_mount(self): self.push_screen(Dashboard())
    def action_dashboard(self): self.push_screen(Dashboard())
    def action_chat(self): self.push_screen(ChatScreen())
    def action_models(self): self.push_screen(ModelsScreen())
    def action_sessions(self): self.push_screen(SessionsScreen())
    def action_mcp(self): self.push_screen(MCPscreen())
    def action_skills(self): self.push_screen(SkillsScreen())
    def action_usage(self): self.push_screen(UsageScreen())
    def action_stats(self): self.push_screen(StatsScreen())
    def action_config(self): self.push_screen(ConfigScreen())
    def action_doctor(self): self.push_screen(DoctorScreen())
    def action_help(self): self.push_screen(HelpScreen())
    def on_button_pressed(self,event):
        bid=event.button.id or ""; key=bid.removeprefix("nav-")
        if key in SCREENS: self.push_screen(SCREENS[key]())

def run_tui(): OpenByteTUI().run()
