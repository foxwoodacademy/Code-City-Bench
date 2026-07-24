Deploy notes

- Railway: connect repo, set environment variables (OPENAI_API_KEY, HF_API_KEY), and deploy. Use a Procfile or the run command: uvicorn app:app --host 0.0.0.0 --port $PORT
- Render: create a Web Service, use the above run command, set env vars.
- Replit: upload files, set secrets in the Secrets panel and press Run.

Caveats:
- Free hosting often sleeps or has low resource limits. For testing, Replit or Railway free tier is convenient.
- For production, add authentication, rate-limiting, logging, and model usage tracking.
