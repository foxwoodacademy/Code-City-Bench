Vertical Local Wrapper

A minimal, model-agnostic FastAPI wrapper to run LLM calls locally or behind an API key. Supports OpenAI and Huggingface Inference API out of the box. Use environment variables or pass api_key per-request.

Quickstart (local):
1. cd vertical_local
2. python3 -m venv .venv && source .venv/bin/activate
3. pip install -r requirements.txt
4. cp .env.example .env and set keys or provide keys per-request
5. ./run.sh

Cloud hosting options (free tiers / small projects):
- Railway or Render (backend): small free credits — deploy the FastAPI app
- Vercel (frontend): host any UI or static assets
- Replit: easy one-click run for testing

Design notes:
- API is model-agnostic: send provider param ("openai" or "hf") and model name
- For production, add auth, rate-limits, and CORS rules
