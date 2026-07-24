import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from providers import generate

load_dotenv()

app = FastAPI(title="Vertical Local Wrapper")

# Serve web/ as static at /static
static_dir = os.path.join(os.path.dirname(__file__), "web")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Presets / personas router (optional)
try:
    from presets_router import router as presets_router
    app.include_router(presets_router, prefix="/presets")
except Exception:
    # presets_router not available yet
    pass

# Personas router
try:
    from personas_router import router as personas_router
    app.include_router(personas_router, prefix="/personas")
except Exception:
    pass

# Debate router
try:
    from debate_router import router as debate_router
    app.include_router(debate_router, prefix="/debate")
except Exception:
    pass

class GenRequest(BaseModel):
    provider: str  # 'openai' or 'hf'
    model: str
    prompt: str
    api_key: str | None = None
    max_tokens: int | None = None


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/boardroom")
def boardroom():
    # Serve the boardroom HTML directly from the web/ folder
    path = os.path.join(os.path.dirname(__file__), 'web', 'boardroom.html')
    if os.path.isfile(path):
        return FileResponse(path, media_type='text/html')
    return {"error": "boardroom UI not found"}


@app.post("/generate")
def gen(req: GenRequest):
    try:
        text = generate(provider=req.provider, prompt=req.prompt, model=req.model, api_key=req.api_key, max_tokens=req.max_tokens)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
