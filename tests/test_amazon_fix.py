#!/usr/bin/env python3
"""
Test the fix for "like Amazon" with $5k budget
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nodes.sanity_check import sanity_check_node
from state import ProposalState


print("="*70)
print("TESTING FIX: Amazon-like platform with $5k budget")
print("="*70)

# Simulate the state after extraction
state: ProposalState = {
    'user_input': 'Full e-commerce platform like Amazon with $5k budget',
    'project_type': 'E-commerce',
    'industry': None,
    'deliverables': [
        'product catalog',
        'shopping cart',
        'checkout',
        'payment integration',
        'user accounts',
        'order tracking',
        'admin dashboard'
    ],
    'timeline_hints': None,
    'budget_hints': '$5,000',
    'tech_hints': None,
    'is_complete': True,
    'missing_fields': None,
    'clarifying_questions': None,
    'information_quality': 'high',
    'estimated_hours': None,  # Not calculated yet (sanity check runs before calculator)
    'cost_range': None,
    'calculated_timeline': None,
    'sanity_warnings': None,
    'Proposal': None,
    'error': None
}

print("\nInput Details:")
print(f"  User Input: {state['user_input']}")
print(f"  Budget: {state['budget_hints']}")
print(f"  Deliverables: {len(state['deliverables'])} features")
print()

# Run sanity check
result = sanity_check_node(state)

warnings = result.get('sanity_warnings')

print("\n" + "="*70)
print("RESULTS")
print("="*70)

if warnings:
    print(f"\n✅ FIXED! Detected {len(warnings)} critical issue(s):\n")
    for i, warning in enumerate(warnings, 1):
        print(f"{i}. {warning}\n")
else:
    print("\n❌ PROBLEM! No warnings detected - should have flagged this!\n")

print("="*70)
print("\nExpected Warnings:")
print("1. Scope Warning: Amazon-scale requires $500M-$1B+")
print("2. Budget Warning: $5k / 7 deliverables = $714 each (too low)")
print("3. Budget Warning: $5k is extremely low for any software project")
print("="*70)
