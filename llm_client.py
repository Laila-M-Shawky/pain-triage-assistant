import os
from huggingface_hub import InferenceClient
from prompts import SYSTEM_PROMPT


def _secret(name: str, default: str | None = None) -> str | None:
    """Look in os.environ first (local .env), then st.secrets (Streamlit Cloud)."""
    value = os.environ.get(name)
    if value:
        return value
    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return default


class TriageClient:
    def __init__(self, token: str | None = None, model: str | None = None):
        self.token = token or _secret("HF_TOKEN")
        self.model = model or _secret("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct")
        if not self.token:
            raise RuntimeError("HF_TOKEN is not set. Add it to your .env file or Streamlit secrets.")
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
