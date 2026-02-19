"""
Generate only output/master_graph.py from system_design.json and existing output/agents/*.py.
Run after generate_agents_from_design.py has created the agent files.
"""
import json
import re
import sys
from pathlib import Path

import anthropic

from config import AGENTS_DIR, ANTHROPIC_API_KEY, OUTPUT_DIR, SYSTEM_DESIGN_JSON

MODEL = "claude-sonnet-4-20250514"

MASTER_GRAPH_PROMPT = """You are a code generator. You will receive:
1) A System Design JSON (agents, human_nodes, edges).
2) A list of existing agent Python module names in output/agents/ (e.g. agent_candidate_data_capture.py).

Generate exactly ONE Python file: output/master_graph.py

Requirements for master_graph.py:
- Use LangGraph: from langgraph.graph import StateGraph, END.
- Define a shared state (TypedDict or dict) that can hold inputs/outputs for all agents and human steps (use a flexible dict with keys that agents expect).
- Import each agent as a function from the agents package. Since the graph will be run from the project root with output on sys.path, use:
  import sys
  sys.path.insert(0, str(Path(__file__).resolve().parent))
  from agents.agent_XXX import agent_XXX  # for each agent
- Add one node per agent (node name = agent id from JSON, e.g. agent_candidate_data_capture).
- Add a single node "human_in_the_loop" that:
  - Receives state and a human_step_id (or next human node id from the edge).
  - Uses input() or a simple callback to get human input and return updated state.
  - Handles all human_node ids by prompting for the relevant data (you can use a dict of prompts per human_step_id).
- Add edges from the "edges" array. Map any "to" that starts with human_ to the node "human_in_the_loop" (and pass the human node id in state so the human knows what to do). Map "from": "start" to the first agent(s).
- For edges with "condition", use add_conditional_edges where appropriate; for simplicity you can also add multiple unconditional edges and let the graph route.
- Compile the graph: graph = builder.compile().
- Add a if __name__ == "__main__": block that runs the graph with an initial state (e.g. empty dict or minimal keys) and prints the result.

Rules:
- Code must be runnable Python 3.10+. Run from project root: python output/master_graph.py (so that output/ is on path and from agents.agent_xxx works after sys.path.insert).
- Use only standard library + langgraph. Agent modules are in output/agents/ and expose a function agent_<name>(state) -> state.
- Node names in the graph must match: agent ids from JSON for agent nodes, and "human_in_the_loop" for any human node.
- Keep the graph construction clear: add all agent nodes, add human_in_the_loop, then add edges in order.

Output your response as a single fenced code block. The first line of the block must be exactly:
# output/master_graph.py
Use opening fence: ```python
"""


def extract_master_graph_code(text: str) -> str | None:
    """Extract the first Python code block; optionally strip # output/master_graph.py from first line."""
    path_pattern = re.compile(r"```(\w*)\s*\n(.*?)```", re.DOTALL)
    for m in path_pattern.finditer(text):
        code = (m.group(2) or "").strip()
        if not code:
            continue
        first = code.split("\n")[0].strip()
        if re.match(r"#\s*output/master_graph\.py", first):
            code = "\n".join(code.split("\n")[1:]).strip()
        return code
    return None


def main() -> None:
    if not SYSTEM_DESIGN_JSON.exists():
        print("Missing output/system_design.json. Run video_to_system_design.py first.", file=sys.stderr)
        sys.exit(1)
    if not ANTHROPIC_API_KEY:
        print("Set ANTHROPIC_API_KEY in .env", file=sys.stderr)
        sys.exit(2)

    design = json.loads(SYSTEM_DESIGN_JSON.read_text(encoding="utf-8"))
    agent_files = sorted(p.name for p in AGENTS_DIR.glob("*.py") if p.suffix == ".py")
    if not agent_files:
        print("No agent files in output/agents/. Run generate_agents_from_design.py first.", file=sys.stderr)
        sys.exit(3)

    # Build a compact summary for the prompt (full edges + human_nodes + agent ids)
    summary = {
        "agents": [{"id": a["id"]} for a in design.get("agents", [])],
        "human_nodes": design.get("human_nodes", []),
        "edges": design.get("edges", []),
    }
    design_str = json.dumps(summary, indent=2)
    agent_list_str = "\n".join(agent_files)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        messages=[{
            "role": "user",
            "content": f"{MASTER_GRAPH_PROMPT}\n\nSystem Design (summary):\n{design_str}\n\nExisting agent modules (output/agents/):\n{agent_list_str}",
        }],
    )
    text = message.content[0].text if message.content else ""
    code = extract_master_graph_code(text)
    if not code:
        (OUTPUT_DIR / "claude_master_graph_raw.txt").write_text(text, encoding="utf-8")
        print("No code block found. Raw response saved to output/claude_master_graph_raw.txt", file=sys.stderr)
        sys.exit(4)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    master_path = OUTPUT_DIR / "master_graph.py"
    master_path.write_text(code, encoding="utf-8")
    print(f"Wrote: {master_path}", flush=True)
    print("Run from project root: python output/master_graph.py", flush=True)


if __name__ == "__main__":
    main()
