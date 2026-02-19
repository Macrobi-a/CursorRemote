"""
Global tool registry: every design-declared tool maps to an implementation (real API or stub).
Any agent gets exactly the tools its system_design.json entry declares.
"""
import json
import os
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, TypedDict

# Real API implementations
from tools.instantly import instantly_send_campaign, instantly_add_leads, instantly_get_campaigns
from tools.heygen import heygen_create_video
from tools.stripe_tools import stripe_create_invoice, stripe_create_customer

# Implementation names agents can call by (in addition to design-normalized keys)
IMPLEMENTATION_NAMES = [
    "instantly_send_campaign", "instantly_add_leads", "instantly_get_campaigns",
    "heygen_create_video", "stripe_create_invoice", "stripe_create_customer",
]

# Real integrations: registry_key -> env var and label. Missing = stub only (user must add integration).
INTEGRATION_INFO: Dict[str, Dict[str, str]] = {
    "instantly_send_campaign": {"env_var": "INSTANTLY_API_KEY", "name": "Instantly (outreach)", "docs": "https://developer.instantly.ai/"},
    "instantly_add_leads": {"env_var": "INSTANTLY_API_KEY", "name": "Instantly (outreach)", "docs": "https://developer.instantly.ai/"},
    "instantly_get_campaigns": {"env_var": "INSTANTLY_API_KEY", "name": "Instantly (outreach)", "docs": "https://developer.instantly.ai/"},
    "email_automation": {"env_var": "INSTANTLY_API_KEY", "name": "Instantly (email)", "docs": "https://developer.instantly.ai/"},
    "email_marketing_platform": {"env_var": "INSTANTLY_API_KEY", "name": "Instantly (email)", "docs": "https://developer.instantly.ai/"},
    "heygen_create_video": {"env_var": "HEYGEN_API_KEY", "name": "HeyGen (video)", "docs": "https://docs.heygen.com/"},
    "video_generation": {"env_var": "HEYGEN_API_KEY", "name": "HeyGen (video)", "docs": "https://docs.heygen.com/"},
    "stripe_create_invoice": {"env_var": "STRIPE_SECRET_KEY", "name": "Stripe (billing)", "docs": "https://dashboard.stripe.com/apikeys"},
    "stripe_create_customer": {"env_var": "STRIPE_SECRET_KEY", "name": "Stripe (billing)", "docs": "https://dashboard.stripe.com/apikeys"},
    "invoicing_software": {"env_var": "STRIPE_SECRET_KEY", "name": "Stripe (invoicing)", "docs": "https://dashboard.stripe.com/apikeys"},
    "invoicing": {"env_var": "STRIPE_SECRET_KEY", "name": "Stripe (invoicing)", "docs": "https://dashboard.stripe.com/apikeys"},
}

from tools.stubs import (
    ats_crm_update,
    ats_crm_search,
    calendar_scheduling_create,
    document_storage_upload,
    document_generation_render,
    crm_software_update,
    linkedin_recruiter_search,
    job_boards_post,
    web_scraper_fetch,
    payroll_submit,
    accounting_export,
    survey_send,
    online_search,
    industry_database_query,
    stub_generic,
)

# Registry key -> callable (one canonical implementation per capability)
IMPLEMENTATIONS: Dict[str, Callable[..., Any]] = {
    # Instantly (outreach / email)
    "instantly_send_campaign": instantly_send_campaign,
    "instantly_add_leads": instantly_add_leads,
    "instantly_get_campaigns": instantly_get_campaigns,
    "email_automation": instantly_send_campaign,
    "email_marketing_platform": instantly_send_campaign,
    # HeyGen (video)
    "heygen_create_video": heygen_create_video,
    "video_generation": heygen_create_video,
    # Stripe (billing)
    "stripe_create_invoice": stripe_create_invoice,
    "stripe_create_customer": stripe_create_customer,
    "invoicing_software": stripe_create_invoice,
    "invoicing": stripe_create_invoice,
    # Stubs (design tools without a concrete API yet)
    "ats_crm": ats_crm_update,
    "ats_crm_search": ats_crm_search,
    "calendar_scheduling": calendar_scheduling_create,
    "document_storage": document_storage_upload,
    "document_generation": document_generation_render,
    "crm_software": crm_software_update,
    "crm": crm_software_update,
    "linkedin_recruiter": linkedin_recruiter_search,
    "job_boards": job_boards_post,
    "web_scraper": web_scraper_fetch,
    "payroll": payroll_submit,
    "accounting": accounting_export,
    "survey": survey_send,
    "online_search": online_search,
    "industry_database": industry_database_query,
}

