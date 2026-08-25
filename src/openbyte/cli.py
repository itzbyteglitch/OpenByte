import argparse
import os
import sys
from .catalog import MODEL_CATALOG, find_model, provider_models
from .agent import Agent
from . import __version__

PROVIDERS = ("openai", "opencode-zen", "nvidia-nim", "openrouter")

def pick_model():
    print("\nOpenByte Model Picker\n")
    choices = []
    number = 1
    for provider in PROVIDERS:
        models = provider_models(provider)
        if not models:
            continue
        print(f"  {provider}")
        for model in models:
            print(f"    {number}. {model.name}  ({model.id})")
            choices.append(model)
            number += 1
    answer = input("\nSelect a model number: ").strip()
    try:
        selected = choices[int(answer) - 1]
    except (ValueError, IndexError):
        raise RuntimeError("Invalid model selection.")
    print(f"Selected: {selected.provider}/{selected.id}")
    print(f"Set {selected.env_key} to authenticate this provider.")

def main():
    parser = argparse.ArgumentParser(prog="openbyte", description="Open-source AI coding agent")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="run the coding agent")
    run.add_argument("prompt", nargs="?", default="")
    run.add_argument("-p", "--provider", default="openai")
    run.add_argument("-m", "--model", default="gpt-5.6")

    model = sub.add_parser("model", help="open the native model picker")
    model.add_argument("-p", "--provider")
    model.add_argument("-m", "--model")

    for name, help_text in [
        ("init", "initialize OpenByte configuration"),
        ("skills", "list and manage Skills"),
        ("agents", "list and manage subagents"),
        ("mcp", "manage MCP servers"),
        ("config", "view and edit OpenByte configuration"),
        ("doctor", "check OpenByte installation and environment"),
    ]:
        sub.add_parser(name, help=help_text)

    args = parser.parse_args()
    try:
        if args.command == "run":
            if not args.prompt.strip():
                raise RuntimeError('Provide a prompt, e.g. openbyte run "fix the tests"')
            definition = find_model(args.provider, args.model)
            if not definition:
                raise RuntimeError(f"Unknown model: {args.provider}/{args.model}. Run 'openbyte model'.")
            Agent(definition).run(args.prompt)
        elif args.command == "model":
            if args.model:
                definition = find_model(args.provider, args.model) if args.provider else next((m for m in MODEL_CATALOG if m.id == args.model), None)
                if not definition:
                    raise RuntimeError("Model not found. Run 'openbyte model'.")
                print(f"{definition.name}\nProvider: {definition.provider}\nModel: {definition.id}\nProtocol: {definition.protocol}\nAPI key: {definition.env_key}\nEndpoint: {definition.base_url}")
            elif args.provider:
                for m in provider_models(args.provider):
                    print(f"{m.id}\t{m.name}")
            else:
                pick_model()
        elif args.command == "init":
            print("OpenByte project initialization will be implemented here.")
        elif args.command == "skills":
            print("Skill registry ready for built-in, project, and user Skills.")
        elif args.command == "agents":
            print("Subagent manager will be implemented here.")
        elif args.command == "mcp":
            print("MCP manager will be implemented here.")
        elif args.command == "config":
            print("Configuration manager will be implemented here.")
        elif args.command == "doctor":
            print("OpenByte doctor will be implemented here.")
        else:
            parser.print_help()
    except Exception as exc:
        print(f"OpenByte: {exc}", file=sys.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
