#!/usr/bin/env python3
"""
Test sanity check node with various scenarios
"""
import sys
import os

# Add src to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nodes.sanity_check import sanity_check_node
from state import ProposalState


def create_test_state(**kwargs) -> ProposalState:
    """Create a test state with default values"""
    base_state = {
        'user_input': '',
        'project_type': None,
        'industry': None,
        'deliverables': None,
        'timeline_hints': None,
        'budget_hints': None,
        'tech_hints': None,
        'is_complete': False,
        'missing_fields': None,
        'clarifying_questions': None,
        'information_quality': None,
        'estimated_hours': None,
        'cost_range': None,
        'calculated_timeline': None,
        'sanity_warnings': None,
        'Proposal': None,
        'error': None
    }
    base_state.update(kwargs)
    return base_state


def test_scenario(name: str, state: ProposalState):
    """Test a scenario and print results"""
    print("\n" + "="*70)
    print(f"TEST: {name}")
    print("="*70)
    print(f"Deliverables: {len(state.get('deliverables', []))} items")
    print(f"Budget: {state.get('budget_hints') or state.get('cost_range')}")
    print(f"Hours: {state.get('estimated_hours')}")
    print(f"Timeline: {state.get('timeline_hints') or state.get('calculated_timeline')}")
    print(f"Tech: {state.get('tech_hints')}")
    print()

    result = sanity_check_node(state)

    warnings = result.get('sanity_warnings')
    if warnings:
        print(f"\nWarnings found: {len(warnings)}")
    else:
        print("\nNo warnings")

    return result


print("="*70)
print("SANITY CHECK TESTS")
print("="*70)

# Test 1: Budget too high for few deliverables
test_scenario(
    "Budget Too High - 2 deliverables with $100k budget",
    create_test_state(
        deliverables=['Login page', 'Contact form'],
        budget_hints='$100,000',
        estimated_hours='100'
    )
)

# Test 2: Budget too low for many deliverables
test_scenario(
    "Budget Too Low - 12 deliverables with $25k budget",
    create_test_state(
        deliverables=[
            'User auth', 'Dashboard', 'Analytics', 'Reporting',
            'Payment integration', 'Email system', 'Admin panel',
            'Search', 'Notifications', 'File upload', 'API', 'CMS'
        ],
        budget_hints='$25,000',
        estimated_hours='1200'
    )
)

# Test 3: Budget-hours mismatch (hours suggest higher budget)
test_scenario(
    "Budget-Hours Mismatch - 1000 hours but only $30k budget",
    create_test_state(
        deliverables=['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4', 'Feature 5'],
        budget_hints='$30,000',
        estimated_hours='1000'
    )
)

# Test 4: Budget-hours mismatch (budget too high for hours)
test_scenario(
    "Budget-Hours Mismatch - 100 hours but $150k budget",
    create_test_state(
        deliverables=['Simple feature', 'Basic UI'],
        budget_hints='$150,000',
        estimated_hours='100'
    )
)

# Test 5: Timeline too aggressive
test_scenario(
    "Timeline Too Aggressive - 1000 hours in 4 weeks",
    create_test_state(
        deliverables=['Complex system 1', 'Complex system 2', 'Complex system 3'],
        estimated_hours='1000',
        timeline_hints='4 weeks',
        budget_hints='$80,000-$120,000'
    )
)

# Test 6: Timeline too long
test_scenario(
    "Timeline Too Long - 150 hours over 8 months",
    create_test_state(
        deliverables=['Simple feature 1', 'Simple feature 2'],
        estimated_hours='150',
        timeline_hints='8 months',
        budget_hints='$12,000-$18,000'
    )
)

# Test 7: Outdated tech - Flash
test_scenario(
    "Outdated Tech - Flash",
    create_test_state(
        deliverables=['Interactive animation', 'Video player'],
        tech_hints=['Flash', 'ActionScript', 'HTML'],
        estimated_hours='200'
    )
)

