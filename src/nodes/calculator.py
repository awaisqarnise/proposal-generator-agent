from state import ProposalState
from tools.calculator import estimate_hours, calculate_timeline, estimate_cost


def calculator_node(state: ProposalState) -> ProposalState:
    """
    Calculate project estimates using calculator tools.

    Uses pure Python functions to estimate:
    - Total hours based on deliverables
    - Project timeline
    - Cost range

    Args:
        state: Current ProposalState with deliverables

    Returns:
        Updated ProposalState with estimated_hours, calculated_timeline, and cost_range
    """
    try:
        # Check if there's already an error in the state
        if state.get('error'):
            # Don't try to calculate if there's already an error
            return state

        deliverables = state.get('deliverables', [])
        project_type = state.get('project_type', 'custom')
        user_input = state.get('user_input', '')

        # Validate deliverables is a list
        if not isinstance(deliverables, list):
            error_msg = "Calculation Error: Invalid deliverables format"
            print(f"Error: {error_msg} - deliverables is type {type(deliverables)}")
            return {
                **state,
                'estimated_hours': None,
                'calculated_timeline': None,
                'cost_range': None,
                'error': f"{error_msg}\n\nThe project deliverables must be provided as a list. Please try again."
            }

        # If no deliverables, skip calculation but don't error (let validation handle it)
        if not deliverables or len(deliverables) == 0:
            print("Info: No deliverables provided for calculation - skipping")
            return {
                **state,
                'estimated_hours': None,
                'calculated_timeline': None,
                'cost_range': None
            }

        # Calculate total hours using the tool function with project type and user context
        total_hours = estimate_hours(deliverables, project_type, user_input)

        # Validate total hours
        if total_hours <= 0:
            print("Warning: Calculated hours is 0 or negative - using minimum estimate")
            return {
                **state,
                'estimated_hours': "40",  # Minimum 1 week estimate
                'calculated_timeline': "1-2 weeks (minimum estimate)",
                'cost_range': "$2,000-$8,000 (minimum estimate)"
            }

        # Calculate timeline using the tool function
        timeline = calculate_timeline(total_hours)

        # Calculate cost range using the tool function
        cost = estimate_cost(total_hours)

        # Update state with calculations
        return {
            **state,
            'estimated_hours': str(total_hours),
            'calculated_timeline': timeline,
            'cost_range': cost
        }

    except TypeError as e:
        error_msg = "Calculation Error: Invalid data type encountered"
        print(f"Error during calculation: {error_msg} - {str(e)}")
        return {
            **state,
            'estimated_hours': None,
            'calculated_timeline': None,
            'cost_range': None,
            'error': f"{error_msg}\n\nPlease ensure all project information is properly formatted. Details: {str(e)}"
        }

    except ValueError as e:
        error_msg = "Calculation Error: Invalid value encountered"
        print(f"Error during calculation: {error_msg} - {str(e)}")
        return {
            **state,
            'estimated_hours': None,
            'calculated_timeline': None,
            'cost_range': None,
            'error': f"{error_msg}\n\nPlease check your project deliverables. Details: {str(e)}"
        }

    except ZeroDivisionError as e:
        error_msg = "Calculation Error: Division by zero"
        print(f"Error during calculation: {error_msg} - {str(e)}")
        return {
            **state,
            'estimated_hours': None,
            'calculated_timeline': None,
            'cost_range': None,
            'error': f"{error_msg}\n\nAn internal calculation error occurred. Please try again."
        }

    except Exception as e:
        error_msg = f"Unexpected Calculation Error: {type(e).__name__}"
        print(f"Error during calculation: {error_msg} - {str(e)}")
        return {
            **state,
            'estimated_hours': None,
            'calculated_timeline': None,
            'cost_range': None,
            'error': f"{error_msg}\n\nUnable to calculate project estimates. Please try again with different input."
        }
