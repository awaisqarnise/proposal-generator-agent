#!/usr/bin/env python3
"""
Automated Test Suite for Proposal Generator
Tests all major scenarios and validates expected behaviors
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import create_graph
from typing import Dict, List, Tuple
import re


class TestCase:
    def __init__(self, test_num: int, name: str, input_text: str, expected: Dict):
        self.test_num = test_num
        self.name = name
        self.input_text = input_text
        self.expected = expected
        self.result = None
        self.passed = False
        self.failures = []
        self.successes = []


def extract_cost_from_range(cost_range: str) -> Tuple[float, float]:
    """Extract min and max from cost range string like '$50,000 - $70,000'"""
    if not cost_range:
        return (0, 0)

    # Remove $ and commas, extract numbers
    numbers = re.findall(r'[\d,]+', cost_range)
    if len(numbers) >= 2:
        min_cost = float(numbers[0].replace(',', ''))
        max_cost = float(numbers[1].replace(',', ''))
        return (min_cost, max_cost)
    return (0, 0)


def check_cost_range(actual: str, expected_min: float, expected_max: float) -> bool:
    """Check if actual cost range overlaps with expected range"""
    if not actual:
        return False

    actual_min, actual_max = extract_cost_from_range(actual)

    # Check if ranges overlap
    return not (actual_max < expected_min or actual_min > expected_max)


def run_test(test: TestCase, graph) -> TestCase:
    """Run a single test case"""
    print(f"\nTEST {test.test_num}: {test.name}")
    print(f"Input: \"{test.input_text[:80]}{'...' if len(test.input_text) > 80 else ''}\"")
    print("-" * 70)

    # Create test input
    test_input = {
        "user_input": test.input_text,
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

    try:
        # Run the graph
        result = graph.invoke(test_input)
        test.result = result

        # Check expected behaviors
        expectations = test.expected

        # Check project_type
        if 'project_type' in expectations:
            expected_type = expectations['project_type']
            actual_type = result.get('project_type')
            if expected_type.lower() in (actual_type or '').lower():
                test.successes.append(f"✓ Project type: {actual_type}")
            else:
                test.failures.append(f"✗ Project type: expected '{expected_type}', got '{actual_type}'")

        # Check deliverables count
        if 'min_deliverables' in expectations:
            deliverables = result.get('deliverables') or []
            actual_count = len(deliverables)
            expected_min = expectations['min_deliverables']
            if actual_count >= expected_min:
                test.successes.append(f"✓ Deliverables count: {actual_count} (>= {expected_min})")
            else:
                test.failures.append(f"✗ Deliverables: expected >= {expected_min}, got {actual_count}")

        # Check cost range
        if 'cost_min' in expectations and 'cost_max' in expectations:
            cost_range = result.get('cost_range')
            expected_min = expectations['cost_min']
            expected_max = expectations['cost_max']
            if check_cost_range(cost_range, expected_min, expected_max):
                test.successes.append(f"✓ Cost range appropriate: {cost_range}")
            else:
                test.failures.append(f"✗ Cost range: expected ${expected_min:,.0f}-${expected_max:,.0f}, got {cost_range}")

        # Check warnings presence/absence
        if 'has_warnings' in expectations:
            warnings = result.get('sanity_warnings') or []
            has_warnings = len(warnings) > 0
            expected_warnings = expectations['has_warnings']

            if has_warnings == expected_warnings:
                if has_warnings:
                    test.successes.append(f"✓ Warnings generated: {len(warnings)} warning(s)")
                else:
                    test.successes.append(f"✓ No warnings (as expected)")
            else:
                if expected_warnings:
                    test.failures.append(f"✗ Expected warnings but got none")
                else:
                    test.failures.append(f"✗ Unexpected warnings: {len(warnings)} found")

        # Check specific warning types
        if 'warning_keywords' in expectations:
            warnings = result.get('sanity_warnings') or []
            warnings_text = ' '.join(warnings).lower()
            for keyword in expectations['warning_keywords']:
                if keyword.lower() in warnings_text:
                    test.successes.append(f"✓ Warning contains '{keyword}'")
                else:
                    test.failures.append(f"✗ Expected warning about '{keyword}' not found")

        # Check is_complete
        if 'is_complete' in expectations:
            actual_complete = result.get('is_complete')
            expected_complete = expectations['is_complete']
            if actual_complete == expected_complete:
                test.successes.append(f"✓ is_complete: {actual_complete}")
            else:
                test.failures.append(f"✗ is_complete: expected {expected_complete}, got {actual_complete}")

        # Check proposal generation
        if 'has_proposal' in expectations:
            proposal = result.get('Proposal')
            has_proposal = proposal is not None and len(proposal) > 100
            expected_proposal = expectations['has_proposal']
            if has_proposal == expected_proposal:
                if has_proposal:
                    test.successes.append(f"✓ Full proposal generated ({len(proposal)} chars)")
                else:
                    test.successes.append(f"✓ No full proposal (as expected)")
            else:
                if expected_proposal:
                    test.failures.append(f"✗ Expected full proposal but got none/short")
                else:
                    test.failures.append(f"✗ Unexpected proposal generated")

        # Check questions generated
        if 'has_questions' in expectations:
            questions = result.get('clarifying_questions')
            has_questions = questions is not None and len(questions) > 0
            expected_questions = expectations['has_questions']
            if has_questions == expected_questions:
                if has_questions:
                    test.successes.append(f"✓ Questions generated")
                else:
                    test.successes.append(f"✓ No questions (as expected)")
            else:
                if expected_questions:
                    test.failures.append(f"✗ Expected questions but got none")
                else:
                    test.failures.append(f"✗ Unexpected questions generated")

        # Check timeline estimate
        if 'timeline_months_min' in expectations:
            timeline = result.get('calculated_timeline')
            if timeline:
                # Extract months from timeline string
                months_match = re.search(r'(\d+\.?\d*)\s*months?', timeline.lower())
                if months_match:
                    actual_months = float(months_match.group(1))
                    expected_min = expectations['timeline_months_min']
                    if actual_months >= expected_min:
                        test.successes.append(f"✓ Timeline: {actual_months} months (>= {expected_min})")
                    else:
                        test.failures.append(f"✗ Timeline: expected >= {expected_min} months, got {actual_months}")

        # Check no crash
        if 'no_crash' in expectations:
            test.successes.append(f"✓ No crash")

        # Determine pass/fail
        test.passed = len(test.failures) == 0

    except Exception as e:
        test.failures.append(f"✗ EXCEPTION: {str(e)}")
        test.passed = False

    # Print results
    for success in test.successes:
        print(success)
    for failure in test.failures:
        print(failure)

    if test.passed:
        print(f"\n{'RESULT: PASS ✓':>70}")
    else:
        print(f"\n{'RESULT: FAIL ✗':>70}")

    return test


def main():
    """Run all tests"""
    print("=" * 80)
    print("AUTOMATED TEST SUITE - PROPOSAL GENERATOR")
    print("=" * 80)

    # Create the graph
    print("\nInitializing workflow graph...")
    graph = create_graph()
    print("✓ Graph initialized\n")

    # Define test cases
    tests = [
        TestCase(
            1,
            "Complete detailed input",
            "E-commerce platform with cart, checkout, payment (Stripe), admin dashboard, reviews. Timeline: 4 months, Budget: $80k, Tech: React + Node.js",
            {
                'project_type': 'E-commerce',
                'min_deliverables': 5,
                'cost_min': 90000,
                'cost_max': 170000,
                'has_warnings': False,
                'has_proposal': True,
                'is_complete': True
            }
        ),
        TestCase(
            2,
            "Vague input",
            "Need a mobile app",
            {
                'is_complete': False,
                'has_questions': True
            }
        ),
        TestCase(
            3,
            "Budget-scope mismatch (high budget, low scope)",
            "Simple landing page with contact form. Budget: $100k",
            {
                'has_warnings': True,
                'warning_keywords': ['budget'],
                'has_proposal': True
            }
        ),
        TestCase(
            4,
            "Budget-scope mismatch (low budget, high scope)",
            "Enterprise ERP with CRM, inventory, accounting, HR, payroll, warehouse management. Budget: $20k",
            {
                'has_warnings': True,
                'warning_keywords': ['budget'],
                'cost_min': 150000,
                'cost_max': 300000
            }
        ),
        TestCase(
            5,
            "Unrealistic timeline",
            "Full e-commerce platform with 10 features in 2 weeks",
            {
                'has_warnings': True,
                'warning_keywords': ['timeline'],
                'timeline_months_min': 3
            }
        ),
        TestCase(
            6,
            "Outdated tech",
            "Build website using Flash and jQuery",
            {
                'has_warnings': True,
                'warning_keywords': ['flash', 'outdated', 'deprecated'],
                'has_proposal': True
            }
        ),
        TestCase(
            7,
            "Enterprise complexity",
            "Enterprise SaaS platform with multi-tenancy, RBAC, SSO, microservices, real-time analytics for 10,000+ users",
            {
                'project_type': 'SaaS',
                'cost_min': 150000,
                'cost_max': 400000,
                'timeline_months_min': 6
            }
        ),
        TestCase(
            8,
            "Healthcare compliance",
            "Healthcare patient portal with HIPAA compliance, EHR integration, telemedicine, e-prescriptions",
            {
                'cost_min': 100000,
                'cost_max': 250000,
                'has_proposal': True
            }
        ),
        TestCase(
            9,
            "Multi-country e-commerce",
            "E-commerce for 5 countries (US, UK, Germany, France, Japan) with multi-currency, multi-language, local payments",
            {
                'cost_min': 80000,
                'cost_max': 180000,
                'has_proposal': True
            }
        ),
        TestCase(
            10,
            "Migration project",
            "Migrate legacy .NET system to modern cloud architecture. 15 years of technical debt.",
            {
                'cost_min': 80000,
                'cost_max': 250000,
                'has_proposal': True
            }
        ),
        TestCase(
            11,
            "Empty input",
            "",
            {
                'no_crash': True,
                'is_complete': False
            }
        ),
        TestCase(
            12,
            "Only budget/timeline, no scope",
            "Need something in 3 months with $50k budget",
            {
                'is_complete': False,
                'has_questions': True
            }
        ),
        TestCase(
            13,
            "Startup MVP",
            "Early-stage startup MVP with core features: user signup, dashboard, basic analytics. Budget: $25k, Timeline: 6 weeks",
            {
                'cost_min': 15000,
                'cost_max': 60000,
                'has_proposal': True
            }
        ),
        TestCase(
            14,
            "SAP/Enterprise integration",
            "Integration with SAP ERP and Salesforce CRM for data synchronization",
            {
                'cost_min': 40000,
                'cost_max': 120000,
                'has_proposal': True
            }
        ),
        TestCase(
            15,
            "Duplicate deliverables",
            "Need user login, authentication system, sign-in functionality, and user access control",
            {
                'has_proposal': True,
                'cost_min': 10000,
                'cost_max': 60000
            }
        )
    ]

    # Run all tests
    results = []
    for test in tests:
        result = run_test(test, graph)
        results.append(result)

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    passed = sum(1 for t in results if t.passed)
    total = len(results)
    percentage = (passed / total) * 100

    print(f"\n{passed}/{total} tests passed ({percentage:.1f}%)")

    if passed < total:
        failed_nums = [t.test_num for t in results if not t.passed]
        print(f"Failed tests: {', '.join(map(str, failed_nums))}")

    print("\n" + "=" * 80)

    # Return exit code based on pass rate
    if percentage >= 90:
        print("✓ TEST SUITE PASSED (>= 90%)")
        return 0
    else:
        print(f"✗ TEST SUITE NEEDS IMPROVEMENT ({percentage:.1f}% < 90%)")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
