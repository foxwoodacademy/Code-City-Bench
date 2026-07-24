UI notes

- Runs with: npm install && npm run dev (inside web/)
- Proxy: In development, the UI expects /generate on same host. Use a dev proxy or run the FastAPI server on port 8000 and the UI on 5173 with CORS or a proxy.
- For deployment: build the UI (npm run build) and serve static files or host separately (Vercel recommended).

UX choices:
- Minimal prompt-first flow for fast onboarding
- Provider and model visible to enable business users to switch providers
- Optional per-request API key for testing with paid keys without storing them
