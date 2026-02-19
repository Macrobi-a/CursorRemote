"""
Instantly.ai API (outreach / cold email). Use for outreach and email automation agents.
API v2: https://developer.instantly.ai/
"""
import os
from typing import Any, Dict, List

try:
    import requests
except ImportError:
    requests = None

BASE_URL = "https://api.instantly.ai/api/v2"
_API_KEY = os.environ.get("INSTANTLY_API_KEY", "").strip()


def _headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {_API_KEY}", "Content-Type": "application/json"}


def instantly_send_campaign(
    campaign_id: str,
    lead_emails: List[str],
    variables: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """Launch or add to an Instantly campaign. Returns API response or error dict."""
    if not _API_KEY or not requests:
        return {"ok": False, "error": "INSTANTLY_API_KEY not set or requests not installed", "stub": True}
    url = f"{BASE_URL}/campaign/launch"
    payload = {
        "campaign_id": campaign_id,
        "lead_emails": lead_emails,
        "variables": variables or {},
    }
    try:
        r = requests.post(url, json=payload, headers=_headers(), timeout=30)
        return {"ok": r.status_code < 400, "status_code": r.status_code, "body": r.json() if r.text else {}}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def instantly_add_leads(
    campaign_id: str,
    leads: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Add leads to an Instantly campaign. Each lead: { email, first_name?, last_name?, company_name? }."""
    if not _API_KEY or not requests:
        return {"ok": False, "error": "INSTANTLY_API_KEY not set or requests not installed", "stub": True}
    url = f"{BASE_URL}/lead/add"
    payload = {"campaign_id": campaign_id, "leads": leads}
    try:
        r = requests.post(url, json=payload, headers=_headers(), timeout=30)
        return {"ok": r.status_code < 400, "status_code": r.status_code, "body": r.json() if r.text else {}}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def instantly_get_campaigns() -> Dict[str, Any]:
    """List Instantly campaigns."""
    if not _API_KEY or not requests:
        return {"ok": False, "error": "INSTANTLY_API_KEY not set or requests not installed", "campaigns": [], "stub": True}
    url = f"{BASE_URL}/campaign/list"
    try:
        r = requests.get(url, headers=_headers(), timeout=30)
        data = r.json() if r.text else {}
        return {"ok": r.status_code < 400, "campaigns": data.get("campaigns", data) if isinstance(data, dict) else []}
    except Exception as e:
        return {"ok": False, "error": str(e), "campaigns": []}
