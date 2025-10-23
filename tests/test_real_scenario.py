#!/usr/bin/env python3
"""
Test the actual scenario that was causing issues
"""
from src.tools.calculator import estimate_hours, estimate_cost, calculate_timeline


def test_real_world_scenario():
    """Test scenarios that were giving similar costs"""

    print("\n" + "="*60)
    print("SCENARIO 1: Small project with 2 deliverables")
    print("="*60)
    deliverables_small = [
        "Simple landing page",
        "Contact form"
    ]
    hours = estimate_hours(deliverables_small, "Website")
    print(f"\n>>> RESULT: {estimate_cost(hours)}")
    print(f">>> TIMELINE: {calculate_timeline(hours)}")

    print("\n" + "="*60)
    print("SCENARIO 2: Medium project with 5 deliverables")
    print("="*60)
    deliverables_medium = [
        "User authentication",
        "Profile management",
        "Search functionality",
        "Payment integration",
        "Email notifications"
    ]
    hours = estimate_hours(deliverables_medium, "SaaS")
    print(f"\n>>> RESULT: {estimate_cost(hours)}")
    print(f">>> TIMELINE: {calculate_timeline(hours)}")

    print("\n" + "="*60)
    print("SCENARIO 3: Large project with 15 deliverables")
    print("="*60)
    deliverables_large = [
        "Admin dashboard with analytics",
        "Real-time messaging system",
        "Video conferencing integration",
        "AI-powered recommendation engine",
        "Advanced reporting system",
        "Inventory management",
        "CMS for content management",
        "Multi-tenant architecture",
        "API gateway and integrations",
        "Payment processing system",
        "Notification system",
        "Search and filtering",
        "User management",
        "Automated workflow engine",
        "Mobile app integration"
    ]
    hours = estimate_hours(deliverables_large, "SaaS")
    print(f"\n>>> RESULT: {estimate_cost(hours)}")
    print(f">>> TIMELINE: {calculate_timeline(hours)}")


if __name__ == "__main__":
    test_real_world_scenario()
