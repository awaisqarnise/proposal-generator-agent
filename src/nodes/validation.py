from state import ProposalState
from typing import List


def validation_node(state: ProposalState) -> ProposalState:
    """
    Validate if the user input makes enough sense to create a proposal.

    Now focuses on INPUT CLARITY rather than information completeness:
    - If input is clear enough (has project_type and deliverables), proceed with proposal
    - If input is too vague (no project_type or no deliverables), ask clarifying questions
    - Missing budget/timeline/tech are now INFERRED in extraction, not asked here

    Quality levels:
    - HIGH: Clear project_type AND 3+ deliverables (ready for proposal)
    - MEDIUM: Clear project_type AND 1-2 deliverables (acceptable for proposal with assumptions)
    - LOW: No project_type OR no deliverables (too vague, need clarification)

    Args:
        state: Current ProposalState with extracted information

    Returns:
        Updated ProposalState with information_quality, is_complete, missing_fields,
        and clarifying_questions populated
    """
    try:
        # Check if there's already an error in the state
        if state.get('error'):
            # Don't validate if there's already an error, just pass through
            return {
                **state,
                'information_quality': 'low',
                'is_complete': False,
                'missing_fields': None,
                'clarifying_questions': None
            }

        project_type = state.get('project_type')
        deliverables = state.get('deliverables', [])
        industry = state.get('industry')

        # Validate deliverables is a list
        if not isinstance(deliverables, list):
            error_msg = "Validation Error: Invalid deliverables format"
            print(f"Error: {error_msg} - deliverables is type {type(deliverables)}")
            deliverables = []
            # Continue with empty list instead of failing

        # Count deliverables
        deliverables_count = len(deliverables) if deliverables else 0

        # Check if we have minimum clarity (project type and at least some deliverables)
        has_project_type = bool(project_type)
        has_deliverables = deliverables_count > 0

        # Determine information quality based on CLARITY, not completeness
        if has_project_type and deliverables_count >= 3:
            quality = 'high'
        elif has_project_type and deliverables_count >= 1:
            quality = 'medium'
        else:
            quality = 'low'

        # Generate clarifying questions ONLY if input doesn't make sense
        missing: List[str] = []
        questions: List[str] = []

        # Only ask questions if the input is too vague to understand
        if not has_project_type or not has_deliverables:
            if not has_project_type:
                missing.append('project_type')
                questions.append("What type of project are you looking to build? (e.g., mobile app, website, e-commerce platform, etc.)")

            if not has_deliverables:
                missing.append('deliverables')
                questions.append("Could you describe what you want this project to do? What are the main features or functionalities?")

            # If it's extremely vague, ask for more context
            if not industry and not has_project_type:
                questions.append("What industry or domain is this for? This will help us understand your needs better.")

        # Mark as complete if we have enough clarity (HIGH or MEDIUM quality)
        # LOW quality means we need more information
        is_complete = (quality in ['high', 'medium'])

        # Update state with validation results
        return {
            **state,
            'information_quality': quality,
            'is_complete': is_complete,
            'missing_fields': missing if missing else None,
            'clarifying_questions': questions if questions else None
        }

    except KeyError as e:
        error_msg = f"Validation Error: Missing required state field - {str(e)}"
        print(f"Error during validation: {error_msg}")
        return {
            **state,
            'information_quality': 'low',
            'is_complete': False,
            'missing_fields': ['project_type', 'deliverables'],
            'clarifying_questions': ["Unable to validate input due to missing data. Please provide project details."],
            'error': f"{error_msg}\n\nThe state is missing required fields. Please ensure all extraction steps completed successfully."
        }

    except TypeError as e:
        error_msg = f"Validation Error: Invalid data type - {str(e)}"
        print(f"Error during validation: {error_msg}")
        return {
            **state,
            'information_quality': 'low',
            'is_complete': False,
            'missing_fields': None,
            'clarifying_questions': None,
            'error': f"{error_msg}\n\nThere was a problem with the data format. Please try again."
        }

    except Exception as e:
        error_msg = f"Unexpected Validation Error: {type(e).__name__}"
        print(f"Error during validation: {error_msg} - {str(e)}")
        return {
            **state,
            'information_quality': 'low',
            'is_complete': False,
            'missing_fields': ['project_type', 'deliverables'],
            'clarifying_questions': ["Unable to validate input. Please provide project details."],
            'error': f"{error_msg}\n\nAn unexpected error occurred during validation. Details: {str(e)}"
        }
