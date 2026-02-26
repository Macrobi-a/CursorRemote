import sys
from pathlib import Path
from typing import TypedDict, Dict, Any, Annotated
from langgraph.graph import StateGraph, START, END


def _merge_dict(left: dict | None, right: dict | None) -> dict:
    """Reducer: merge dicts so multiple nodes can update the same state key."""
    if left is None: return right or {}
    if right is None: return left or {}
    return {**left, **right}


def _merge_list(left: list | None, right: list | None) -> list:
    """Reducer: concatenate lists so multiple nodes can update the same state key."""
    if left is None: return list(right or [])
    if right is None: return list(left or [])
    return list(left) + list(right)


def _last_wins(left: Any, right: Any) -> Any:
    """Reducer: take the update (right) so multiple nodes can write to same key."""
    return right if right is not None else left

# Add output directory to path for agent imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import all available agents
from agents.agent_application_preparer import agent_application_preparer
from agents.agent_candidate_assessment import agent_candidate_assessment
from agents.agent_candidate_data_capture import agent_candidate_data_capture
from agents.agent_candidate_database_update import agent_candidate_database_update
from agents.agent_candidate_info_capture import agent_candidate_info_capture
from agents.agent_candidate_motivation_analysis import agent_candidate_motivation_analysis
from agents.agent_candidate_presentation import agent_candidate_presentation
from agents.agent_candidate_qualifier import agent_candidate_qualifier
from agents.agent_candidate_relationship_management import agent_candidate_relationship_management
from agents.agent_candidate_sourcer import agent_candidate_sourcer
from agents.agent_candidate_sourcing import agent_candidate_sourcing
from agents.agent_client_relationship_management import agent_client_relationship_management
from agents.agent_contract_generation import agent_contract_generation
from agents.agent_contact_info_lookup import agent_contact_info_lookup
from agents.agent_crm_manager import agent_crm_manager
from agents.agent_crm_update import agent_crm_update
from agents.agent_lead_generation import agent_lead_generation
from agents.agent_cv_screening import agent_cv_screening
from agents.agent_cv_submission import agent_cv_submission
from agents.agent_document_generation import agent_document_generation
from agents.agent_document_requester import agent_document_requester
from agents.agent_document_storage_and_tracking import agent_document_storage_and_tracking
from agents.agent_email_automation import agent_email_automation
from agents.agent_feedback_collector import agent_feedback_collector
from agents.agent_financing_company_interface import agent_financing_company_interface
from agents.agent_info_gatherer_linkedin import agent_info_gatherer_linkedin
from agents.agent_interview_questionnaire_prep import agent_interview_questionnaire_prep
from agents.agent_interview_scheduler import agent_interview_scheduler
from agents.agent_interview_scheduling import agent_interview_scheduling
from agents.agent_invoice_generation import agent_invoice_generation
from agents.agent_job_ad_creation import agent_job_ad_creation
from agents.agent_job_info_gathering import agent_job_info_gathering
from agents.agent_job_matching_engine import agent_job_matching_engine
from agents.agent_offer_analysis import agent_offer_analysis
from agents.agent_outreach_communicator import agent_outreach_communicator
from agents.agent_payroll_setup import agent_payroll_setup
from agents.agent_post_offer_followup import agent_post_offer_followup
from agents.agent_profit_tracking import agent_profit_tracking
from agents.agent_referral_requestor import agent_referral_requestor
from agents.agent_reporting import agent_reporting
from agents.agent_screening_scheduler import agent_screening_scheduler

# Define shared state (Annotated reducers allow multiple nodes to update same key per step)
class RecruitmentState(TypedDict, total=False):
    candidate_profile: Annotated[Dict[str, Any], _merge_dict]
    candidate_documents: Annotated[Dict[str, Any], _merge_dict]
    candidate_status: Annotated[str, _last_wins]
    candidate_notes: Annotated[str, _last_wins]
    client_requirements: Annotated[Dict[str, Any], _merge_dict]
    client_feedback: Annotated[str, _last_wins]
    job_matches: Annotated[list, _merge_list]
    current_step: Annotated[str, _last_wins]
    human_step_id: Annotated[str, _last_wins]
    next_human_node: Annotated[str, _last_wins]
    interview_details: Annotated[Dict[str, Any], _merge_dict]
    offer_details: Annotated[Dict[str, Any], _merge_dict]
    documents: Annotated[list, _merge_list]
    communications: Annotated[list, _merge_list]
    financial_data: Annotated[Dict[str, Any], _merge_dict]
    data: Annotated[Dict[str, Any], _merge_dict]

