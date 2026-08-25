import os
from openai import OpenAI
from .catalog import ModelDefinition

class Agent:
    def __init__(self, model: ModelDefinition, max_iterations: int = 20):
        key = os.getenv(model.env_key)
        if not key:
            raise RuntimeError(f"{model.env_key} is not set. Add it to your environment before running OpenByte.")
        headers = None
        if model.provider == "openrouter":
            headers = {"HTTP-Referer": "https://github.com/itzbyteglitch/OpenByte", "X-Title": "OpenByte"}
        self.model = model
        self.client = OpenAI(api_key=key, base_url=model.base_url, default_headers=headers)
        self.max_iterations = max_iterations

    def run(self, prompt: str) -> None:
        if self.model.protocol == "responses":
            self._run_responses(prompt)
        else:
            self._run_chat(prompt)

    def _run_responses(self, prompt: str) -> None:
        with self.client.responses.stream(model=self.model.id, input=prompt) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="", flush=True)
            stream.until_done()
        print()

    def _run_chat(self, prompt: str) -> None:
        stream = self.client.chat.completions.create(
            model=self.model.id,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        for chunk in stream:
            text = chunk.choices[0].delta.content if chunk.choices else None
            if text:
                print(text, end="", flush=True)
        print()
