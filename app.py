"""
Chainlit UI for the recruitment workflow — browser-based, step-by-step (Lovable-style).
Run: chainlit run app.py -w
Use side-by-side: Cursor (code) + browser (steps). Reloads keep state via SQLite checkpointer.
"""
import asyncio
import sys
import uuid
from pathlib import Path

# Ensure master_graph (in output/) is importable — from project root and in Docker (WORKDIR /app)
ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
# Railway/Docker: insert /app/output first so "from master_graph" always finds output/master_graph.py
_DOCKER_OUTPUT = Path("/app/output")
if _DOCKER_OUTPUT.exists():
    sys.path.insert(0, str(_DOCKER_OUTPUT))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(OUTPUT_DIR))

import chainlit as cl


def _initial_state(user_input: str = "Starting recruitment process"):
    from master_graph import RecruitmentState
    return RecruitmentState(
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
        data={"initial_input": user_input},
    )


# Human step prompts (same as in master_graph) so we can show them in the UI
HUMAN_PROMPTS = {
    "human_outbound_caller": "Make outbound calls. Enter call outcomes:",
    "human_client_job_intake": "Conduct client job intake. Enter job requirements:",
    "human_candidate_interview": "Interview candidate. Enter interview assessment:",
    "human_offer_negotiation": "Handle offer negotiation. Enter final offer terms:",
    "human_temp_onboarding_review": "Review temp contract. Enter contract status:",
    "human_strategy_oversight": "Strategic oversight review. Enter strategic decisions:",
    "human_initial_screening_call": "Conduct initial screening call. Enter call notes:",
    "human_legal_compliance_verification": "Review compliance documents. Enter verification status:",
    "human_client_submission_approval": "Review candidate matches. Approve candidates (yes/no):",
    "human_interview_prep_debriefer": "Conduct interview prep and debrief. Enter notes:",
    "human_candidate_follow_up": "Follow up with candidate. Enter follow-up notes:",
}


def _get_human_prompt(state: dict) -> str:
    step = (state.get("data") or {}).get("next_human_node") or state.get("next_human_node") or ""
    return HUMAN_PROMPTS.get(step, f"Handle human step: {step}. Enter your input:")


@cl.on_chat_start
async def start():
    try:
        from master_graph import get_graph_for_chainlit
    except Exception as e:
        await cl.Message(content=f"⚠️ Error loading master graph: {e}. Check Railway logs for details.").send()
        return
    
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
        db_path = ROOT / "data" / "recruitment_checkpoints.sqlite"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        # Use file path for SQLite (persists across Chainlit reloads)
        checkpointer = SqliteSaver.from_conn_string(f"file:{db_path}?mode=rwc")
    except Exception:
        from langgraph.checkpoint.memory import MemorySaver
        checkpointer = MemorySaver()
    
    try:
        graph = get_graph_for_chainlit(checkpointer)
    except Exception as e:
        await cl.Message(content=f"⚠️ Error creating graph: {e}. Check Railway logs.").send()
        return
    thread_id = str(uuid.uuid4())
    cl.user_session.set("graph", graph)
    cl.user_session.set("thread_id", thread_id)
    cl.user_session.set("waiting_for_human", False)
    cl.user_session.set("human_prompt", "")
    await cl.Message(
        content="**Recruitment workflow** is active. Type **Start** (or any message) to run the pipeline. "
                "You'll see each step in the UI. When a human step appears, reply in chat — your reply is fed back into the graph. "
                "Use **done** / **exit** to end the workflow."
    ).send()


async def _run_stream_and_collect_state(graph, initial_input, config):
    """Run graph stream in a thread; return (steps list, final_state, state_snapshot for interrupt check)."""
    loop = asyncio.get_event_loop()
    steps_done = []
    state_snapshot = None

    def run():
        nonlocal state_snapshot
        for event in graph.stream(initial_input, config=config, stream_mode="updates"):
            # event is dict like { "agent_lead_generation": {...}, ... }
            if isinstance(event, dict):
                for node_name, value in event.items():
                    if node_name:
                        steps_done.append((node_name, value))
        try:
            state_snapshot = graph.get_state(config)
        except Exception:
            pass
        return steps_done, state_snapshot

    return await loop.run_in_executor(None, run)


@cl.on_message
async def main(message: cl.Message):
    graph = cl.user_session.get("graph")
    thread_id = cl.user_session.get("thread_id")
    waiting = cl.user_session.get("waiting_for_human")
    config = {"configurable": {"thread_id": thread_id}}

    if not graph:
        await cl.Message(content="Session missing graph. Please refresh the page.").send()
        return

    # Resuming after a human step: inject the user's message and continue
    if waiting:
        cl.user_session.set("waiting_for_human", False)
        update = {"data": {"pending_human_input": message.content.strip()}}
        initial_input = update
    else:
        initial_input = _initial_state(message.content.strip() or "Start")

    # Stream steps to the UI (Lovable-style collapsible steps)
    steps_done = []
    state_snapshot = None
    try:
        steps_done, state_snapshot = await _run_stream_and_collect_state(graph, initial_input, config)
    except Exception as e:
        await cl.Message(content=f"Workflow error: {e}").send()
        return

    # Show each node as a step (agentic debugging: click into step to see output)
    for node_name, output in steps_done:
        async with cl.Step(name=node_name) as step:
            if isinstance(output, dict) and output:
                summary = []
                for k, v in list(output.items())[:5]:
                    if k == "data" and isinstance(v, dict):
                        summary.append(f"data keys: {list(v.keys())[:8]}")
                    elif v is not None and str(v)[:1] != "<":
                        summary.append(f"{k}: {str(v)[:80]}")
                if summary:
                    await step.stream_token("\n".join(summary) + "\n")
            else:
                await step.stream_token(f"Node **{node_name}** completed.\n")

    # Check if we're paused before a human step (interrupt_before)
    try:
        if state_snapshot and getattr(state_snapshot, "next", None):
            next_nodes = state_snapshot.next if isinstance(state_snapshot.next, (list, tuple)) else [state_snapshot.next]
            if next_nodes and "human_in_the_loop" in str(next_nodes):
                vals = getattr(state_snapshot, "values", None) or {}
                prompt = _get_human_prompt(vals)
                cl.user_session.set("waiting_for_human", True)
                cl.user_session.set("human_prompt", prompt)
                await cl.Message(
                    content=f"**Human step** — {prompt}\n\nReply in chat with your input (or type **done** / **exit** to finish)."
                ).send()
                return
    except Exception:
        pass

    # Check for workflow exit (from state after human node ran)
    try:
        if state_snapshot and getattr(state_snapshot, "values", None):
            data = (state_snapshot.values or {}).get("data") or {}
            if data.get("_workflow_exit"):
                await cl.Message(content="Workflow ended (you typed done/exit). Type **Start** to run again.").send()
                return
    except Exception:
        pass

    if not waiting and not steps_done:
        await cl.Message(content="Workflow started. Check the steps above; if a human step appears, reply in chat.").send()
