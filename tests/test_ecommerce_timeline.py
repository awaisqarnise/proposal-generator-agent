#!/usr/bin/env python3
"""
Test the e-commerce timeline fix
"""
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
        'checkout'
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

print("Testing: E-commerce in 2 weeks")
print(f"User input: {state['user_input']}")
print(f"Timeline hints: {state['timeline_hints']}")
print(f"Deliverables: {len(state['deliverables'])}")
print()

result = sanity_check_node(state)
warnings = result.get('sanity_warnings')

if warnings:
    print(f"✅ SUCCESS! Detected {len(warnings)} warning(s):")
    for w in warnings:
        print(f"  - {w}")

    # Check if e-commerce specific warning was triggered
    ecommerce_specific = any('e-commerce/platform' in w.lower() for w in warnings)
    if ecommerce_specific:
        print("\n✅ E-commerce specific timeline check triggered!")
    else:
        print("\n⚠️ Only generic timeline warning (not e-commerce specific)")
else:
    print("❌ FAILED - NO WARNINGS")
