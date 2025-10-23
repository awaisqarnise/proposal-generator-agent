from typing import TypedDict, List, Optional

class ProposalState(TypedDict):
    """State that flows through the proposal generator agent"""

    
    #input
    user_input: str

    #extracted info
    project_type: Optional[str]
    industry: Optional[str]
    deliverables: Optional[List[str]]
    timeline_hints: Optional[str]
    budget_hints: Optional[str]
    tech_hints: Optional[List[str]]

    #validations
    is_complete: bool
    missing_fields: Optional[List[str]]
    clarifying_questions: Optional[List[str]]
    information_quality: Optional[str]  # 'high', 'medium', or 'low'

    #calcualtions
    estimated_hours: Optional[str]
    cost_range: Optional[str]
    calculated_timeline: Optional[str]

    #sanity checks
    sanity_warnings: Optional[List[str]]

    #output
    Proposal: Optional[str]
    error: Optional[str]  # Error messages for graceful failure handling