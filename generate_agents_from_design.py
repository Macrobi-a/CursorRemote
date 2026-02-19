"""
Step 2: Read output/system_design.json, call Claude to generate:
  - output/agents/<agent_id>.py for each agent
  - output/master_graph.py (LangGraph graph + human-in-the-loop)
"""
import json
import re
import sys
from pathlib import Path

import anthropic

from config import AGENTS_DIR, ANTHROPIC_API_KEY, OUTPUT_DIR, SYSTEM_DESIGN_JSON

# Use a capable model for code generation (Claude 4 / Sonnet 4 or latest)
MODEL = "claude-sonnet-4-20250514"

PROMPT = """You are a code generator. You will receive a System Design JSON that describes agents, human nodes, and edges for automating a business course.

Generate the following as separate Python code blocks. Output ONLY the requested code blocks, each wrapped in a fenced block with the exact filename as the label.

1) For EACH agent in the "agents" array, output one code block with label: `output/agents/<agent_id>.py`
   - Each file must define a runnable agent that:
     - Accepts inputs (dict or typed state) and returns outputs (dict or state updates).
     - Uses LangChain/LangGraph-friendly tools where listed (you can stub tools with placeholder implementations).
     - Is a function or callable that can be used as a node in a LangGraph graph (e.g. def agent_xxx(state: dict) -> dict).
   - File name must be exactly the agent "id" + ".py" (e.g. agent_outreach.py).

2) One code block with label: `output/master_graph.py`
   - Build a LangGraph StateGraph that:
     - Has a shared state type (e.g. TypedDict) with fields for all agent inputs/outputs and human_node inputs/outputs.
     - Adds a node for each agent (import from agents/<agent_id>.py and add as node).
     - Adds a node for "human_in_the_loop" that:
       - Receives state when the graph needs human action (e.g. for any human_node in the design).
       - Returns updated state after human provides input (e.g. meeting_notes, next_steps).
       - Can be implemented as a function that prompts for input (input() or a callback) and returns state updates.
     - Adds edges according to "edges" in the JSON (from/to node names: use agent id for agents, "human_in_the_loop" for human nodes, "start" -> first agent).
     - Conditional edges: implement where "condition" is present (e.g. route to human when meeting_requested).
   - Compile the graph and expose a runnable (e.g. graph.compile() and a main that invokes it).
   - Use LangGraph: from langgraph.graph import StateGraph, END; state type as a TypedDict or dict.

Rules:
- Code must be runnable Python 3.10+.
- Use only standard library + langgraph, langchain_core (and langchain_anthropic if you need an LLM in an agent). No other packages unless necessary.
- In master_graph.py, node names must match: agent ids from JSON (e.g. agent_outreach), and "human_in_the_loop" for human steps.
- If the design has no human_nodes, still add a human_in_the_loop node that can be used for oversight (e.g. optional review step).
- Output each file in order: all output/agents/<agent_id>.py blocks first, then output/master_graph.py."""


def extract_code_blocks(text: str) -> dict[str, str]:
    """Extract fenced code blocks; key = path (e.g. output/agents/agent_foo.py), value = code."""
    # Match ```label\n...code...``` (label may be "python" or "output/agents/xxx.py")
    path_pattern = re.compile(r"```(\w*)\s*\n(.*?)```", re.DOTALL)
    out = {}
    for m in path_pattern.finditer(text):
        label = (m.group(1) or "").strip()
        code = (m.group(2) or "").strip()
        if not code:
            continue
        # Path can be in fence label (output/agents/xxx.py) or in first line of code (# output/...)
        path = None
        if "output/" in label:
            path = label.split()[0] if " " in label else label
        else:
            first_line = code.split("\n")[0].strip()
            comment_match = re.match(r"#\s*(output/[\w/\.\-]+\.py)", first_line)
            if comment_match:
                path = comment_match.group(1).strip()
                code = "\n".join(code.split("\n")[1:]).strip()  # drop path comment line
        if path and path not in out:
            out[path] = code
    return out


def main() -> None:
    if not SYSTEM_DESIGN_JSON.exists():
        print(f"Missing {SYSTEM_DESIGN_JSON}. Run video_to_system_design.py first.", file=sys.stderr)
        sys.exit(1)
    if not ANTHROPIC_API_KEY:
        print("Set ANTHROPIC_API_KEY in .env", file=sys.stderr)
        sys.exit(2)

    design = json.loads(SYSTEM_DESIGN_JSON.read_text(encoding="utf-8"))
    design_str = json.dumps(design, indent=2)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        messages=[{"role": "user", "content": f"{PROMPT}\n\nSystem Design JSON:\n{design_str}"}],
    )
    text = message.content[0].text if message.content else ""

    blocks = extract_code_blocks(text)
    if not blocks:
        (OUTPUT_DIR / "claude_raw_response.txt").write_text(text, encoding="utf-8")
        print("No code blocks found. Raw response saved to output/claude_raw_response.txt", file=sys.stderr)
        sys.exit(3)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    for path_key, code in blocks.items():
        # path_key e.g. "output/agents/agent_outreach.py" or "output/master_graph.py"
        if path_key.startswith("output/"):
            rel = path_key[7:]  # strip "output/"
        else:
            rel = path_key
        p = OUTPUT_DIR / rel
        if ".." in rel or not str(p.resolve()).startswith(str(OUTPUT_DIR.resolve())):
            p = OUTPUT_DIR / Path(path_key).name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(code, encoding="utf-8")
        print(f"Wrote: {p}", flush=True)

    print("Done. Run the master graph: python output/master_graph.py (or from your app).", flush=True)


if __name__ == "__main__":
    main()
