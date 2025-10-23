from langgraph.graph import StateGraph, END
from state import ProposalState
from nodes.extraction import extraction_node
from nodes.generation import generation_node
from nodes.validation import validation_node
from nodes.questions_only import questions_only_node
from nodes.calculator import calculator_node
from nodes.sanity_check import sanity_check_node


def create_graph():
    """Create the LangGraph workflow"""
    # Create the graph
    workflow = StateGraph(ProposalState)

    # Add the extraction node
    workflow.add_node("extraction", extraction_node)

    #Add the validaiton node
    workflow.add_node("validation", validation_node)

    # Add the Sanity Check Node
    workflow.add_node('sanity_check', sanity_check_node)

    # Add Calculator Node
    workflow.add_node("calculator", calculator_node)

    #Add the generation node
    workflow.add_node("generation", generation_node)

    #Add the conditional node
    workflow.add_node("questions_only", questions_only_node)

    # Set entry point
    workflow.set_entry_point("extraction")

    # Connect nodes
    workflow.add_edge("extraction", "validation")

    workflow.add_edge("validation", "sanity_check")

    #conditional routing based on the quality
    workflow.add_conditional_edges(
        "sanity_check", 
        route_after_validation,
        {
            "generation": "calculator",
            "questions_only" : "questions_only"
        }
    )


    workflow.add_edge("calculator", "generation")
    workflow.add_edge("generation", END)
    workflow.add_edge("questions_only", END)

    # Compile the graph
    return workflow.compile()


def route_after_validation(state: ProposalState) -> str:
    """
    Routing based on information quality. 
    Only generate the full proposal if we have enough information
    """
    if state['is_complete']:
        return "generation"
    else:
         return "questions_only"


def main():
    """MAIN function to trigger graphs"""
    # Create the graph
    graph = create_graph()

    # Test input
    test_input = {
        "user_input": """Need e-commerce site in 2 weeks""",
        "project_type": None,
        "deliverables": None,
        "timeline_hints": None,
        "budget_hints": None,
        "tech_hints": None,
        "is_complete": False,
        "missing_fields": None,
        "estimated_hours": None,
        "cost_range": None,
        "Proposal": None
    }


    



    # Run the graph
    print("Running proposal generator...")
    print(f"\nInput: {test_input['user_input']}")
    print("\n" + "="*60 + "\n")

    result = graph.invoke(test_input)

    # Print the output state
    print("Extraction Results:")
    print(f"Deliverables: {result['deliverables']}")
    print(f"Timeline Hints: {result['timeline_hints']}")
    print(f"Budget Hints: {result['budget_hints']}")
    print(f"Tech Hints: {result['tech_hints']}")
    print("\n" + "="*60)
    print(f"Proposal: {result['Proposal']}")


if __name__ == "__main__":
    main()
