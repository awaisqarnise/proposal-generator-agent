from state import ProposalState


def questions_only_node(state: ProposalState) -> ProposalState:
    """
    Outputs only clarifying questions, no proposal.

    Used when information quality is too low to generate a meaningful proposal.

    Args:
        state: Current ProposalState with clarifying_questions

    Returns:
        Updated ProposalState with Proposal field containing only questions
    """
    try:
        questions = state.get('clarifying_questions', [])

        # Validate questions is a list
        if not isinstance(questions, list):
            questions = []
            print("Warning: clarifying_questions is not a list")

        if questions and len(questions) > 0:
            output = f"""# Insufficient Information to Generate Proposal

To create an accurate proposal, I need more details:

{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(questions))}

Please provide this information and I'll generate a comprehensive proposal."""
        else:
            output = "# Unable to Generate Proposal\n\nPlease provide more information about your project requirements."

        return {
            **state,
            'Proposal': output
        }

    except Exception as e:
        error_msg = f"Questions generation failed: {str(e)}"
        print(f"Error in questions_only_node: {error_msg}")
        return {
            **state,
            'Proposal': f"❌ Error: {error_msg}\n\nUnable to generate clarifying questions. Please provide detailed project requirements."
        }
