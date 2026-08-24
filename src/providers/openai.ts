import OpenAI from "openai";
import type { ModelEvent, ModelRequest } from "../core/types.js";
import type { ModelProvider } from "./provider.js";

export class OpenAIProvider implements ModelProvider {
  readonly id = "openai" as const;
  private readonly client: OpenAI;

  constructor(client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })) {
    this.client = client;
  }

  async *stream(request: ModelRequest): AsyncIterable<ModelEvent> {
    const response = await this.client.responses.create({
      model: request.model,
      instructions: request.system,
      input: request.input as never,
      stream: true,
    });

    for await (const event of response) {
      if (event.type === "response.output_text.delta") {
        yield { type: "text-delta", text: event.delta };
      }
      if (event.type === "response.completed") {
        yield { type: "done" };
      }
    }
  }
}