def human_in_the_loop(state: RecruitmentState) -> RecruitmentState:
    """Handle all human interactions based on the human_step_id or next_human_node"""
    
    human_step_id = state.get('human_step_id') or state.get('next_human_node') or ''
    
    # Define prompts for each human step
    human_prompts = {
        'human_initial_screening_call': 'Conduct initial screening call. Enter call notes and candidate assessment:',
        'human_legal_compliance_verification': 'Review compliance documents. Enter verification status (pass/fail):',
        'human_relationship_management': 'Handle relationship management. Enter interaction notes:',
        'human_client_submission_approval': 'Review candidate matches for client submission. Approve candidates (yes/no):',
        'human_interview_prep_debriefer': 'Conduct interview prep and debrief. Enter preparation and debrief notes:',
        'human_offer_negotiation': 'Handle offer negotiation. Enter final offer terms and acceptance status:',
        'human_resilience_manager': 'Manage resilience issues. Enter action plan:',
        'human_candidate_interview_preparation': 'Prepare candidate for interview. Enter preparation notes:',
        'human_client_meeting_or_call': 'Client meeting/call. Enter meeting outcomes and next steps:',
        'human_negotiation_and_offer_management': 'Handle negotiation and offers. Enter negotiation results:',
        'human_candidate_start_confirmation': 'Confirm candidate start date. Enter confirmed start date:',
        'human_client_management': 'Manage client relationship. Enter relationship notes:',
        'human_client_job_intake': 'Conduct client job intake. Enter job requirements:',
        'human_candidate_interview': 'Interview candidate. Enter interview assessment:',
        'human_client_temp_intake': 'Client temp staffing intake. Enter temp requirements:',
        'human_temp_onboarding_review': 'Review temp contract. Enter contract status:',
        'human_financing_company_selection': 'Select financing company. Enter company details:',
        'human_strategy_oversight': 'Strategic oversight review. Enter strategic decisions:',
        'human_client_relationship_management': 'Client relationship management. Enter client updates:',
        'human_candidate_pitch_to_client': 'Pitch candidate to client. Enter client response:',
        'human_client_interview_coordination': 'Coordinate client interviews. Enter interview schedule:',
        'human_candidate_follow_up': 'Follow up with candidate. Enter follow-up notes:',
        'human_candidate_closing': 'Close candidate. Enter closing outcome:',
        'human_troubleshooting': 'Handle troubleshooting. Enter resolution actions:',
        'human_strategic_business_setup_and_planning': 'Business setup and planning. Enter business parameters:',
        'human_client_candidate_relationship_management_and_negotiation': 'Handle client/candidate relationships. Enter outcomes:',
        'human_strategic_review_and_adjustment': 'Strategic review. Enter strategic adjustments:',
        'human_outbound_caller': 'Make outbound calls. Enter call outcomes:',
        'human_negotiation_and_details_gathering': 'Gather negotiation details. Enter details:',
        'human_credit_control_follow_up': 'Credit control follow-up. Enter actions taken:',
        'human_strategic_business_development': 'Strategic business development. Enter strategic decisions:',
        'human_rate_negotiation_client_communication': 'Rate negotiation. Enter agreed rates:',
        'human_payment_method_selection_onboarding': 'Payment method selection. Enter selected method:',
        'human_dispute_resolution_course_consultation': 'Dispute resolution. Enter resolution:',
        'human_initial_client_brief': 'Initial client brief. Enter client requirements:',
        'human_negotiation_client_terms': 'Negotiate client terms. Enter agreed terms:',
        'human_negotiation_candidate_package': 'Negotiate candidate package. Enter package details:',
        'human_timesheet_approval': 'Approve timesheet. Enter approval status:',
        'human_candidate_interview_deep_dive': 'Deep dive candidate interview. Enter detailed assessment:',
        'human_client_outreach_warm': 'Warm client outreach. Enter outreach results:',
        'human_client_negotiation_meeting': 'Client negotiation meeting. Enter meeting outcomes:',
        'human_strategic_decision_making': 'Strategic decision making. Enter strategic decisions:',
        'human_candidate_relationship_nurturing': 'Nurture candidate relationships. Enter relationship updates:',
        'human_client_consultation': 'Client consultation. Enter consultation outcomes:',
        'human_candidate_interview_and_qualification': 'Interview and qualify candidate. Enter qualification results:',
        'human_contract_finalization': 'Finalize contract. Enter contract status:'
    }
    
    prompt = human_prompts.get(human_step_id, f'Handle human step: {human_step_id}. Enter your input:')
    
    # When running in Chainlit (or any UI), use injected input instead of blocking on input()
    data = state.get("data") or {}
    human_input = (data.get("pending_human_input") or "").strip()
    if not human_input:
        print(f"\n=== HUMAN STEP: {human_step_id} ===")
        print(f"Current state data: {data}")
        print(f"Prompt: {prompt}")
        human_input = input("Your input (type 'done' or 'exit' to finish workflow): ").strip()
    
    # Update state with human input (return only changed keys to avoid LangGraph "one value per step" conflict)
    if 'data' not in state:
        state = {**state, 'data': {}}
    data = {**(state.get('data') or {}), f'{human_step_id or "human_step"}_input': human_input}
    if "pending_human_input" in data:
        del data["pending_human_input"]
    data["last_human_step_id"] = human_step_id or "human_step"
    if human_input.lower() in ("done", "exit", "quit"):
        data["_workflow_exit"] = True
    # After outbound caller, next human step is client job intake (so we have contact details first)
    if (human_step_id or "").strip() == "human_outbound_caller":
        data["next_human_node"] = "human_client_job_intake"
    state['data'] = data
    state['current_step'] = human_step_id or 'human_step'

    return {
        "data": state["data"],
        "current_step": state["current_step"],
        "human_step_id": "",
        "next_human_node": state.get("data", {}).get("next_human_node", ""),
    }