# Map normalized design tool string -> registry key (so each agent's declared tool gets an implementation)
# Order matters: more specific first. We normalize design tools and then match by substring or exact.
DESIGN_TO_REGISTRY: List[tuple[str, str]] = [
    ("instantly", "instantly_send_campaign"),
    ("email_marketing", "email_marketing_platform"),
    ("email_automation", "email_automation"),
    ("email_sms", "email_automation"),
    ("email_parsing", "email_automation"),
    ("heygen", "heygen_create_video"),
    ("video", "heygen_create_video"),
    ("stripe", "stripe_create_invoice"),
    ("invoice", "invoicing_software"),
    ("invoicing", "invoicing_software"),
    ("accounting", "accounting"),
    ("payroll", "payroll"),
    ("ats_crm", "ats_crm"),
    ("ats_keyword", "ats_crm_search"),
    ("ats_screening", "ats_crm_search"),
    ("calendar", "calendar_scheduling"),
    ("scheduling", "calendar_scheduling"),
    ("calendly", "calendar_scheduling"),
    ("document_generation", "document_generation"),
    ("document_management", "document_storage"),
    ("dms", "document_storage"),
    ("sharepoint", "document_storage"),
    ("crm", "crm_software"),
    ("linkedin", "linkedin_recruiter"),
    ("job_board", "job_boards"),
    ("job_board_apis", "job_boards"),
    ("web_scraper", "web_scraper"),
    ("web_scraping", "web_scraper"),
    ("industry_database", "industry_database"),
    ("online_search", "online_search"),
    ("corporate_directories", "online_search"),
    ("survey", "survey"),
    ("docusign", "document_generation"),
    ("contract_template", "document_generation"),
    ("bi_dashboard", "accounting"),
    ("reporting", "accounting"),
]


