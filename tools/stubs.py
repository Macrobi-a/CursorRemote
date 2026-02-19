"""
Stub implementations for design-declared tools that don't yet have a real API binding.
Each returns a consistent shape so agents can branch: if result.get("stub") then fallback logic.
"""
from typing import Any, Dict, List


def _stub(tool_name: str, **kwargs: Any) -> Dict[str, Any]:
    return {"ok": False, "stub": True, "tool": tool_name, "message": "Not implemented", **kwargs}


def ats_crm_update(profile: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """ATS/CRM update - stub until integrated with real ATS (e.g. Greenhouse, Lever)."""
    return _stub("ats_crm", **kwargs)


def ats_crm_search(query: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """ATS/CRM search - stub."""
    return _stub("ats_crm_search", **kwargs)


def email_automation_send(to: str, subject: str, body: str, **kwargs: Any) -> Dict[str, Any]:
    """Send email - stub when Instantly not used; otherwise use Instantly."""
    return _stub("email_automation", **kwargs)


def calendar_scheduling_create(event: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Calendar/scheduling - stub until Calendly/Microsoft Bookings API."""
    return _stub("calendar_scheduling", **kwargs)


def document_storage_upload(file_ref: str, metadata: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """DMS/SharePoint/Drive - stub."""
    return _stub("document_storage", **kwargs)


def document_generation_render(template_id: str, variables: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Document generation - stub until DocuSign/Google Docs API."""
    return _stub("document_generation", **kwargs)


def crm_software_update(record: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """CRM (Salesforce, HubSpot) - stub."""
    return _stub("crm_software", **kwargs)


def linkedin_recruiter_search(params: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """LinkedIn Recruiter / Sales Navigator - stub until API."""
    return _stub("linkedin_recruiter", **kwargs)


def job_boards_post(job: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Job boards (Indeed, etc.) - stub."""
    return _stub("job_boards", **kwargs)


def web_scraper_fetch(url: str, **kwargs: Any) -> Dict[str, Any]:
    """Web scraper - stub."""
    return _stub("web_scraper", **kwargs)


def payroll_submit(entries: List[Dict[str, Any]], **kwargs: Any) -> Dict[str, Any]:
    """Payroll - stub until Sonovate/Xero."""
    return _stub("payroll", **kwargs)


def accounting_export(report_type: str, **kwargs: Any) -> Dict[str, Any]:
    """Accounting (Xero, QuickBooks) - stub."""
    return _stub("accounting", **kwargs)


def survey_send(recipient: str, template_id: str, **kwargs: Any) -> Dict[str, Any]:
    """Survey / feedback collection - stub."""
    return _stub("survey", **kwargs)


def online_search(query: str, **kwargs: Any) -> Dict[str, Any]:
    """Online search / corporate directories - stub."""
    return _stub("online_search", **kwargs)


def industry_database_query(criteria: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Industry database - stub."""
    return _stub("industry_database", **kwargs)


def stub_generic(tool_name: str = "unknown", **kwargs: Any) -> Dict[str, Any]:
    """Fallback for any design-declared tool that has no implementation yet."""
    return _stub("generic", tool=tool_name, **kwargs)
