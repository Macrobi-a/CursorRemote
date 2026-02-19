"""
Deployment server: run the recruitment graph 24/7 (Railway, AWS, or any host).
- Health check for orchestration.
- Optional: trigger workflow via API or run graph in background with human input via API.
"""
import os
import sys
from pathlib import Path

# Ensure project root and output are on path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "output"))

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

app = FastAPI(title="Recruitment workflow API", version="1.0")


@app.get("/", response_class=PlainTextResponse)
def root():
    return "Recruitment workflow server. GET /health to check. POST /run to trigger workflow (optional)."


@app.get("/health", response_class=PlainTextResponse)
def health():
    """Orchestrators (Railway, AWS, k8s) use this for liveness."""
    return "ok"


@app.get("/tools")
def list_tool_bindings():
    """List which agents are bound to which external APIs."""
    try:
        from tools import list_bindings
        return list_bindings()
    except Exception as e:
        return {"error": str(e), "bindings": {}}


@app.get("/integrations/required")
def integrations_required():
    """
    Ask: list per-agent tools that need a real integration to do their job properly.
    For each agent, either set the indicated env var (e.g. INSTANTLY_API_KEY) or add a real API for stub tools.
    """
    try:
        from tools import agents_needing_integration, required_integrations_all
        need = agents_needing_integration()
        all_reqs = required_integrations_all()
        return {
            "message": "Add a real integration for each AI agent to do its job properly. See per_agent list.",
            "per_agent": [
                {
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "requirements": [
                        {
                            "tool": r["tool_design_name"],
                            "status": r["status"],
                            "env_var": r.get("env_var"),
                            "integration_name": r.get("integration_name"),
                            "message": r["message"],
                            "docs": r.get("docs"),
                        }
                        for r in reqs
                    ],
                }
                for agent_id, agent_name, reqs in need
            ],
            "all_agents": {aid: [{"tool": r["tool_design_name"], "status": r["status"], "message": r["message"]} for r in reqs] for aid, reqs in all_reqs.items()},
        }
    except Exception as e:
        return {"error": str(e), "per_agent": [], "all_agents": {}}


class RunInput(BaseModel):
    initial_input: str = "Starting recruitment process (API)"


@app.post("/run")
def run_workflow(body: RunInput):
    """
    Run the master graph once. In production, human steps can be replaced with
    queued tasks or webhook callbacks so the system runs autonomously.
    """
    try:
        from master_graph import graph, RecruitmentState
        state = RecruitmentState(
            candidate_profile={},
            candidate_documents={},
            candidate_status="new",
            candidate_notes="",
            client_requirements={},
            client_feedback="",
            job_matches=[],
            current_step="start",
            human_step_id="",
            next_human_node="",
            interview_details={},
            offer_details={},
            documents=[],
            communications=[],
            financial_data={},
            data={"initial_input": body.initial_input},
        )
        result = graph.invoke(state)
        return {"ok": True, "current_step": result.get("current_step"), "data_keys": list(result.get("data", {}).keys())}
    except Exception as e:
        return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    # On startup, remind that agents need real integrations
    try:
        from tools import agents_needing_integration
        need = agents_needing_integration()
        if need:
            print("Integration check: the following agents need you to add a real integration to do their job properly.")
            print("Run: python check_integrations.py  or  GET /integrations/required")
            print(f"Agents needing integration: {len(need)}")
    except Exception:
        pass
    uvicorn.run(app, host="0.0.0.0", port=port)
