import sys
sys.path.append('src')

from state import ProposalState
from nodes.extraction import extraction_node
from dotenv import load_dotenv

load_dotenv()

# Test case 1: Rich input
test_state_1 = ProposalState(
    user_input="Build a mobile app for restaurant ordering with online payments and delivery tracking. Need it in 3 months, budget is $50k. Use React Native.",
    deliverables=None,
    timeline_hints=None,
    budget_hints=None,
    tech_hints=None,
    is_complete=False,
    missing_fields=None,
    estimated_hours=None,
    cost_range=None,
    Proposal=None
)

print("Testing extraction with rich input...")
result_1 = extraction_node(test_state_1)
print(f"\nDeliverables: {result_1['deliverables']}")
print(f"Timeline: {result_1['timeline_hints']}")
print(f"Budget: {result_1['budget_hints']}")
print(f"Tech: {result_1['tech_hints']}")

print("\n" + "="*50 + "\n")

# Test case 2: Minimal input
test_state_2 = ProposalState(
    user_input="Need a simple website",
    deliverables=None,
    timeline_hints=None,
    budget_hints=None,
    tech_hints=None,
    is_complete=False,
    missing_fields=None,
    estimated_hours=None,
    cost_range=None,
    Proposal=None
)

print("Testing extraction with minimal input...")
result_2 = extraction_node(test_state_2)
print(f"\nDeliverables: {result_2['deliverables']}")
print(f"Timeline: {result_2['timeline_hints']}")
print(f"Budget: {result_2['budget_hints']}")
print(f"Tech: {result_2['tech_hints']}")