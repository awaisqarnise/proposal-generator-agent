#!/usr/bin/env python3
"""
Test enterprise and high-value system keywords
"""
from src.tools.calculator import estimate_hours, estimate_cost, calculate_timeline


def test_enterprise_scenarios():
    """Test various enterprise scenarios"""

    print("\n" + "="*60)
    print("TEST 1: Multi-currency E-commerce (from main.py)")
    print("="*60)
    deliverables = [
        "Multi-currency payment system",
        "Multi-language support",
        "Local payment method integrations (5 countries)",
        "Product catalog management",
        "Shopping cart and checkout",
        "Order management system",
        "Inventory management",
        "Customer account management",
        "Admin dashboard"
    ]
    hours = estimate_hours(deliverables, "E-commerce")
    print(f"\n>>> RESULT: {estimate_cost(hours)}")
    print(f">>> TIMELINE: {calculate_timeline(hours)}")

    print("\n" + "="*60)
    print("TEST 2: Enterprise ERP System")
    print("="*60)
    deliverables = [
        "ERP core system",
        "Accounting module",
        "HR system and payroll",
        "Inventory management",
        "Supply chain management",
        "Warehouse management",
        "Reporting dashboard",
        "Multi-tenant architecture",
        "Compliance and audit logging (SOX, GDPR)",
        "CRM integration"
    ]
    hours = estimate_hours(deliverables, "SaaS")
    print(f"\n>>> RESULT: {estimate_cost(hours)}")
    print(f">>> TIMELINE: {calculate_timeline(hours)}")

    print("\n" + "="*60)
    print("TEST 3: Healthcare Compliance System")
    print("="*60)
    deliverables = [
        "HIPAA compliant data storage",
        "Patient management system",
        "Electronic health records",
        "Appointment scheduling",
        "Billing and insurance integration",
        "Compliance reporting",
        "Audit trail system",
        "Role-based access control"
    ]
    hours = estimate_hours(deliverables, "Custom Software")
    print(f"\n>>> RESULT: {estimate_cost(hours)}")
    print(f">>> TIMELINE: {calculate_timeline(hours)}")

    print("\n" + "="*60)
    print("TEST 4: Legacy System Migration")
    print("="*60)
    deliverables = [
        "Legacy system analysis",
        "Data migration from Oracle to PostgreSQL",
        "API modernization",
        "Microservices architecture",
        "User authentication migration",
        "Reporting system rebuild",
        "Integration testing"
    ]
    hours = estimate_hours(deliverables, "Custom Software")
    print(f"\n>>> RESULT: {estimate_cost(hours)}")
    print(f">>> TIMELINE: {calculate_timeline(hours)}")

    print("\n" + "="*60)
    print("TEST 5: Financial Risk Management")
    print("="*60)
    deliverables = [
        "Fraud detection system with AI",
        "Risk management dashboard",
        "PCI compliance implementation",
        "Transaction monitoring",
        "Real-time analytics",
        "Automated reporting",
        "Alert system"
    ]
    hours = estimate_hours(deliverables, "SaaS")
    print(f"\n>>> RESULT: {estimate_cost(hours)}")
    print(f">>> TIMELINE: {calculate_timeline(hours)}")


if __name__ == "__main__":
    test_enterprise_scenarios()
