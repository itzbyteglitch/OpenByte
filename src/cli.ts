#!/usr/bin/env node

import { Command } from "commander";
import { Agent } from "./core/agent.js";
import type { AgentConfig } from "./core/types.js";
import { OpenAIProvider } from "./providers/openai.js";

const program = new Command();

program
  .name("openbyte")
  .description("Open-source AI coding agent")
  .version("0.1.0");

program
  .command("run")
  .argument("[prompt]", "task for the agent")
  .option("-m, --model <model>", "model name", "gpt-5.6")
  .action(async (prompt = "", options) => {
    if (!prompt.trim()) throw new Error("Provide a prompt, e.g. openbyte run \"fix the tests\"");

    const config: AgentConfig = {
      provider: "openai",
      model: options.model,
      maxIterations: 20,
      permissionMode: "ask",
    };

    await new Agent(new OpenAIProvider(), config).run(prompt);
  });

program
  .command("init")
  .description("Initialize OpenByte configuration in the current project")
  .action(() => console.log("OpenByte project initialization will be implemented here."));

program
  .command("skills")
  .description("List and manage Skills")
  .action(() => console.log("Skill registry ready for built-in, project, and user Skills."));

program
  .command("agents")
  .description("List and manage subagents")
  .action(() => console.log("Subagent manager will be implemented here."));

program
  .command("mcp")
  .description("Manage MCP servers")
  .action(() => console.log("MCP manager will be implemented here."));

program
  .command("config")
  .description("View and edit OpenByte configuration")
  .action(() => console.log("Configuration manager will be implemented here."));

program
  .command("model")
  .description("Select the active model/provider")
  .action(() => console.log("Model gateway will be implemented here."));

program
  .command("doctor")
  .description("Check OpenByte installation and environment")
  .action(() => console.log("OpenByte doctor will be implemented here."));

program.parseAsync().catch((error) => {
  console.error(`OpenByte: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
});
