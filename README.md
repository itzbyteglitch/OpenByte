# OpenByte

OpenByte is an open-source, Claude Code–inspired AI coding agent with a provider-neutral runtime and native OpenAI support.

## Goals

- Native OpenAI Responses API support
- Pluggable Anthropic and OpenAI-compatible providers
- Claude Code-style Skills with `SKILL.md`
- Filesystem, shell, Git, and MCP tools
- Permission-aware tool execution
- Sessions, context management, compaction, and streaming
- Subagents and task delegation
- Clean interactive CLI

## CLI

```bash
openbyte
openbyte init
openbyte run "build a login page"
openbyte skills
openbyte agents
openbyte mcp
openbyte config
openbyte model
openbyte doctor
```

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
  ├── Anthropic
  └── OpenAI-compatible endpoints
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

## Status

Early architecture / foundation phase. The repository is intentionally being built in layers so the provider interface, agent loop, tool contracts, Skills system, and CLI remain independently testable.

## License

To be decided before the first public release.
