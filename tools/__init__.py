"""
Tool bindings: every agent gets the tools it declares in system_design.json.
Design-driven: load each agent's "tools" array and map to implementations (Instantly, HeyGen, Stripe, or stubs).
"""
from pathlib import Path
from typing import Any, Callable, Dict, List

from tools.registry import (
    get_tools_for_agent,
    list_bindings,
    get_agent_tool_names,
    required_integrations_for_agent,
    required_integrations_all,
    agents_needing_integration,
    IMPLEMENTATIONS,
    normalize_design_tool,
    design_tool_to_registry_key,
    get_implementation,
)

__all__ = [
    "get_tools_for_agent",
    "list_bindings",
    "get_agent_tool_names",
    "required_integrations_for_agent",
    "required_integrations_all",
    "agents_needing_integration",
    "has_tools",
    "IMPLEMENTATIONS",
    "normalize_design_tool",
    "design_tool_to_registry_key",
    "get_implementation",
]


def has_tools(agent_id: str, design_path: Path | None = None) -> bool:
    """True if this agent has at least one tool in the design."""
    return len(get_agent_tool_names(agent_id, design_path)) > 0