def normalize_design_tool(raw: str) -> str:
    """Turn a design tool string into a key: lowercase, replace / and spaces with underscore, drop parentheticals."""
    s = (raw or "").strip().lower()
    s = re.sub(r"\s*\([^)]*\)", "", s)
    s = re.sub(r"[\s/\-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "unknown"


def design_tool_to_registry_key(normalized: str) -> str:
    """Resolve a normalized design tool to a registry key (implementation)."""
    for pattern, reg_key in DESIGN_TO_REGISTRY:
        if pattern in normalized or normalized in pattern:
            return reg_key
    if normalized in IMPLEMENTATIONS:
        return normalized
    return "stub_generic"


def get_implementation(registry_key: str) -> Callable[..., Any] | None:
    return IMPLEMENTATIONS.get(registry_key)


def _load_design(path: Path | None = None) -> Dict[str, Any]:
    if path is None:
        path = Path(__file__).resolve().parent.parent / "output" / "system_design.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_agent_tool_names(agent_id: str, design_path: Path | None = None) -> List[str]:
    """Return the raw list of tool names (from system_design.json) for the given agent."""
    design = _load_design(design_path)
    for a in design.get("agents", []):
        if a.get("id") == agent_id:
            return list(a.get("tools", []))
    return []


def get_tools_for_agent(agent_id: str, design_path: Path | None = None) -> Dict[str, Callable[..., Any]]:
    """
    Return tool_name -> callable for this agent based on system_design.json.
    Every agent gets the tools it declares; each maps to a real implementation or stub.
    """
    tool_names = get_agent_tool_names(agent_id, design_path)
    out: Dict[str, Callable[..., Any]] = {}
    seen_registry: set = set()
    for raw in tool_names:
        norm = normalize_design_tool(raw)
        reg_key = design_tool_to_registry_key(norm)
        if reg_key not in seen_registry:
            fn = get_implementation(reg_key)
            if not fn and reg_key == "stub_generic":
                fn = lambda *a, _n=norm, **k: stub_generic(tool_name=_n, *a, **k)
            if fn:
                seen_registry.add(reg_key)
                out[norm] = fn
                # Agents can also call by implementation name (e.g. instantly_add_leads)
                for impl_name in IMPLEMENTATION_NAMES:
                    if get_implementation(impl_name) is fn and impl_name not in out:
                        out[impl_name] = fn
    return out


def list_bindings(design_path: Path | None = None) -> Dict[str, List[str]]:
    """Return agent_id -> list of (normalized) tool names from the design."""
    design = _load_design(design_path)
    result: Dict[str, List[str]] = {}
    for a in design.get("agents", []):
        aid = a.get("id")
        if not aid:
            continue
        raw_tools = a.get("tools", [])
        result[aid] = [normalize_design_tool(t) for t in raw_tools]
    return result


class IntegrationRequirement(TypedDict, total=False):
    agent_id: str
    agent_name: str
    tool_design_name: str
    tool_registry_key: str
    status: str  # "configured" | "needs_key" | "stub"
    env_var: str
    integration_name: str
    docs: str
    message: str


def _is_configured(registry_key: str) -> bool:
    """True if this implementation has its required env var set."""
    info = INTEGRATION_INFO.get(registry_key)
    if not info:
        return False
    return bool(os.environ.get(info["env_var"], "").strip())


def required_integrations_for_agent(agent_id: str, design_path: Path | None = None) -> List[IntegrationRequirement]:
    """
    For one agent, list each tool it needs and whether you must add a real integration.
    status: "configured" = API key set; "needs_key" = real API but key missing; "stub" = no API bound, add integration.
    """
    design = _load_design(design_path)
    agent_name = ""
    for a in design.get("agents", []):
        if a.get("id") == agent_id:
            agent_name = a.get("name", agent_id)
            break
    tool_names = get_agent_tool_names(agent_id, design_path)
    seen_registry: set = set()
    out: List[IntegrationRequirement] = []
    for raw in tool_names:
        norm = normalize_design_tool(raw)
        reg_key = design_tool_to_registry_key(norm)
        if reg_key in seen_registry:
            continue
        seen_registry.add(reg_key)
        info = INTEGRATION_INFO.get(reg_key)
        if info:
            if _is_configured(reg_key):
                status = "configured"
                message = f"Set {info['env_var']} (OK)"
            else:
                status = "needs_key"
                message = f"Add real integration for this agent to do its job: set {info['env_var']} in .env. See {info['docs']}"
        else:
            status = "stub"
            message = "Add a real integration for this agent to do its job properly (no API bound yet). Implement or plug in an API for this tool."
        out.append(IntegrationRequirement(
            agent_id=agent_id,
            agent_name=agent_name,
            tool_design_name=raw,
            tool_registry_key=reg_key,
            status=status,
            env_var=info.get("env_var", "") if info else "",
            integration_name=info.get("name", "Custom integration") if info else "Custom integration",
            docs=info.get("docs", "") if info else "",
            message=message,
        ))
    return out


def required_integrations_all(design_path: Path | None = None) -> Dict[str, List[IntegrationRequirement]]:
    """Per agent_id, list of integration requirements (so the system can ask you to add real integrations)."""
    design = _load_design(design_path)
    result: Dict[str, List[IntegrationRequirement]] = {}
    for a in design.get("agents", []):
        aid = a.get("id")
        if not aid:
            continue
        result[aid] = required_integrations_for_agent(aid, design_path)
    return result


def agents_needing_integration(design_path: Path | None = None) -> List[tuple[str, str, List[IntegrationRequirement]]]:
    """List of (agent_id, agent_name, requirements) where at least one tool is not configured (needs_key or stub)."""
    all_reqs = required_integrations_all(design_path)
    out: List[tuple[str, str, List[IntegrationRequirement]]] = []
    for agent_id, reqs in all_reqs.items():
        need = [r for r in reqs if r["status"] != "configured"]
        if not need:
            continue
        name = (reqs[0].get("agent_name") or agent_id) if reqs else agent_id
        out.append((agent_id, name, need))
    return out
