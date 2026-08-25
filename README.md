# OpenByte

OpenByte is an open-source, Claude Code-inspired AI coding agent with a provider-neutral runtime, native OpenAI support, Claude Code-style Skills, and a native multi-provider model picker.

## Installation with uv

OpenByte uses **uv** as its package and installation system.

```bash
uv tool install openbyte
```

Then run:

```bash
openbyte
```

For development:

```bash
git clone https://github.com/itzbyteglitch/OpenByte.git
cd OpenByte
uv sync
uv run openbyte
```

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

## Native model providers

- **OpenAI** — native Responses API
- **OpenCode Zen** — Zen Responses and OpenAI-compatible Chat Completions
- **NVIDIA NIM** — NVIDIA hosted OpenAI-compatible endpoint
- **OpenRouter** — OpenAI-compatible unified model gateway

Provider API keys are read from environment variables and are never stored in source code.

| Provider | Environment variable | Endpoint |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | `https://api.openai.com/v1` |
| OpenCode Zen | `OPENCODE_ZEN_API_KEY` | `https://opencode.ai/zen/v1` |
| NVIDIA NIM | `NVIDIA_API_KEY` | `https://integrate.api.nvidia.com/v1` |
| OpenRouter | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` |

## Architecture

```text
uv
 ↓
OpenByte CLI (Python)
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
 └── OpenAI-compatible adapter
      ├── OpenCode Zen Chat Completions
      ├── NVIDIA NIM
      └── OpenRouter
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
- Native OpenCode Zen, NVIDIA NIM, and OpenRouter support
- Claude Code-style Skills with `SKILL.md`
- Filesystem, shell, Git, and MCP tools
- Permission-aware tool execution
- Sessions, context management, compaction, and streaming
- Subagents and task delegation
- Cross-platform installation through uv

## Status

Early architecture / foundation phase. The Python/uv runtime and native provider picker are now in place. Agent tools, Skills execution, MCP, permissions, sessions, and subagents are being built in layers.

## License

To be decided before the first public release.
