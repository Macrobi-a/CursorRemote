from typing import Dict, Any

def agent_interview_questionnaire_prep(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepares tailored interview questions to thoroughly vet candidates, focusing on motivations and practicalities
    """
    # Stub implementation - would integrate with document generator, AI question proposer
    job_description = state.get("structured_job_description", {})
    
    # Generate tailored questions (placeholder logic)
    interview_questions = {
        "technical_questions": [
            "Describe your experience with Python and React",
            "How would you approach scaling a web application?",
            "Tell me about a challenging technical problem you solved"
        ],
        "motivational_questions": [
            "What attracts you to this role specifically?",
            "Where do you see your career in 2-3 years?",
            "What would need to be true about a role for you to accept it?"
        ],
        "practical_questions": [
            "What are your salary expectations for this role?",
            "How do you feel about the commute to our office?",
            "What benefits are most important to you?",
            "How much notice would you need to give your current employer?"
        ],
        "probing_questions": [
            "What would make you turn down an offer?",
            "How flexible are you on salary if other benefits are strong?",
            "Have you interviewed elsewhere recently?",
            "What questions do you have about our company culture?"
        ]
    }
    
    return {
        **state,
        "tailored_interview_questions": interview_questions
    }