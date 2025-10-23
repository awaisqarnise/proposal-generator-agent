#!/usr/bin/env python3
"""
Test script to debug calculator cost estimation
"""
from src.tools.calculator import estimate_hours, estimate_cost, calculate_timeline


def test_scenario(name, deliverables, project_type="Custom Software"):
    """Test a scenario and display results"""
    print(f"\n{'#'*60}")
    print(f"TEST: {name}")
    print(f"{'#'*60}")

    hours = estimate_hours(deliverables, project_type)
    cost = estimate_cost(hours)
    timeline = calculate_timeline(hours)

    print(f"\nFINAL SUMMARY:")
    print(f"Timeline: {timeline}")
    print(f"\n")


if __name__ == "__main__":
    print("="*60)
    print("CALCULATOR DEBUG TESTS")
    print("="*60)

    # Test 1: 2 simple deliverables (should be ~$20-30k)
    test_scenario(
        "2 Simple Deliverables (Target: $20-30k)",
        deliverables=[
            "Login page",
            "Contact form"
        ]
    )

    # Test 2: 5 mixed deliverables (should be ~$50-70k)
    test_scenario(
        "5 Mixed Deliverables (Target: $50-70k)",
        deliverables=[
            "Login page",
            "User profile",
            "Payment integration",
            "Email notifications",
            "Search feature"
        ]
    )

    # Test 3: 15 complex deliverables (should be ~$150-200k+)
    test_scenario(
        "15 Complex Deliverables (Target: $150-200k+)",
        deliverables=[
            "Admin dashboard",
            "Analytics system",
            "Real-time chat",
            "Payment integration",
            "Inventory management system",
            "CMS for content",
            "User authentication",
            "Email notification system",
            "Search and filter functionality",
            "Reporting dashboard",
            "API integration layer",
            "File upload and management",
            "Recommendation engine",
            "Video streaming feature",
            "Automation workflows"
        ]
    )

    # Test 4: Current issue - similar costs for different complexities
    print(f"\n{'#'*60}")
    print("COMPARISON TEST - Different complexity, same deliverable count")
    print(f"{'#'*60}")

    test_scenario(
        "5 Simple Deliverables",
        deliverables=[
            "Login page",
            "Signup page",
            "Contact form",
            "About page",
            "Landing page"
        ]
    )

    test_scenario(
        "5 Complex Deliverables",
        deliverables=[
            "Admin dashboard",
            "Analytics reporting",
            "Real-time chat system",
            "AI recommendation engine",
            "Inventory management CMS"
        ]
    )
