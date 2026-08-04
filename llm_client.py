import os
from huggingface_hub import InferenceClient
from prompts import SYSTEM_PROMPT


class TriageClient:
    def __init__(self, token: str | None = None, model: str | None = None):
        self.token = token or os.environ.get("HF_TOKEN")
        self.model = model or os.environ.get("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct")
        if not self.token:
            raise RuntimeError("HF_TOKEN is not set. Add it to your .env file.")
        self.client = InferenceClient(model=self.model, token=self.token)

    def assess(self, user_prompt: str) -> str:
        completion = self.client.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )
        return completion.choices[0].message.content
