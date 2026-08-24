# OpenByte

OpenByte is an open-source, Claude Code–inspired AI coding agent with a provider-neutral runtime, native OpenAI support, and a native multi-provider model picker.

## Native model providers

OpenByte currently supports:

- **OpenAI** — native OpenAI Responses API
- **OpenCode Zen** — Zen Responses and OpenAI-compatible Chat Completions models
- **NVIDIA NIM** — NVIDIA hosted NIM OpenAI-compatible endpoint
- **OpenRouter** — OpenAI-compatible unified model gateway

Provider API keys are read from environment variables; keys are never stored in the source code.

| Provider | Environment variable | Endpoint |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | `https://api.openai.com/v1` |
| OpenCode Zen | `OPENCODE_ZEN_API_KEY` | `https://opencode.ai/zen/v1` |
| NVIDIA NIM | `NVIDIA_API_KEY` | `https://integrate.api.nvidia.com/v1` |
| OpenRouter | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` |

## CLI

```bash
openbyte
openbyte init
openbyte run "build a login page"
openbyte run -p openrouter -m openai/gpt-5.6-luna "refactor this component"
openbyte skills
openbyte agents
openbyte mcp
openbyte config
openbyte model
openbyte model --provider openrouter
openbyte model --model openai/gpt-5.6-luna
openbyte doctor
```

Running `openbyte model` opens the interactive native model picker. The catalog is intentionally provider-aware so the agent can select the correct protocol and endpoint automatically.

## Architecture

```text
CLI
  ↓
Application / Commands
  ↓
Agent Runtime
  ├── Context Manager
  ├── Agent Loop
  ├── Planner / Task Manager
  ├── Permission Manager
  └── Session Store
       ↓
Model Gateway
  ├── OpenAI Responses API
  ├── OpenCode Zen Responses
  ├── OpenAI-compatible adapter
  │    ├── OpenCode Zen Chat Completions
  │    ├── NVIDIA NIM
  │    └── OpenRouter
  └── Future providers
       ↓
Tool Registry
  ├── filesystem
  ├── shell
  ├── git
  ├── search
  └── MCP
       ↓
Skills Registry
  ├── built-in skills
  ├── project skills
  └── user skills
```

## Goals

- Claude Code-style agent workflow
- Native OpenAI Responses API
- Provider-neutral model gateway
- Native OpenCode Zen, NVIDIA NIM, and OpenRouter support
- Claude Code-style Skills with `SKILL.md`
- Filesystem, shell, Git, and MCP tools
- Permission-aware tool execution
- Sessions, context management, compaction, and streaming
- Subagents and task delegation
- Clean interactive CLI

## Status

Early architecture / foundation phase. Provider selection and the first native model catalog are now in place. The repository is being built in layers so the provider interface, agent loop, tool contracts, Skills system, and CLI remain independently testable.

## License

To be decided before the first public release.
