# OpenByte

<div align="center">

**An open-source, Claude Code-inspired AI coding agent with native multi-provider support.**

[![GitHub Stars](https://img.shields.io/github/stars/itzbyteglitch/OpenByte?style=for-the-badge&logo=github)](https://github.com/itzbyteglitch/OpenByte/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/itzbyteglitch/OpenByte?style=for-the-badge&logo=github)](https://github.com/itzbyteglitch/OpenByte/network/members)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-powered-6E56CF?style=for-the-badge&logo=uv&logoColor=white)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/github/license/itzbyteglitch/OpenByte?style=for-the-badge)](https://github.com/itzbyteglitch/OpenByte)

</div>

## Install

### Recommended — one-line installer

**Linux / macOS / WSL:**

```bash
curl -fsSL https://raw.githubusercontent.com/itzbyteglitch/OpenByte/main/scripts/install.sh | sh
```

The installer sets up OpenByte using `uv` and makes the `openbyte` command available in your user environment without requiring a system-wide Python installation.

> **Security note:** Piping a remote script directly to a shell executes code from the downloaded file. If you prefer to inspect it first, download the script and review it before running it.

### Install directly with uv

```bash
uv tool install openbyte
```

Then:

```bash
openbyte
```

### Windows

Install `uv`, then:

```powershell
uv tool install openbyte
```

## Uninstall

OpenByte also provides a matching uninstall script:

```bash
curl -fsSL https://raw.githubusercontent.com/itzbyteglitch/OpenByte/main/scripts/uninstall.sh | sh
```

Or uninstall through `uv` directly:

```bash
uv tool uninstall openbyte
```

## Quick start

```bash
openbyte
```

Inside a project:

```bash
cd my-project
openbyte
```

Or give OpenByte a task directly:

```bash
openbyte run "build a login page"
```

## CLI

```text
openbyte
├── init                         Initialize OpenByte in a project
├── run <prompt>                 Run an agent task
├── model                        Open the interactive model picker
├── skills                       Manage and inspect Skills
├── agents                       Manage subagents
├── mcp                          Manage MCP servers
├── config                       Configure OpenByte
└── doctor                       Diagnose installation and configuration
```

Examples:

```bash
openbyte init
openbyte run "fix the authentication bug"
openbyte model
openbyte model --provider openrouter
openbyte model --model openai/gpt-5.6
openbyte skills
openbyte agents
openbyte mcp
openbyte config
openbyte doctor
```

## Native model providers

OpenByte is provider-neutral at the agent-runtime level and supports these providers in the native model picker:

| Provider | API | Environment variable |
|---|---|---|
| **OpenAI** | Native Responses API | `OPENAI_API_KEY` |
| **OpenCode Zen** | Zen API / OpenAI-compatible API | `OPENCODE_ZEN_API_KEY` |
| **NVIDIA NIM** | OpenAI-compatible API | `NVIDIA_API_KEY` |
| **OpenRouter** | OpenAI-compatible API | `OPENROUTER_API_KEY` |

API keys are loaded from the environment and are never committed to the repository.

Select interactively:

```bash
openbyte model
```

Or specify a provider/model directly:

```bash
openbyte run -p openrouter -m openai/gpt-5.6 "refactor this component"
```

## Skills

OpenByte uses a Claude Code-style Skills architecture based around `SKILL.md`.

```text
.agent/
└── skills/
    ├── frontend-design/
    │   └── SKILL.md
    ├── github/
    │   └── SKILL.md
    └── custom-skill/
        └── SKILL.md
```

Skills can provide instructions, scripts, references, and reusable workflows. OpenByte can load built-in, project, and user Skills as the agent determines they are relevant.

## Architecture

```text
                         OpenByte CLI
                              │
                              ▼
                       Agent Runtime
              ┌───────────────┼────────────────┐
              │               │                │
         Agent Loop      Context Manager    Sessions
              │               │                │
              └───────────────┼────────────────┘
                              ▼
                        Model Gateway
                              │
          ┌───────────────────┼──────────────────┐
          │                   │                  │
       OpenAI            OpenCode Zen       Compatible
   Responses API          Zen API              APIs
                                                │
                                     ┌──────────┼──────────┐
                                     │          │          │
                                  NVIDIA    OpenRouter   Future
                                    NIM                   providers
                                                │
                                                ▼
                                          Tool Registry
                                     ┌──────────┼──────────┐
                                     │          │          │
                                  Filesystem  Shell       Git
                                                │
                                                ▼
                                               MCP
                                                │
                                                ▼
                                          Skills Registry
                                     ┌──────────┼──────────┐
                                     │          │          │
                                  Built-in   Project      User
```

## Development

Clone the repository:

```bash
git clone https://github.com/itzbyteglitch/OpenByte.git
cd OpenByte
```

Install dependencies with `uv`:

```bash
uv sync
```

Run the development CLI:

```bash
uv run openbyte
```

Run tests:

```bash
uv run pytest
```

## Configuration

Create environment variables for the providers you want to use:

```bash
export OPENAI_API_KEY="..."
export OPENCODE_ZEN_API_KEY="..."
export NVIDIA_API_KEY="..."
export OPENROUTER_API_KEY="..."
```

Never put real API keys in source code, commits, issues, screenshots, or public logs.

## Roadmap

- [x] Python + uv project foundation
- [x] Native model picker
- [x] OpenAI provider
- [x] OpenCode Zen provider
- [x] NVIDIA NIM provider
- [x] OpenRouter provider
- [ ] Full agent/tool execution loop
- [ ] Filesystem tools
- [ ] Shell execution with permissions
- [ ] Git tools
- [ ] Skills loader and execution
- [ ] MCP client
- [ ] Context compaction
- [ ] Sessions and resume
- [ ] Subagents / task delegation
- [ ] Cross-platform release automation
- [ ] PyPI release

## Contributing

Issues and pull requests are welcome. Please keep provider integrations, Skills, tools, and the core agent runtime modular so OpenByte can remain provider-neutral.

## License

To be decided before the first public release.