def _human_routes_to(state: dict) -> str:
    """Route from human_in_the_loop: end, or next step (client job intake, then job gathering, else default)."""
    if state.get("data", {}).get("_workflow_exit"):
        return "end"
    last = state.get("data", {}).get("last_human_step_id", "")
    if last == "human_outbound_caller":
        return "human_again"  # re-enter human for human_client_job_intake (has contact details now)
    if last == "human_client_job_intake":
        return "client_job"  # then agent_job_info_gathering
    return "continue"

# Create the graph
builder = StateGraph(RecruitmentState)

# Add all agent nodes (client-acquisition path first so job intake has contact details)
builder.add_node("agent_lead_generation", agent_lead_generation)
builder.add_node("agent_contact_info_lookup", agent_contact_info_lookup)
builder.add_node("agent_candidate_data_capture", agent_candidate_data_capture)
builder.add_node("agent_screening_scheduler", agent_screening_scheduler)
builder.add_node("agent_document_requester", agent_document_requester)
builder.add_node("agent_document_storage_and_tracking", agent_document_storage_and_tracking)
builder.add_node("agent_candidate_database_update", agent_candidate_database_update)
builder.add_node("agent_job_matching_engine", agent_job_matching_engine)
builder.add_node("agent_application_preparer", agent_application_preparer)
builder.add_node("agent_feedback_collector", agent_feedback_collector)
builder.add_node("agent_reporting", agent_reporting)
builder.add_node("agent_candidate_sourcer", agent_candidate_sourcer)
builder.add_node("agent_candidate_qualifier", agent_candidate_qualifier)
builder.add_node("agent_outreach_communicator", agent_outreach_communicator)
builder.add_node("agent_cv_submission", agent_cv_submission)
builder.add_node("agent_interview_scheduler", agent_interview_scheduler)
builder.add_node("agent_crm_manager", agent_crm_manager)
builder.add_node("agent_referral_requestor", agent_referral_requestor)
builder.add_node("agent_info_gatherer_linkedin", agent_info_gatherer_linkedin)
builder.add_node("agent_job_info_gathering", agent_job_info_gathering)
builder.add_node("agent_candidate_sourcing", agent_candidate_sourcing)
builder.add_node("agent_interview_questionnaire_prep", agent_interview_questionnaire_prep)
builder.add_node("agent_candidate_assessment", agent_candidate_assessment)
builder.add_node("agent_candidate_motivation_analysis", agent_candidate_motivation_analysis)
builder.add_node("agent_candidate_presentation", agent_candidate_presentation)
builder.add_node("agent_interview_scheduling", agent_interview_scheduling)
builder.add_node("agent_offer_analysis", agent_offer_analysis)
builder.add_node("agent_post_offer_followup", agent_post_offer_followup)
builder.add_node("agent_contract_generation", agent_contract_generation)
builder.add_node("agent_payroll_setup", agent_payroll_setup)
builder.add_node("agent_invoice_generation", agent_invoice_generation)
builder.add_node("agent_financing_company_interface", agent_financing_company_interface)
builder.add_node("agent_profit_tracking", agent_profit_tracking)
builder.add_node("agent_candidate_relationship_management", agent_candidate_relationship_management)
builder.add_node("agent_client_relationship_management", agent_client_relationship_management)
builder.add_node("agent_job_ad_creation", agent_job_ad_creation)
builder.add_node("agent_cv_screening", agent_cv_screening)
builder.add_node("agent_candidate_info_capture", agent_candidate_info_capture)
builder.add_node("agent_document_generation", agent_document_generation)
builder.add_node("agent_email_automation", agent_email_automation)
builder.add_node("agent_crm_update", agent_crm_update)

