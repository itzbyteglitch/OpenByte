from dataclasses import dataclass
from typing import Literal

Protocol = Literal["responses", "chat-completions"]

@dataclass(frozen=True)
class ModelDefinition:
    provider: str
    id: str
    name: str
    protocol: Protocol
    env_key: str
    base_url: str

MODEL_CATALOG = [
    ModelDefinition("openai", "gpt-5.6", "OpenAI GPT-5.6", "responses", "OPENAI_API_KEY", "https://api.openai.com/v1"),
    ModelDefinition("opencode-zen", "gpt-5.6-luna", "OpenCode Zen · GPT-5.6 Luna", "responses", "OPENCODE_ZEN_API_KEY", "https://opencode.ai/zen/v1"),
    ModelDefinition("opencode-zen", "gpt-5.6-sol", "OpenCode Zen · GPT-5.6 Sol", "responses", "OPENCODE_ZEN_API_KEY", "https://opencode.ai/zen/v1"),
    ModelDefinition("opencode-zen", "gpt-5.6-terra", "OpenCode Zen · GPT-5.6 Terra", "responses", "OPENCODE_ZEN_API_KEY", "https://opencode.ai/zen/v1"),
    ModelDefinition("opencode-zen", "deepseek-v4-pro", "OpenCode Zen · DeepSeek V4 Pro", "chat-completions", "OPENCODE_ZEN_API_KEY", "https://opencode.ai/zen/v1"),
    ModelDefinition("opencode-zen", "kimi-k2.7-code", "OpenCode Zen · Kimi K2.7 Code", "chat-completions", "OPENCODE_ZEN_API_KEY", "https://opencode.ai/zen/v1"),
    ModelDefinition("nvidia-nim", "nvidia/nemotron-3-nano-30b-a3b", "NVIDIA NIM · Nemotron 3 Nano", "chat-completions", "NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1"),
    ModelDefinition("nvidia-nim", "nvidia/nemotron-3-super-120b-a12b", "NVIDIA NIM · Nemotron 3 Super", "chat-completions", "NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1"),
    ModelDefinition("nvidia-nim", "nvidia/llama-3.3-nemotron-super-49b-v1", "NVIDIA NIM · Nemotron Super 49B", "chat-completions", "NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1"),
    ModelDefinition("openrouter", "openai/gpt-5.6-luna", "OpenRouter · GPT-5.6 Luna", "chat-completions", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1"),
    ModelDefinition("openrouter", "anthropic/claude-sonnet-4.6", "OpenRouter · Claude Sonnet 4.6", "chat-completions", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1"),
    ModelDefinition("openrouter", "google/gemini-3.1-pro-preview", "OpenRouter · Gemini 3.1 Pro", "chat-completions", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1"),
    ModelDefinition("openrouter", "deepseek/deepseek-v4", "OpenRouter · DeepSeek V4", "chat-completions", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1"),
]

def find_model(provider: str, model: str):
    return next((m for m in MODEL_CATALOG if m.provider == provider and m.id == model), None)

def provider_models(provider: str | None = None):
    return [m for m in MODEL_CATALOG if provider is None or m.provider == provider]
