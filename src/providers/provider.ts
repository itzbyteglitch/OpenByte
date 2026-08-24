import type { ModelEvent, ModelRequest, ProviderId } from "../core/types.js";

export interface ModelProvider {
  readonly id: ProviderId;
  stream(request: ModelRequest): AsyncIterable<ModelEvent>;
}

export interface ProviderFactory {
  create(): ModelProvider;
}