# Add human interaction node
builder.add_node("human_in_the_loop", human_in_the_loop)

# Add edges from graph entry: client path first (lead -> contact lookup -> human outbound -> human job intake -> job gathering)
builder.add_edge(START, "agent_lead_generation")
builder.add_edge("agent_lead_generation", "agent_contact_info_lookup")
builder.add_edge("agent_contact_info_lookup", "human_in_the_loop")  # human_outbound_caller (state has next_human_node set)

# Candidate path (runs in parallel from START if we ever branch; for now client path is first)
builder.add_edge(START, "agent_candidate_data_capture")

# Add agent-to-agent edges
builder.add_edge("agent_candidate_data_capture", "agent_screening_scheduler")
builder.add_edge("agent_screening_scheduler", "human_in_the_loop")  # to human_initial_screening_call
builder.add_edge("agent_candidate_database_update", "agent_document_requester")
builder.add_edge("agent_document_requester", "agent_document_storage_and_tracking")
builder.add_edge("agent_document_storage_and_tracking", "human_in_the_loop")  # to human_legal_compliance_verification
builder.add_edge("agent_candidate_database_update", "agent_job_matching_engine")
builder.add_edge("agent_job_matching_engine", "human_in_the_loop")  # to human_client_submission_approval
builder.add_edge("agent_application_preparer", "human_in_the_loop")  # to human_interview_prep_debriefer
builder.add_edge("agent_feedback_collector", "human_in_the_loop")  # to human_offer_negotiation
builder.add_edge("agent_candidate_sourcer", "agent_candidate_qualifier")
builder.add_edge("agent_candidate_sourcer", "agent_info_gatherer_linkedin")
builder.add_edge("agent_info_gatherer_linkedin", "agent_candidate_qualifier")
builder.add_edge("agent_candidate_qualifier", "agent_outreach_communicator")
builder.add_edge("agent_outreach_communicator", "human_in_the_loop")  # to human_candidate_interview_preparation
builder.add_edge("agent_cv_submission", "human_in_the_loop")  # to human_client_meeting_or_call
builder.add_edge("agent_interview_scheduler", "human_in_the_loop")  # to human_client_meeting_or_call
builder.add_edge("agent_crm_manager", "human_in_the_loop")  # to human_client_management
builder.add_edge("agent_job_info_gathering", "agent_candidate_sourcing")
builder.add_edge("agent_candidate_sourcing", "agent_interview_questionnaire_prep")
builder.add_edge("agent_interview_questionnaire_prep", "human_in_the_loop")  # to human_candidate_interview
builder.add_edge("agent_candidate_assessment", "agent_candidate_motivation_analysis")
builder.add_edge("agent_candidate_motivation_analysis", "agent_candidate_presentation")
builder.add_edge("agent_candidate_presentation", "agent_interview_scheduling")
builder.add_edge("agent_interview_scheduling", "human_in_the_loop")  # to human_offer_negotiation
builder.add_edge("agent_offer_analysis", "agent_post_offer_followup")
builder.add_edge("agent_post_offer_followup", "agent_candidate_relationship_management")
builder.add_edge("agent_contract_generation", "human_in_the_loop")  # to human_temp_onboarding_review
builder.add_edge("agent_payroll_setup", "agent_invoice_generation")
builder.add_edge("agent_invoice_generation", "agent_financing_company_interface")
builder.add_edge("agent_financing_company_interface", "agent_profit_tracking")
builder.add_edge("agent_profit_tracking", "human_in_the_loop")  # to human_strategy_oversight
builder.add_edge("agent_job_ad_creation", "agent_candidate_sourcing")
builder.add_edge("agent_cv_screening", "human_in_the_loop")  # to human_candidate_interview
builder.add_edge("agent_candidate_info_capture", "agent_crm_update")
builder.add_edge("agent_document_generation", "agent_email_automation")
builder.add_edge("agent_email_automation", "human_in_the_loop")  # to human_candidate_follow_up

