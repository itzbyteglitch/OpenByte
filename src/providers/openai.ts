import OpenAI from "openai";
import type { ModelEvent, ModelRequest, ProviderId } from "../core/types.js";
import type { ModelProvider } from "./provider.js";

export class OpenAIProvider implements ModelProvider {
  readonly id: ProviderId;
  private readonly client: OpenAI;

  constructor(options: { id?: ProviderId; apiKey?: string; baseURL?: string } = {}) {
    this.id = options.id ?? "openai";
    this.client = new OpenAI({
      apiKey: options.apiKey ?? process.env.OPENAI_API_KEY,
      baseURL: options.baseURL,
    });
  }

  async *stream(request: ModelRequest): AsyncIterable<ModelEvent> {
    const response = await this.client.responses.create({
      model: request.model,
      instructions: request.system,
      input: request.input as never,
      stream: true,
    });

    for await (const event of response) {
      if (event.type === "response.output_text.delta") yield { type: "text-delta", text: event.delta };
      if (event.type === "response.completed") yield { type: "done" };
    }
  }
}
