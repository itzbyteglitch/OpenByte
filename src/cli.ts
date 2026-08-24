#!/usr/bin/env node

import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { Command } from "commander";
import { Agent } from "./core/agent.js";
import type { AgentConfig, ProviderId } from "./core/types.js";
import { MODEL_CATALOG, findModel, providerModels } from "./providers/catalog.js";
import { OpenAIProvider } from "./providers/openai.js";
import { OpenAICompatibleProvider } from "./providers/openai-compatible.js";

const program = new Command();

function createProvider(provider: ProviderId, model: string) {
  const definition = findModel(provider, model);
  if (!definition) throw new Error(`Unknown model: ${provider}/${model}. Run 'openbyte model'.`);

  const apiKey = process.env[definition.envKey];
  if (!apiKey) throw new Error(`${definition.envKey} is not set. Add it to your environment before running OpenByte.`);

  if (definition.protocol === "responses") {
    return new OpenAIProvider({ id: provider, apiKey, baseURL: definition.baseURL });
  }

  return new OpenAICompatibleProvider({
    id: provider,
    apiKey,
    baseURL: definition.baseURL,
    defaultHeaders: provider === "openrouter"
      ? { "HTTP-Referer": "https://github.com/itzbyteglitch/OpenByte", "X-Title": "OpenByte" }
      : undefined,
  });
}

async function pickModel(): Promise<void> {
  console.log("\nOpenByte Model Picker\n");
  const groups = ["openai", "opencode-zen", "nvidia-nim", "openrouter"] as const;
  let index = 1;
  const choices: typeof MODEL_CATALOG = [];

  for (const provider of groups) {
    const models = providerModels(provider);
    if (!models.length) continue;
    console.log(`  ${provider}`);
    for (const model of models) {
      console.log(`    ${index}. ${model.name}  (${model.id})`);
      choices.push(model);
      index++;
    }
  }

  const rl = createInterface({ input, output });
  try {
    const answer = await rl.question("\nSelect a model number: ");
    const selected = choices[Number(answer) - 1];
    if (!selected) throw new Error("Invalid model selection.");
    console.log(`Selected: ${selected.provider}/${selected.id}`);
    console.log(`Set ${selected.envKey} to authenticate this provider.`);
  } finally {
    rl.close();
  }
}

program
  .name("openbyte")
  .description("Open-source AI coding agent")
  .version("0.1.0");

program
  .command("run")
  .argument("[prompt]", "task for the agent")
  .option("-p, --provider <provider>", "provider", "openai")
  .option("-m, --model <model>", "model name", "gpt-5.6")
  .action(async (prompt = "", options) => {
    if (!prompt.trim()) throw new Error('Provide a prompt, e.g. openbyte run "fix the tests"');

    const config: AgentConfig = {
      provider: options.provider as ProviderId,
      model: options.model,
      maxIterations: 20,
      permissionMode: "ask",
    };

    await new Agent(createProvider(config.provider, config.model), config).run(prompt);
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
  .description("Open the native model picker")
  .option("-p, --provider <provider>", "show models for one provider")
  .option("-m, --model <model>", "show details for one model")
  .action(async (options) => {
    if (options.model) {
      const provider = options.provider as ProviderId | undefined;
      const model = provider ? findModel(provider, options.model) : MODEL_CATALOG.find((entry) => entry.id === options.model);
      if (!model) throw new Error("Model not found. Run 'openbyte model' to see available models.");
      console.log(`${model.name}\nProvider: ${model.provider}\nModel: ${model.id}\nProtocol: ${model.protocol}\nAPI key: ${model.envKey}\nEndpoint: ${model.baseURL}`);
      return;
    }

    if (options.provider) {
      for (const model of providerModels(options.provider as ProviderId)) console.log(`${model.id}\t${model.name}`);
      return;
    }

    await pickModel();
  });

program
  .command("doctor")
  .description("Check OpenByte installation and environment")
  .action(() => console.log("OpenByte doctor will be implemented here."));

program.parseAsync().catch((error) => {
  console.error(`OpenByte: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
});
