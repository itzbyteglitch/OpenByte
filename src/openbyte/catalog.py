from dataclasses import dataclass
from typing import Literal
import json
import os
from urllib.request import Request, urlopen

Protocol = Literal["responses", "chat-completions"]

@dataclass(frozen=True)
class ModelDefinition:
    provider: str
    id: str
    name: str
    protocol: Protocol
    env_key: str
    base_url: str

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_ENV_KEY = "OPENROUTER_API_KEY"
OPENCODE_ZEN_BASE_URL = "https://opencode.ai/zen/v1"
OPENCODE_ZEN_ENV_KEY = "OPENCODE_ZEN_API_KEY"

MODEL_CATALOG = [
    ModelDefinition("openai", "gpt-5.6", "OpenAI GPT-5.6", "chat-completions", "OPENAI_API_KEY", "https://api.openai.com/v1"),
    ModelDefinition("opencode-zen", "gpt-5.6-luna", "OpenCode Zen · GPT-5.6 Luna", "responses", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "gpt-5.6-sol", "OpenCode Zen · GPT-5.6 Sol", "responses", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "gpt-5.6-terra", "OpenCode Zen · GPT-5.6 Terra", "responses", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "deepseek-v4-pro", "OpenCode Zen · DeepSeek V4 Pro", "chat-completions", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "kimi-k2.7-code", "OpenCode Zen · Kimi K2.7 Code", "chat-completions", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    # Current OpenCode Zen free models.
    ModelDefinition("opencode-zen", "big-pickle", "OpenCode Zen · Big Pickle · FREE", "chat-completions", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "x-preview-f-free", "OpenCode Zen · Ox Alpha Free · FREE", "chat-completions", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "mimo-v2.5-free", "OpenCode Zen · MiMo-V2.5 Free · FREE", "chat-completions", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "hy3-free", "OpenCode Zen · Hy3 Free · FREE", "chat-completions", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "nemotron-3-ultra-free", "OpenCode Zen · Nemotron 3 Ultra Free · FREE", "chat-completions", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "nemotron-3.5-lightning-free", "OpenCode Zen · Nemotron 3.5 Lightning Free · FREE", "chat-completions", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("opencode-zen", "muse-spark-1.2-contributor-free", "OpenCode Zen · Muse Spark 1.2 Contributor Free · FREE", "responses", OPENCODE_ZEN_ENV_KEY, OPENCODE_ZEN_BASE_URL),
    ModelDefinition("nvidia-nim", "nvidia/nemotron-3-nano-30b-a3b", "NVIDIA NIM · Nemotron 3 Nano", "chat-completions", "NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1"),
    ModelDefinition("nvidia-nim", "nvidia/nemotron-3-super-120b-a12b", "NVIDIA NIM · Nemotron 3 Super", "chat-completions", "NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1"),
    ModelDefinition("nvidia-nim", "nvidia/llama-3.3-nemotron-super-49b-v1", "NVIDIA NIM · Nemotron Super 49B", "chat-completions", "NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1"),
]

_openrouter_cache: list[ModelDefinition] | None = None

def fetch_openrouter_models(force: bool = False) -> list[ModelDefinition]:
    """Fetch the complete live OpenRouter model catalog when an API key is configured."""
    global _openrouter_cache
    if _openrouter_cache is not None and not force:
        return _openrouter_cache
    if not os.getenv(OPENROUTER_ENV_KEY):
        return []
    request = Request(f"{OPENROUTER_BASE_URL}/models", headers={"Authorization": f"Bearer {os.environ[OPENROUTER_ENV_KEY]}", "User-Agent": "OpenByte"})
    try:
        with urlopen(request, timeout=10) as response:
            payload = json.load(response)
    except Exception:
        return _openrouter_cache or []
    models = []
    for item in payload.get("data", []):
        model_id = item.get("id")
        if not model_id:
            continue
        name = item.get("name") or model_id
        models.append(ModelDefinition("openrouter", model_id, f"OpenRouter · {name}", "chat-completions", OPENROUTER_ENV_KEY, OPENROUTER_BASE_URL))
    models.sort(key=lambda model: model.id.lower())
    _openrouter_cache = models
    return models

def provider_models(provider: str | None = None):
    models = list(MODEL_CATALOG)
    if provider in (None, "openrouter"):
        models.extend(fetch_openrouter_models())
    if provider is None:
        return models
    return [m for m in models if m.provider == provider]

def find_model(provider: str, model: str):
    return next((m for m in provider_models(provider) if m.id == model), None)

def refresh_openrouter_models():
    """Refresh and return the live OpenRouter catalog."""
    return fetch_openrouter_models(force=True)
