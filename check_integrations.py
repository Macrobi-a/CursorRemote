"""
Ask the user to add real integrations for each AI agent to do its job properly.
Run: python check_integrations.py
Shows which agents need which API keys or custom integrations (stubs).
"""
import sys
from pathlib import Path

# Project root
sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools import agents_needing_integration, required_integrations_all


def main() -> None:
    need = agents_needing_integration()
    if not need:
        print("All agents have their tools configured (or no agents in design).")
        return

    print()
    print("=" * 70)
    print("REAL INTEGRATIONS NEEDED PER AGENT")
    print("Add the following so each AI agent can do its job properly.")
    print("=" * 70)

    for agent_id, agent_name, reqs in need:
        print()
        print(f"Agent: {agent_name} ({agent_id})")
        print("-" * 60)
        for r in reqs:
            status = r["status"]
            msg = r["message"]
            if status == "needs_key":
                print(f"  - Tool: {r['tool_design_name']}")
                print(f"    -> Add real integration: set {r.get('env_var', '')} in .env")
                print(f"    -> {r.get('docs', '')}")
            else:
                print(f"  - Tool: {r['tool_design_name']}")
                print(f"    -> {msg}")
        print()

    print("=" * 70)
    print("Summary: set env vars in .env (see .env.example), or implement and")
    print("register a real API for stub tools in tools/registry.py.")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
