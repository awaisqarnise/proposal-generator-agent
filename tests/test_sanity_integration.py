#!/usr/bin/env python3
"""
Example showing how sanity_check_node integrates with the proposal flow
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nodes.sanity_check import sanity_check_node
from state import ProposalState


def simulate_proposal_flow():
    """Simulate a proposal generation flow with sanity check"""

    print("="*70)
    print("SIMULATED PROPOSAL FLOW WITH SANITY CHECK")
    print("="*70)

    # Step 1: Extraction (simulated)
    print("\n1. EXTRACTION NODE")
    print("   Extracting project requirements...")
    state: ProposalState = {
        'user_input': 'Build an e-commerce platform using jQuery and Flash for animations',
        'project_type': 'E-commerce',
        'industry': 'Retail',
        'deliverables': [
            'Product catalog',
            'Shopping cart',
            'Payment integration',
            'User authentication',
            'Admin dashboard',
            'Order management',
            'Inventory system',
            'Email notifications',
            'Search functionality',
            'Customer reviews',
            'Wishlist feature',
            'Analytics dashboard'
        ],
        'timeline_hints': '2 months',
        'budget_hints': '$25,000',
        'tech_hints': ['jQuery', 'Flash', 'PHP 5', 'MySQL'],
        'is_complete': True,
        'missing_fields': None,
        'clarifying_questions': None,
        'information_quality': 'high',
        'estimated_hours': None,
        'cost_range': None,
        'calculated_timeline': None,
        'sanity_warnings': None,
        'Proposal': None,
        'error': None
    }
    print("   ✓ Extracted 12 deliverables")

    # Step 2: Validation (simulated)
    print("\n2. VALIDATION NODE")
    print("   Validating completeness...")
    print("   ✓ All required fields present")

    # Step 3: Calculator (simulated)
    print("\n3. CALCULATOR NODE")
    print("   Calculating costs and timeline...")
    state['estimated_hours'] = '1200'
    state['cost_range'] = '$96,000 - $144,000'
    state['calculated_timeline'] = '7.5 months'
    print(f"   ✓ Estimated hours: {state['estimated_hours']}")
    print(f"   ✓ Cost range: {state['cost_range']}")
    print(f"   ✓ Timeline: {state['calculated_timeline']}")

    # Step 4: SANITY CHECK (our new node!)
    print("\n4. SANITY CHECK NODE")
    state = sanity_check_node(state)

    # Step 5: Handle warnings
    warnings = state.get('sanity_warnings')
    if warnings:
        print("\n" + "="*70)
        print("⚠️  SANITY CHECK RESULTS")
        print("="*70)
        print(f"\nFound {len(warnings)} potential issue(s):\n")
        for i, warning in enumerate(warnings, 1):
            print(f"{i}. {warning}\n")

        print("\n" + "="*70)
        print("RECOMMENDATION")
        print("="*70)
        print("These warnings should be:")
        print("- Included in the proposal as 'Assumptions & Risks' section")
        print("- Discussed with the client before finalizing")
        print("- Used to adjust scope, budget, or timeline")
        print("="*70)
    else:
        print("\n✓ No issues detected - proposal looks good!")

    # Step 6: Generation (simulated)
    print("\n5. GENERATION NODE")
    print("   Generating proposal with warnings included...")
    print("   ✓ Proposal generated")

    return state


def show_how_to_use_in_generation():
    """Show how to incorporate warnings into proposal"""

    print("\n\n" + "="*70)
    print("HOW TO USE WARNINGS IN PROPOSAL GENERATION")
    print("="*70)

    example_template = '''
# Project Proposal

## Executive Summary
[Your proposal content...]

## Scope of Work
[Deliverables list...]

## Timeline & Budget
- Estimated Timeline: {calculated_timeline}
- Budget Range: {cost_range}

## ⚠️ Important Considerations

{warnings_section}

We recommend addressing these points before proceeding with the project
to ensure realistic expectations and successful delivery.

## Next Steps
[Next steps...]
'''

    print("\nProposal template with warnings:")
    print(example_template)

    print("\nCode example:")
    code_example = '''
def generation_node(state: ProposalState) -> ProposalState:
    warnings = state.get('sanity_warnings')

    # Build warnings section
    warnings_section = ""
    if warnings:
        warnings_section = "Based on our analysis, please note:\\n\\n"
        for warning in warnings:
            # Remove emoji and format nicely
            clean_warning = warning.replace("⚠️", "").strip()
            warnings_section += f"- {clean_warning}\\n"

    # Include in prompt
    prompt = f"""
    Generate a proposal with these warnings:
    {warnings_section}
    """

    # ... rest of generation logic
'''
    print(code_example)


if __name__ == "__main__":
    # Run simulation
    final_state = simulate_proposal_flow()

    # Show integration example
    show_how_to_use_in_generation()

    print("\n" + "="*70)
    print("✓ Sanity check integration demonstration complete!")
    print("="*70)
