import OpenAI from "openai";
import type { ModelEvent, ModelRequest, ProviderId } from "../core/types.js";
import type { ModelProvider } from "./provider.js";

export interface OpenAICompatibleOptions {
  id: ProviderId;
  apiKey: string | undefined;
  baseURL: string;
  defaultHeaders?: Record<string, string>;
}

/** Adapter for services exposing the OpenAI Chat Completions API. */
export class OpenAICompatibleProvider implements ModelProvider {
  readonly id: ProviderId;
  private readonly client: OpenAI;

  constructor(options: OpenAICompatibleOptions) {
    this.id = options.id;
    this.client = new OpenAI({
      apiKey: options.apiKey ?? "",
      baseURL: options.baseURL,
      defaultHeaders: options.defaultHeaders,
    });
  }

  async *stream(request: ModelRequest): AsyncIterable<ModelEvent> {
    const messages = [
      ...(request.system ? [{ role: "system" as const, content: request.system }] : []),
      { role: "user" as const, content: String(request.input) },
    ];

    const response = await this.client.chat.completions.create({
      model: request.model,
      messages,
      stream: true,
    });

    for await (const chunk of response) {
      const text = chunk.choices[0]?.delta?.content;
      if (text) yield { type: "text-delta", text };
    }

    yield { type: "done" };
  }
}
