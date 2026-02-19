from typing import Dict, Any

def agent_outreach_communicator(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sends initial outreach messages, manages replies, schedules initial calls/interviews, and maintains ongoing candidate communication.
    Tool binding: when INSTANTLY_API_KEY is set, uses Instantly.ai for outreach campaigns.
    """
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))  # project root
    tools = {}
    try:
        from tools import get_tools_for_agent
        tools = get_tools_for_agent("agent_outreach_communicator")
    except Exception:
        pass

    qualified_candidates = state.get("qualified_candidate_list", [])
    outreach_templates = state.get("predefined_outreach_templates", {})
    scheduling_availability = state.get("scheduling_availability", "9am-5pm weekdays")
    
    # Handle outreach (placeholder logic)
    engagement_status = {}
    scheduled_interviews = []
    candidate_queries = []
    additional_info_requests = []
    
    campaign_result = None
    if tools and qualified_candidates:
        add_leads = tools.get("instantly_add_leads")
        if add_leads:
            leads = [{"email": c.get("contact_info", {}).get("email") or f"{c.get('name', 'user')}@example.com", "first_name": (c.get("name") or "Candidate").split()[0]} for c in qualified_candidates[:20]]
            campaign_result = add_leads(campaign_id=state.get("data", {}).get("instantly_campaign_id") or "default", leads=leads)

    for candidate in qualified_candidates:
        name = candidate.get("name")
        # Simulate outreach responses (or use Instantly result when available)
        if candidate.get("qualification_score", 0) > 0.8:
            engagement_status[name] = "interested"
            # Schedule interview
            interview = {
                "candidate_name": name,
                "scheduled_time": "2024-01-05 2:00 PM",
                "interview_type": "initial_screening",
                "meeting_link": f"https://meet.example.com/{name.replace(' ', '_')}"
            }
            scheduled_interviews.append(interview)
        elif candidate.get("qualification_score", 0) > 0.7:
            engagement_status[name] = "interested"
            # Request additional info
            additional_info_requests.append({
                "candidate_name": name,
                "info_requested": ["passport_copy", "alternative_contact"],
                "reason": "eligibility_verification"
            })
        else:
            engagement_status[name] = "not_interested"
    
    data = dict(state.get("data") or {})
    if campaign_result:
        data["instantly_last_result"] = campaign_result
    return {
        **state,
        "data": data,
        "candidate_engagement_status": engagement_status,
        "scheduled_interviews": scheduled_interviews,
        "candidate_queries": candidate_queries,
        "request_for_additional_info": additional_info_requests
    }