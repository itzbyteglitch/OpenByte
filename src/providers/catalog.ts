import type { ProviderId } from "../core/types.js";

export interface ModelDefinition {
  provider: ProviderId;
  id: string;
  name: string;
  protocol: "responses" | "chat-completions";
  envKey: string;
  baseURL: string;
}

export const MODEL_CATALOG: ModelDefinition[] = [
  { provider: "openai", id: "gpt-5.6", name: "OpenAI GPT-5.6", protocol: "responses", envKey: "OPENAI_API_KEY", baseURL: "https://api.openai.com/v1" },
  { provider: "opencode-zen", id: "gpt-5.6-luna", name: "OpenCode Zen · GPT-5.6 Luna", protocol: "responses", envKey: "OPENCODE_ZEN_API_KEY", baseURL: "https://opencode.ai/zen/v1" },
  { provider: "opencode-zen", id: "gpt-5.6-sol", name: "OpenCode Zen · GPT-5.6 Sol", protocol: "responses", envKey: "OPENCODE_ZEN_API_KEY", baseURL: "https://opencode.ai/zen/v1" },
  { provider: "opencode-zen", id: "gpt-5.6-terra", name: "OpenCode Zen · GPT-5.6 Terra", protocol: "responses", envKey: "OPENCODE_ZEN_API_KEY", baseURL: "https://opencode.ai/zen/v1" },
  { provider: "opencode-zen", id: "deepseek-v4-pro", name: "OpenCode Zen · DeepSeek V4 Pro", protocol: "chat-completions", envKey: "OPENCODE_ZEN_API_KEY", baseURL: "https://opencode.ai/zen/v1" },
  { provider: "opencode-zen", id: "kimi-k2.7-code", name: "OpenCode Zen · Kimi K2.7 Code", protocol: "chat-completions", envKey: "OPENCODE_ZEN_API_KEY", baseURL: "https://opencode.ai/zen/v1" },
  { provider: "nvidia-nim", id: "nvidia/llama-3.3-nemotron-super-49b-v1", name: "NVIDIA NIM · Nemotron Super", protocol: "chat-completions", envKey: "NVIDIA_API_KEY", baseURL: "https://integrate.api.nvidia.com/v1" },
  { provider: "nvidia-nim", id: "moonshotai/kimi-k2.5", name: "NVIDIA NIM · Kimi K2.5", protocol: "chat-completions", envKey: "NVIDIA_API_KEY", baseURL: "https://integrate.api.nvidia.com/v1" },
  { provider: "openrouter", id: "openai/gpt-5.6-luna", name: "OpenRouter · GPT-5.6 Luna", protocol: "chat-completions", envKey: "OPENROUTER_API_KEY", baseURL: "https://openrouter.ai/api/v1" },
  { provider: "openrouter", id: "anthropic/claude-sonnet-4.6", name: "OpenRouter · Claude Sonnet", protocol: "chat-completions", envKey: "OPENROUTER_API_KEY", baseURL: "https://openrouter.ai/api/v1" },
  { provider: "openrouter", id: "google/gemini-3.1-pro-preview", name: "OpenRouter · Gemini Pro", protocol: "chat-completions", envKey: "OPENROUTER_API_KEY", baseURL: "https://openrouter.ai/api/v1" },
  { provider: "openrouter", id: "deepseek/deepseek-v4", name: "OpenRouter · DeepSeek V4", protocol: "chat-completions", envKey: "OPENROUTER_API_KEY", baseURL: "https://openrouter.ai/api/v1" },
];

export function findModel(provider: ProviderId, model: string): ModelDefinition | undefined {
  return MODEL_CATALOG.find((entry) => entry.provider === provider && entry.id === model);
}

export function providerModels(provider?: ProviderId): ModelDefinition[] {
  return MODEL_CATALOG.filter((entry) => !provider || entry.provider === provider);
}
