# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python-based "Course-to-Agents" pipeline that converts business course videos into a multi-agent recruitment workflow using LangGraph. The pre-generated output in `output/` contains 41 agent files and a master graph that can be run without re-generating.

### Services

| Service | Command | Port | Notes |
|---------|---------|------|-------|
| **Chainlit UI** | `chainlit run app.py --host 0.0.0.0 --port 8080` | 8080 | Browser-based step-by-step workflow UI |
| **FastAPI server** | `uvicorn server:app --host 0.0.0.0 --port 8000` | 8000 | REST API with `/health`, `/tools`, `/run` endpoints |

### Running services

- Both services can run simultaneously on different ports.
- The `.chainlit/config.toml` file may become outdated when Chainlit is upgraded. If Chainlit fails to start with a "config file is outdated" error, delete `.chainlit/config.toml` and restart — Chainlit regenerates it automatically.
- The `.env` file must exist (copy from `.env.example`). API keys (Gemini, Anthropic) are only required for the generation pipeline; the runtime workflow and UI work without them since all tool integrations gracefully degrade to stubs.

### Linting

No lint configuration is committed. Use `flake8 --max-line-length=120 --exclude=.venv,output/agents` for basic checks. The `output/agents/` directory contains auto-generated code and is excluded from linting.

### Testing

No automated test suite exists. Verify the setup by:
1. Importing the master graph: `python -c "import sys; sys.path.insert(0,'output'); from master_graph import graph; print('OK')"`
2. Checking the FastAPI health endpoint: `curl http://localhost:8000/health`
3. Loading the Chainlit UI at `http://localhost:8080` and typing "Start"
