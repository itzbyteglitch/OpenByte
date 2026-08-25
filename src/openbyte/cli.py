import argparse, os, sys
from .catalog import MODEL_CATALOG, find_model, provider_models
from .agent import Agent
from . import __version__, session
from .config import load, save, init_project
from .skills import list_skills
from .mcp import servers

PROVIDERS=("openai","opencode-zen","nvidia-nim","openrouter")

def pick_model():
    print("\nOpenByte Model Picker\n"); choices=[]; n=1
    for provider in PROVIDERS:
        models=provider_models(provider)
        if not models: continue
        print(f"  {provider}")
        for model in models:
            print(f"    {n}. {model.name} ({model.id})"); choices.append(model); n+=1
    if not choices: raise RuntimeError("No models configured.")
    answer=input("\nSelect a model number: ").strip()
    try: selected=choices[int(answer)-1]
    except (ValueError,IndexError): raise RuntimeError("Invalid model selection.")
    cfg=load(); cfg.update(provider=selected.provider,model=selected.id); save(cfg)
    print(f"Selected and saved: {selected.provider}/{selected.id}")

def main():
    parser=argparse.ArgumentParser(prog="openbyte",description="Open-source autonomous AI coding agent")
    parser.add_argument("--version",action="version",version=__version__); sub=parser.add_subparsers(dest="command")
    run=sub.add_parser("run",help="run the coding agent"); run.add_argument("prompt",nargs="?",default=""); run.add_argument("-p","--provider"); run.add_argument("-m","--model"); run.add_argument("--auto-approve",action="store_true"); run.add_argument("--session")
    model=sub.add_parser("model",help="open the native model picker"); model.add_argument("-p","--provider"); model.add_argument("-m","--model")
    sub.add_parser("init",help="initialize OpenByte in this project")
    sub.add_parser("skills",help="list discovered Skills")
    sub.add_parser("agents",help="show agent/subagent status")
    sub.add_parser("mcp",help="show configured MCP servers")
    sub.add_parser("config",help="show or update configuration")
    sub.add_parser("doctor",help="diagnose installation and environment")
    sub.add_parser("sessions",help="list resumable sessions")
    args=parser.parse_args()
    try:
        if args.command=="run":
            cfg=load(); provider=args.provider or cfg["provider"]; model=args.model or cfg["model"]; d=find_model(provider,model)
            if not d: raise RuntimeError(f"Unknown model: {provider}/{model}. Run 'openbyte model'.")
            Agent(d,approval_mode="auto" if args.auto_approve else cfg["approval_mode"],session_id=args.session).run(args.prompt or input("OpenByte> "))
        elif args.command=="model":
            if args.model:
                d=find_model(args.provider,args.model) if args.provider else next((m for m in MODEL_CATALOG if m.id==args.model),None)
                if not d: raise RuntimeError("Model not found.")
                print(f"{d.name}\nProvider: {d.provider}\nModel: {d.id}\nProtocol: {d.protocol}\nAPI key: {d.env_key}\nEndpoint: {d.base_url}")
            elif args.provider:
                for m in provider_models(args.provider): print(f"{m.id}\t{m.name}")
            else: pick_model()
        elif args.command=="init": print(f"Initialized {init_project()}")
        elif args.command=="skills":
            skills=list_skills(); print("\n".join(skills) if skills else "No Skills found. Add .openbyte/skills/<name>/SKILL.md")
        elif args.command=="agents": print("Agent runtime: active; subagent delegation is planned for the next runtime milestone.")
        elif args.command=="mcp":
            s=servers(); print("\n".join(f"{k}: {v}" for k,v in s.items()) if s else "No MCP servers configured.")
        elif args.command=="config": print(__import__('json').dumps(load(),indent=2))
        elif args.command=="sessions": print("\n".join(session.list_sessions()) or "No sessions.")
        elif args.command=="doctor":
            cfg=load(); print(f"OpenByte {__version__}\nPython: {sys.version.split()[0]}\nProject: {os.getcwd()}\nProvider: {cfg['provider']}\nModel: {cfg['model']}")
            print(f"Auth: {'configured' if os.getenv(next(m.env_key for m in MODEL_CATALOG if m.provider==cfg['provider']),None) else 'missing'}")
        else: parser.print_help()
    except KeyboardInterrupt: print("\nCancelled.",file=sys.stderr); raise SystemExit(130)
    except Exception as exc: print(f"OpenByte: {exc}",file=sys.stderr); raise SystemExit(1)

if __name__=="__main__": main()
