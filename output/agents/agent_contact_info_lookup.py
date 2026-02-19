from typing import Dict, Any


def agent_contact_info_lookup(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieves contact details (phone, email) for companies and specific roles.
    Sets next_human_node so the graph routes to human_outbound_caller for cold calls.
    """
    data = dict(state.get("data") or {})
    list_of_company_names = data.get("list_of_company_names") or state.get("client_requirements", {}).get("lead_companies") or []
    # Stub: would use online_search_tool, corporate_directories (or Clearbit/Apollo APIs)
    initial_client_contacts = []
    for name in list_of_company_names[:5]:
        initial_client_contacts.append({
            "company_name": name,
            "company_phone_number": "+44 20 7123 4567",
            "contact_email": f"hr@{name.lower().replace(' ', '')}.com",
            "target_role": "HR / Hiring Manager",
        })
    data["initial_client_contact_details"] = initial_client_contacts
    data["next_human_node"] = "human_outbound_caller"
    return {
        **state,
        "data": data,
        "client_requirements": {
            **state.get("client_requirements", {}),
            "initial_client_contact_details": initial_client_contacts,
        },
    }
