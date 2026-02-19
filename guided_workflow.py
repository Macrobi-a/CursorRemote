"""
Guided workflow: explain the revenue-from-course path, then walk the human
step-by-step in logical order. For each step, explain clearly; when it's a human
task, explain what to do and wait for the human to report back, then continue.
Run after the course has been processed (output/system_design.json exists).
"""
import json
from collections import deque
from pathlib import Path

from config import SYSTEM_DESIGN_JSON


def load_design():
    path = SYSTEM_DESIGN_JSON
    if not path.exists():
        raise SystemExit("Run the pipeline first so output/system_design.json exists.")
    return json.loads(path.read_text(encoding="utf-8"))


def ordered_steps_from_edges(edges: list, agents: list, human_nodes: list) -> list[tuple[str, str]]:
    """Build a logical order of steps (agent then human) from the graph edges. Returns [(node_id, "agent"|"human"), ...]."""
    agent_ids = {a["id"] for a in agents}
    human_ids = {h["id"] for h in human_nodes}
    # Edges from each node (first edge only per source to get a simple path; we'll add more for full coverage)
    out_edges = {}
    for e in edges:
        src = e.get("from") or ""
        tgt = e.get("to") or ""
        if src == "start":
            src = "__start__"
        if tgt not in agent_ids and tgt not in human_ids:
            continue
        if src not in out_edges:
            out_edges[src] = []
        out_edges[src].append(tgt)

    # BFS from start; collect (node_id, type) in discovery order, each node once
    seen = set()
    order = []
    q = deque(out_edges.get("__start__", []))
    while q:
        n = q.popleft()
        if n in seen:
            continue
        seen.add(n)
        if n in agent_ids:
            order.append((n, "agent"))
        elif n in human_ids:
            order.append((n, "human"))
        for next_n in out_edges.get(n, []):
            if next_n not in seen:
                q.append(next_n)
    return order


def main():
    design = load_design()
    course_summary = design.get("course_summary", "")
    agents = design.get("agents", [])
    human_nodes = design.get("human_nodes", [])
    edges = design.get("edges", [])

    agents_by_id = {a["id"]: a for a in agents}
    human_by_id = {h["id"]: h for h in human_nodes}

    steps = ordered_steps_from_edges(edges, agents, human_nodes)
    if not steps:
        # Fallback: list agents first, then human nodes
        steps = [(a["id"], "agent") for a in agents] + [(h["id"], "human") for h in human_nodes]

    # --- Intro: what the course is and the full path to revenue ---
    print()
    print("=" * 60)
    print("GUIDED WORKFLOW: FROM COURSE TO REVENUE")
    print("=" * 60)
    print()
    print("The course has been analysed. Here's what it covers:")
    print()
    print(course_summary)
    print()
    print("-" * 60)
    print("STEPS TO GENERATE REVENUE (in logical order)")
    print("-" * 60)
    for i, (node_id, kind) in enumerate(steps, 1):
        if kind == "agent":
            a = agents_by_id.get(node_id, {})
            name = a.get("name", node_id)
            print(f"  {i}. [AUTOMATED] {name}")
        else:
            h = human_by_id.get(node_id, {})
            desc = (h.get("description") or "")[:60] + "..." if len(h.get("description") or "") > 60 else (h.get("description") or node_id)
            print(f"  {i}. [YOUR TASK] {desc}")
    print()
    print("We'll go through each step one by one. For automated steps you'll see what the system does; for your tasks you'll get a clear explanation and then report back.")
    print()
    # Ask user to add real integrations per agent
    try:
        from tools import agents_needing_integration
        need = agents_needing_integration()
        if need:
            print("-" * 60)
            print("INTEGRATIONS NEEDED")
            print("Each AI agent needs a real integration to do its job properly.")
            print("Run:  python check_integrations.py")
            print("to see what to add (env vars or APIs) for each agent.")
            print("-" * 60)
            print()
    except Exception:
        pass
    input("Press Enter to start step-by-step... ")
    print()

    # --- Step-by-step with explanations and report-back for human steps ---
    human_reports = []
    for i, (node_id, kind) in enumerate(steps, 1):
        print()
        print("=" * 60)
        print(f"STEP {i} of {len(steps)}")
        print("=" * 60)

        if kind == "agent":
            a = agents_by_id.get(node_id, {})
            name = a.get("name", node_id)
            role = a.get("role", "")
            outputs = a.get("outputs", [])
            tools = a.get("tools", [])
            print(f"[AUTOMATED] {name}")
            print()
            print(f"  What this step does: {role}")
            if outputs:
                print(f"  It produces: {', '.join(outputs)}")
            if tools:
                print(f"  Tools used: {', '.join(tools)}")
            try:
                from tools import required_integrations_for_agent
                reqs = required_integrations_for_agent(node_id)
                need = [r for r in reqs if r.get("status") != "configured"]
                if need:
                    print()
                    print("  To do this step properly, add a real integration for this agent:")
                    for r in need[:3]:
                        print(f"    • {r.get('message', '')}")
                    if len(need) > 3:
                        print(f"    ... and {len(need) - 3} more (run python check_integrations.py).")
            except Exception:
                pass
            print()
            print("  (This step would run automatically in the full graph. Proceeding.)")
        else:
            h = human_by_id.get(node_id, {})
            desc = h.get("description", "")
            trigger = h.get("trigger_condition", "")
            inputs_from = h.get("inputs_from_agents", [])
            outputs_for = h.get("outputs_for_agents", [])
            print(f"[YOUR TASK] {node_id}")
            print()
            print("  What you need to do:")
            print(f"  {desc}")
            print()
            if trigger:
                print(f"  When this is needed: {trigger}")
            if inputs_from:
                print(f"  You have (from previous steps): {', '.join(inputs_from)}")
                # Clarify when "Initial client contact details" is required but comes from a different path
                if any("client contact" in str(x).lower() for x in inputs_from):
                    print()
                    print("  Note: Initial client contact details are normally produced by the Lead Generation")
                    print("  Agent and Contact Information Lookup Agent, then the human Outbound Caller step")
                    print("  (cold calls to get direct contact). Those steps appear later in this list. If you")
                    print("  don't have client contacts yet, source them (e.g. do that path first) or use your")
                    print("  own list, then do this task.")
            if outputs_for:
                print(f"  You need to produce / report: {', '.join(outputs_for)}")
            print()
            report = input("  Do this task, then type your report here and press Enter: ").strip()
            human_reports.append((node_id, report))
            if report.lower() in ("done", "exit", "quit"):
                print("  (Ending guided workflow. Type 'done', 'exit', or 'quit' at any report to finish.)")
                break
        print()

    # --- Summary ---
    print()
    print("=" * 60)
    print("WORKFLOW SESSION COMPLETE")
    print("=" * 60)
    if human_reports:
        print()
        print("Your reports:")
        for node_id, report in human_reports:
            print(f"  • {node_id}: {report[:80]}{'...' if len(report) > 80 else ''}")
    print()
    print("To run the full automated graph (agents + human-in-the-loop), use: python output/master_graph.py")
    print()


if __name__ == "__main__":
    main()
