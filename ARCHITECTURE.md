# OpenByte Architecture

OpenByte is split into six layers. Each layer has a narrow responsibility so model providers can change without rewriting the agent runtime.

## 1. CLI

`src/cli.ts`

Owns commands, flags, terminal rendering, and process lifecycle.

Planned command surface:

- `openbyte`
- `openbyte init`
- `openbyte run <prompt>`
- `openbyte model`
- `openbyte skills`
- `openbyte agents`
- `openbyte mcp`
- `openbyte config`
- `openbyte doctor`

## 2. Agent Runtime

`src/core/`

The runtime is provider-neutral.

```text
User prompt
    ↓
Context Manager
    ↓
Agent Loop
    ├── plan
    ├── request model
    ├── receive text/tool calls
    ├── permission check
    ├── execute tools
    └── continue until done
```

Future modules:

- `context.ts` — conversation state, files, summaries
- `session.ts` — persisted sessions and resume
- `permissions.ts` — ask/allow/deny policies
- `compaction.ts` — context reduction
- `task.ts` — long-running task state

## 3. Model Gateway

`src/providers/`

All providers implement the same `ModelProvider` interface.

```text
                 ┌── OpenAI Responses API
Agent Runtime ───┼── Anthropic API
                 └── OpenAI-compatible HTTP API
```

OpenAI is implemented natively through the official SDK and Responses API. The gateway must preserve streaming, tool calls, reasoning events, structured output, and provider-specific capabilities without leaking provider details into the agent loop.

## 4. Tool System

Planned structure:

```text
src/tools/
├── registry.ts
├── filesystem.ts
├── shell.ts
├── search.ts
├── git.ts
└── permissions.ts
```

Every tool exposes a schema plus an execution function. The registry converts registered tools into the provider's tool format and routes tool calls back to the correct implementation.

Shell and filesystem operations must always pass through the permission layer.

## 5. Skills

`src/skills/`

OpenByte uses a `SKILL.md` convention.

Skill sources will be loaded in this order:

1. Built-in OpenByte Skills
2. Project Skills: `.openbyte/skills/*/SKILL.md`
3. User Skills: `~/.openbyte/skills/*/SKILL.md`
4. Optional compatible Skill locations

A Skill contains instructions and may contain supporting scripts/resources. Skills are loaded selectively rather than injecting every Skill into every prompt.

## 6. MCP and Subagents

Planned modules:

```text
src/mcp/
├── client.ts
├── config.ts
└── registry.ts

src/agents/
├── registry.ts
├── runner.ts
└── delegation.ts
```

MCP provides external tools. Subagents provide isolated specialist work. Both feed results back through the same permission and context infrastructure.

## Configuration

Project configuration will live under `.openbyte/`:

```text
.openbyte/
├── config.json
├── skills/
├── agents/
└── sessions/
```

Global configuration will live under `~/.openbyte/`.

Environment variables such as `OPENAI_API_KEY` are supported for provider credentials.

## Design principles

1. Provider-neutral core.
2. OpenAI-native implementation, not a compatibility shim.
3. Skills are filesystem artifacts, not hard-coded prompts.
4. Tools are permission-gated.
5. Streaming is first-class.
6. Sessions are resumable.
7. Every major subsystem is independently testable.
8. The CLI remains usable without a web UI.