# Test 8: Outdated tech - jQuery
test_scenario(
    "Outdated Tech - jQuery with old versions",
    create_test_state(
        deliverables=['Interactive UI', 'Form validation'],
        tech_hints=['jQuery', 'PHP 5', 'MySQL 5.5'],
        user_input='Build a web app using jQuery and PHP 5',
        estimated_hours='300'
    )
)

# Test 9: Conflicting frameworks - React and Angular
test_scenario(
    "Conflicting Frameworks - React + Angular",
    create_test_state(
        deliverables=['Frontend app', 'Admin dashboard', 'API'],
        tech_hints=['React', 'Angular', 'Node.js'],
        user_input='We want to use React for the main app and Angular for the admin panel',
        estimated_hours='600'
    )
)

# Test 10: Multiple issues
test_scenario(
    "Multiple Issues - Budget low + Timeline aggressive + Outdated tech",
    create_test_state(
        deliverables=[
            'User auth', 'Dashboard', 'Analytics', 'Reporting',
            'Payment', 'Email', 'Admin', 'Search', 'Notifications',
            'Upload', 'API', 'CMS'
        ],
        budget_hints='$20,000',
        estimated_hours='1200',
        timeline_hints='2 months',
        tech_hints=['jQuery', 'AngularJS', 'Backbone', 'PHP 5'],
        user_input='Legacy system using jQuery and AngularJS'
    )
)

# Test 11: Everything looks good
test_scenario(
    "Everything Looks Good - Reasonable project",
    create_test_state(
        deliverables=[
            'User authentication',
            'Dashboard',
            'API integration',
            'Reporting',
            'Admin panel'
        ],
        budget_hints='$50,000-$75,000',
        estimated_hours='500',
        calculated_timeline='3.1 months',
        tech_hints=['React', 'Node.js', 'PostgreSQL', 'TypeScript']
    )
)

# Test 12: Enterprise project with context
test_scenario(
    "Enterprise Project - High budget, many deliverables, modern tech",
    create_test_state(
        deliverables=[
            'ERP core system',
            'Accounting module',
            'HR and payroll',
            'Inventory management',
            'Reporting dashboard',
            'Multi-tenant architecture',
            'Compliance logging',
            'API gateway'
        ],
        budget_hints='$200,000-$300,000',
        estimated_hours='2000',
        calculated_timeline='12.5 months',
        tech_hints=['React', 'Node.js', 'PostgreSQL', 'TypeScript', 'AWS', 'Docker'],
        user_input='Enterprise ERP system with GDPR compliance'
    )
)

# Test 13: Python 2 warning
test_scenario(
    "Deprecated Python 2",
    create_test_state(
        deliverables=['API backend', 'Data processing'],
        tech_hints=['Python 2.7', 'Django'],
        user_input='Backend using Python 2',
        estimated_hours='400'
    )
)

# Test 14: Old Node.js version
test_scenario(
    "Old Node.js Version",
    create_test_state(
        deliverables=['REST API', 'WebSocket server'],
        tech_hints=['Node.js 8', 'Express'],
        user_input='Build API with Node 8',
        estimated_hours='300'
    )
)

# Test 15: Budget from cost_range instead of budget_hints
test_scenario(
    "Budget from cost_range - Too low for scope",
    create_test_state(
        deliverables=[
            'Feature 1', 'Feature 2', 'Feature 3', 'Feature 4',
            'Feature 5', 'Feature 6', 'Feature 7', 'Feature 8',
            'Feature 9', 'Feature 10', 'Feature 11', 'Feature 12'
        ],
        cost_range='$25,000 - $35,000',
        estimated_hours='1200'
    )
)

print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)
print("✓ Budget-scope mismatch detection: TESTED")
print("✓ Timeline reality checks: TESTED")
print("✓ Tech stack issues (outdated tech): TESTED")
print("✓ Tech stack issues (conflicting frameworks): TESTED")
print("✓ Multiple issues in one project: TESTED")
print("✓ Valid project (no warnings): TESTED")
print("="*70)
