# Deployment: Run 24/7 (Railway or AWS)

Run the recruitment workflow as a **persistent server** so it operates without your laptop.

## Quick start (Railway)

1. Install Railway CLI: `npm i -g @railway/cli` or see https://docs.railway.app/
2. In project root:
   ```bash
   railway login
   railway init
   railway add --dockerfile Dockerfile
   ```
3. Set env vars in Railway dashboard: `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, and optionally `INSTANTLY_API_KEY`, `HEYGEN_API_KEY`, `STRIPE_SECRET_KEY`.
4. Deploy:
   ```bash
   railway up
   ```
5. Your app will get a URL. Use `GET /health` for liveness.

## AWS (ECS / App Runner / EC2)

- **Option A – App Runner**: Build from this repo, use the Dockerfile, set env vars in the console, deploy. App Runner calls `GET /health` for health checks.
- **Option B – ECS**: Build image with `docker build -t recruitment-workflow .`, push to ECR, create a task definition and service. Set `PORT=8000` and map port 8000.
- **Option C – EC2**: On an EC2 instance, clone repo, install deps, run `uvicorn server:app --host 0.0.0.0 --port 8000` (e.g. with systemd or screen).

## Endpoints

| Endpoint       | Description |
|----------------|-------------|
| `GET /`        | Brief info  |
| `GET /health`  | Liveness (returns `ok`) |
| `GET /tools`   | List agent → API tool bindings (Instantly, HeyGen, Stripe) |
| `POST /run`    | Trigger one run of the master graph (body: `{"initial_input": "..."}`) |

**Note:** `POST /run` runs the graph until it hits a human step (which uses `input()`). For fully autonomous 24/7 operation, replace human steps with a queue or webhook that supplies responses from your UI or external system.

## Tool bindings (APIs)

Set these in `.env` or your platform’s env vars so agents can perform real actions:

- **Instantly** (outreach): `INSTANTLY_API_KEY` – used by outreach/email agents.
- **HeyGen** (video): `HEYGEN_API_KEY` – used for video outreach/follow-up.
- **Stripe** (billing): `STRIPE_SECRET_KEY` – used for invoices and customers.

See `.env.example` and the `tools/` package for details.
