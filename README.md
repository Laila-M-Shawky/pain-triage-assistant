# 🩺 Pain Triage Assistant

A Streamlit app where a patient describes pain/symptoms in Arabic or English and
gets a **preliminary, non-diagnostic** triage: possible general causes, urgency
level, suggested specialist, and red-flag warnings — powered by an LLM on the
Hugging Face Inference API.

**This is not a medical device and does not diagnose.** It is a triage helper
that always tells the user to consult a licensed physician, and it independently
flags emergency-sounding descriptions (`red_flags.py`) regardless of what the
LLM says.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then paste your HF token into .env
```

Get a free token at https://huggingface.co/settings/tokens (read-only is enough).

## Run

```bash
streamlit run app.py
```

## How it works

- `app.py` — Streamlit UI: free-text description + optional age/sex/duration/severity.
- `red_flags.py` — regex-based emergency screening (Arabic + English), independent
  safety net that fires before the LLM is even called.
- `prompts.py` — the system prompt that constrains the LLM to hedged, structured,
  non-diagnostic output (possible causes / urgency / specialist / red flags / disclaimer).
- `llm_client.py` — thin wrapper around `huggingface_hub.InferenceClient` for chat
  completion. Default model: `Qwen/Qwen2.5-7B-Instruct` (ungated, handles Arabic +
  English). Swap `HF_MODEL` in `.env` for any chat model available on HF Inference
  Providers.

## Known limitations

- LLM output can be wrong or inconsistent — it is a starting point for the patient
  to bring to a real doctor, not a substitute for one.
- The red-flag list in `red_flags.py` is a coarse keyword net, not exhaustive.
- No patient data is stored; each request is stateless.
