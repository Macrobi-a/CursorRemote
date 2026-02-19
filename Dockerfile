# Recruitment workflow: run 24/7 on Railway or AWS
FROM python:3.11-slim

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App and pipeline output (generated agents + graph)
COPY . .
# Don't copy .venv or heavy caches
RUN rm -rf .venv __pycache__ output/__pycache__ output/agents/__pycache__ 2>/dev/null; true

# Load .env at runtime (or use platform env vars)
ENV PYTHONUNBUFFERED=1
# Railway sets PORT dynamically; default to 8000 if not set
ENV PORT=8000
EXPOSE $PORT

# Run Chainlit (browser UI) - use Railway's PORT env var
CMD ["sh", "-c", "chainlit run app.py --host 0.0.0.0 --port ${PORT:-8000}"]