# Conditional edge from human: end, or human_again (client job intake), or client_job (job gathering), or continue (default)
builder.add_conditional_edges(
    "human_in_the_loop",
    _human_routes_to,
    {
        "end": END,
        "human_again": "human_in_the_loop",
        "client_job": "agent_job_info_gathering",
        "continue": "agent_candidate_database_update",
    },
)
builder.add_edge("agent_reporting", END)

# Compile the graph (CLI: no checkpointer)
graph = builder.compile()


def get_graph_for_chainlit(checkpointer=None):
    """
    Compile the same graph with a checkpointer and interrupt before human steps.
    Use in Chainlit so (1) state persists across reloads, (2) graph pauses for human input in the UI.
    """
    if checkpointer is None:
        try:
            import sqlite3
            import tempfile
            from langgraph.checkpoint.sqlite import SqliteSaver
            db = str(Path(tempfile.gettempdir()) / "recruitment_checkpoints.sqlite")
            conn = sqlite3.connect(db, check_same_thread=False)
            checkpointer = SqliteSaver(conn)
        except Exception:
            from langgraph.checkpoint.memory import MemorySaver
            checkpointer = MemorySaver()
    return builder.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_in_the_loop"],
    )

if __name__ == "__main__":
    # Initialize the state
    initial_state = RecruitmentState(
        candidate_profile={},
        candidate_documents={},
        candidate_status="new",
        candidate_notes="",
        client_requirements={},
        client_feedback="",
        job_matches=[],
        current_step="start",
        human_step_id="",
        next_human_node="",
        interview_details={},
        offer_details={},
        documents=[],
        communications=[],
        financial_data={},
        data={"initial_input": "Starting recruitment process"}
    )
    
    print("Starting recruitment workflow...")
    print("=" * 50)
    
    # Run the graph
    try:
        result = graph.invoke(initial_state)
        print("\n" + "=" * 50)
        print("WORKFLOW COMPLETED")
        print("Final state:")
        for key, value in result.items():
            if key != 'data' or len(str(value)) < 200:
                print(f"{key}: {value}")
    except Exception as e:
        print(f"\nWorkflow error: {e}")
        print("This is expected as the workflow requires human interaction.")