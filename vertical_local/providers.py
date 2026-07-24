import os
import requests
from typing import Optional

# OpenAI adapter (thread-safe simple call)
try:
    import openai
except Exception:
    openai = None


def openai_generate(prompt: str, model: str = "gpt-4o-mini", api_key: Optional[str] = None, **kwargs) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OpenAI API key not provided")
    if openai is None:
        raise RuntimeError("openai package not installed")
    openai.api_key = key
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"user","content":prompt}],
        **kwargs,
    )
    # simple extraction
    return resp.choices[0].message.content


# HuggingFace Inference API adapter
HF_API_URL = "https://api-inference.huggingface.co/models/"

def hf_generate(prompt: str, model: str, api_key: Optional[str] = None, **kwargs) -> str:
    key = api_key or os.getenv("HF_API_KEY")
    if not key:
        raise ValueError("HuggingFace API key not provided")
    headers = {"Authorization": f"Bearer {key}"}
    url = HF_API_URL + model
    payload = {"inputs": prompt}
    res = requests.post(url, headers=headers, json=payload, timeout=120)
    res.raise_for_status()
    data = res.json()
    # HF inference may return list or dict depending on model
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        return data[0].get("generated_text") or str(data[0])
    if isinstance(data, dict):
        # common shape {"generated_text": "..."}
        return data.get("generated_text") or str(data)
    return str(data)


PROVIDERS = {
    "openai": openai_generate,
    "hf": hf_generate,
}


def generate(provider: str, prompt: str, model: str, api_key: Optional[str] = None, **kwargs) -> str:
    fn = PROVIDERS.get(provider)
    if not fn:
        raise ValueError(f"Unknown provider: {provider}")
    return fn(prompt=prompt, model=model, api_key=api_key, **kwargs)
