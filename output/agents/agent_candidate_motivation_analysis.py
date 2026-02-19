from typing import Dict, Any

def agent_candidate_motivation_analysis(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts and categorizes deep-seated candidate motivations and potential deal-breakers from interview data
    """
    # Stub implementation - would integrate with AI NLP for motivation extraction
    interview_responses = state.get("candidate_interview_responses", "")
    suitability_rating = state.get("initial_suitability_rating", "medium")
    
    # Analyze motivations (placeholder logic)
    detailed_motivations = {
        "salary_expectations": {
            "minimum_acceptable": 65000,
            "target": 75000,
            "negotiation_flexibility": "moderate"
        },
        "acceptance_threshold": {
            "must_haves": ["Competitive salary", "Growth opportunities", "Good team"],
            "nice_to_haves": ["Remote work", "Learning budget", "Flexible hours"],
            "deal_breakers": ["Long commute", "No career progression", "Toxic culture"]
        },
        "commute_preferences": {
            "max_commute_time": "45 minutes",
            "transport_preference": "Public transport",
            "remote_work_importance": "high"
        },
        "progression_desires": {
            "career_goal": "Senior Engineer then Tech Lead",
            "timeline": "2-3 years",
            "learning_priorities": ["Leadership skills", "System architecture"]
        },
        "team_preferences": {
            "team_size": "5-10 people",
            "collaboration_style": "Agile/collaborative",
            "management_style": "Supportive and hands-off"
        },
        "benefits": {
            "health_insurance": "important",
            "pension": "important",
            "learning_budget": "very important",
            "holiday_allowance": "standard expectations"
        }
    }
    
    return {
        **state,
        "detailed_candidate_motivations": detailed_motivations
    }