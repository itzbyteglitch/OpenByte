import type { AgentConfig, ModelRequest, ToolDefinition } from "./types.js";
import type { ModelProvider } from "../providers/provider.js";

export class Agent {
  constructor(
    private readonly provider: ModelProvider,
    private readonly config: AgentConfig,
    private readonly tools: ToolDefinition[] = [],
  ) {}

  async run(input: string): Promise<void> {
    let currentInput: unknown = input;

    for (let iteration = 0; iteration < this.config.maxIterations; iteration++) {
      const request: ModelRequest = {
        model: this.config.model,
        input: currentInput,
        tools: this.tools,
      };

      let completed = false;
      for await (const event of this.provider.stream(request)) {
        if (event.type === "text-delta") process.stdout.write(event.text ?? "");
        if (event.type === "tool-call") {
          // Tool execution is intentionally separated into the tool runner.
          // This keeps the agent loop provider-neutral.
          completed = false;
        }
        if (event.type === "done") completed = true;
      }

      process.stdout.write("\n");
      if (completed) return;
    }

    throw new Error("OpenByte reached its maximum agent iterations.");
  }
}
