# OpenByte

<div align="center">

**An open-source, Claude Code-inspired autonomous AI coding agent with native multi-provider support.**

[![GitHub Stars](https://img.shields.io/github/stars/itzbyteglitch/OpenByte?style=for-the-badge&logo=github)](https://github.com/itzbyteglitch/OpenByte/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/itzbyteglitch/OpenByte?style=for-the-badge&logo=github)](https://github.com/itzbyteglitch/OpenByte/network/members)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-powered-6E56CF?style=for-the-badge&logo=uv&logoColor=white)](https://docs.astral.sh/uv/)
[![CI](https://img.shields.io/github/actions/workflow/status/itzbyteglitch/OpenByte/ci.yml?style=for-the-badge&label=CI)](https://github.com/itzbyteglitch/OpenByte/actions)
[![License](https://img.shields.io/github/license/itzbyteglitch/OpenByte?style=for-the-badge)](https://github.com/itzbyteglitch/OpenByte)

</div>

OpenByte is designed around the workflow of modern coding agents: inspect the repository, load project instructions and relevant Skills, call tools, edit files, run commands with approval, keep a session, and iterate until the task is complete.

## Install

### Recommended — one-line installer

**Linux / macOS / WSL:**

```bash
curl -fsSL https://raw.githubusercontent.com/itzbyteglitch/OpenByte/main/scripts/install.sh | sh
```

The installer bootstraps `uv` when necessary and installs OpenByte as a user tool.

> **Security note:** Piping a remote script directly to a shell executes downloaded code. Download and inspect the script first if you prefer manual verification.

### Directly with uv

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

### From source

```bash
git clone https://github.com/itzbyteglitch/OpenByte.git
cd OpenByte
uv sync --extra dev
uv run openbyte
```

## Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/itzbyteglitch/OpenByte/main/scripts/uninstall.sh | sh
```

Or:

```bash
uv tool uninstall openbyte
```

## Quick start

Initialize a project:

```bash
cd my-project
openbyte init
```

Run an autonomous task:

```bash
openbyte run "inspect this project, fix the failing tests, and explain the changes"
```

Open the model picker:

```bash
openbyte model
```

## CLI

```text
openbyte
├── init                         Initialize project configuration
├── run <prompt>                 Run the autonomous coding agent
├── model                        Interactive native model picker
├── skills                       List discovered Skills
├── agents                       Agent/subagent status
├── mcp                          Inspect MCP configuration
├── config                       Show current configuration
├── sessions                     List resumable sessions
└── doctor                       Diagnose installation and authentication
```

Useful options:

```bash
openbyte run "fix the tests" --auto-approve
openbyte run "refactor the API" --provider openrouter --model anthropic/claude-sonnet-4.6
openbyte run "continue the previous task" --session <session-id>
openbyte model --provider nvidia-nim
openbyte skills
openbyte sessions
openbyte doctor
```

## Native model providers

OpenByte keeps the agent runtime provider-neutral and currently includes these providers in its native picker:

| Provider | Endpoint | Environment variable |
|---|---|---|
| **OpenAI** | OpenAI API | `OPENAI_API_KEY` |
| **OpenCode Zen** | Zen API | `OPENCODE_ZEN_API_KEY` |
| **NVIDIA NIM** | NVIDIA hosted NIM | `NVIDIA_API_KEY` |
| **OpenRouter** | OpenRouter API | `OPENROUTER_API_KEY` |

All providers use the OpenAI Python SDK's tool-capable interface, allowing the same agent/tool loop to work across native and OpenAI-compatible APIs.

API keys are read from the environment and are never stored in OpenByte configuration.

## Agent capabilities

### Autonomous tool loop

OpenByte can repeatedly reason, call a tool, inspect its result, and continue until the model decides the task is complete or a safety iteration limit is reached.

### Built-in coding tools

- Read files
- Write files
- List directories
- Recursive text search
- Shell commands
- Git status
- Project-root path protection
- File-size limits
- Interactive approval for writes and shell commands
- `--auto-approve` for trusted workflows

### Skills

OpenByte uses a portable `SKILL.md` format inspired by Claude Code's Skills model.

Skills can live in:

```text
.openbyte/skills/
.agent/skills/
skills/
~/.openbyte/skills/
```

Built-in Skills are bundled with OpenByte. The initial set includes:

- `code-review`
- `frontend-design`
- `testing`

A Skill can contain instructions, references, examples, and scripts. Relevant Skills are selected from the task prompt and injected into the agent context.

### Project instructions

OpenByte recognizes project-level instructions such as:

```text
AGENTS.md
CLAUDE.md
.openbyte/AGENTS.md
```

`openbyte init` creates `.openbyte.json` and the `.openbyte/` workspace directory.

### Sessions

Every task receives a lightweight JSONL session stored under `~/.openbyte/sessions/`. Sessions can be inspected and resumed with:

```bash
openbyte sessions
openbyte run "continue the task" --session <id>
```

### MCP configuration

OpenByte discovers MCP server configuration from:

```text
.mcp.json
.openbyte/mcp.json
~/.openbyte/mcp.json
```

The configuration layer is intentionally isolated so full MCP transport/tool bridging can evolve without coupling it to the agent runtime.

## Configuration

Global configuration lives at:

```text
~/.openbyte/config.json
```

Project overrides live at:

```text
.openbyte.json
```

Example:

```json
{
  "provider": "openrouter",
  "model": "anthropic/claude-sonnet-4.6",
  "max_iterations": 50,
  "approval_mode": "ask",
  "max_file_bytes": 1000000
}
```

Supported approval modes are designed around safety first: `ask` requires confirmation for file writes and shell commands; `auto` can be enabled explicitly for trusted environments.

## Architecture

```text
                              OpenByte CLI
                                   │
                                   ▼
                            Agent Runtime
                     ┌─────────────┼─────────────┐
                     │             │             │
                 Agent Loop    Context       Sessions
                     │          + Skills         │
                     └─────────────┼─────────────┘
                                   ▼
                             Model Gateway
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
          OpenAI              OpenCode Zen        OpenAI-compatible
                                                   │
                                             ┌─────┴─────┐
                                             │           │
                                          NVIDIA      OpenRouter
                                            NIM
                                   │
                                   ▼
                              Tool Registry
                    ┌────────────┼─────────────┐
                    │            │             │
                Filesystem     Shell          Git
                    │            │             │
                    └────────────┼─────────────┘
                                 ▼
                              MCP Layer
                                 │
                                 ▼
                         Future external tools
```

## Development

```bash
git clone https://github.com/itzbyteglitch/OpenByte.git
cd OpenByte
uv sync --extra dev
uv run openbyte
```

Tests and linting:

```bash
uv run pytest
uv run ruff check src tests
```

GitHub Actions runs the same checks on pushes and pull requests.

## Security model

OpenByte is intentionally conservative by default:

- API keys stay in environment variables.
- Tool paths are restricted to the current project root.
- File reads have a configurable size limit.
- File writes require approval by default.
- Shell commands require approval by default.
- Shell execution has a bounded timeout.
- The agent has a maximum iteration limit.
- Sessions contain model/tool text but should not be treated as a secret vault.

Never run OpenByte with auto-approval in an untrusted repository or with credentials you would not want a shell command to access.

## Roadmap

### Core

- [x] Python + uv distribution foundation
- [x] Native model picker
- [x] OpenAI, OpenCode Zen, NVIDIA NIM, and OpenRouter providers
- [x] Autonomous tool loop
- [x] Filesystem/search/shell/Git tools
- [x] Approval and project-root safety controls
- [x] Persistent configuration
- [x] JSONL sessions and resume
- [x] Portable Skills discovery
- [x] Built-in Skills
- [x] MCP configuration discovery
- [x] CI, tests, and linting

### Next runtime milestones

- [ ] Full MCP client transport and tool bridging
- [ ] True subagent delegation and parallel tasks
- [ ] Context compaction and token-aware history management
- [ ] Patch/diff editing tool with atomic writes
- [ ] Interactive approval UI with command previews
- [ ] Rich terminal UI and streaming status indicators
- [ ] Model discovery APIs and provider-specific capabilities
- [ ] Retry/backoff and rate-limit handling
- [ ] Structured telemetry with opt-in privacy controls
- [ ] Checkpoints and automatic rollback
- [ ] Git diff/review/test automation
- [ ] Plugin/Skill installer and versioning
- [ ] Cross-platform release binaries
- [ ] PyPI publishing

## Contributing

Issues and pull requests are welcome. Keep provider integrations, Skills, tools, safety controls, and the agent runtime modular.

## License

To be decided before the first public release.
