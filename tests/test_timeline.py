import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nodes.sanity_check import sanity_check_node

state = {
    'user_input': 'Need e-commerce site in 2 weeks',
    'project_type': 'E-commerce',
    'industry': None,
    'deliverables': [
        'product catalog',
        'shopping cart',
        'checkout',
        'payment integration',
        'user accounts'
    ],
    'timeline_hints': '2 weeks',
    'budget_hints': None,
    'tech_hints': None,
    'is_complete': True,
    'missing_fields': None,
    'clarifying_questions': None,
    'information_quality': 'high',
    'estimated_hours': None,  # Not calculated yet
    'cost_range': None,
    'calculated_timeline': None,
    'sanity_warnings': None,
    'Proposal': None,
    'error': None
}

print("Testing: E-commerce in 2 weeks with 5 deliverables")
print("Timeline hints:", state['timeline_hints'])
print("Deliverables:", len(state['deliverables']))
print()

result = sanity_check_node(state)
warnings = result.get('sanity_warnings')

if warnings:
    print(f"✅ Detected {len(warnings)} warning(s):")
    for w in warnings:
        print(f"  - {w}")
else:
    print("❌ NO WARNINGS - This should have been flagged!")
