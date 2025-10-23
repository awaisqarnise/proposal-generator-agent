#!/usr/bin/env python3
"""
Before/After comparison showing the impact of calculator changes
"""
from src.tools.calculator import estimate_hours, estimate_cost


print("="*80)
print("BEFORE vs AFTER COMPARISON")
print("="*80)
print("\nChanges Made:")
print("1. COMPLEX: 200 hrs → 300 hrs (+50%)")
print("2. MEDIUM/DEFAULT: 100 hrs → 150 hrs (+50%)")
print("3. NEW VERY_COMPLEX: 500 hrs (2+ complex keywords OR system/platform + complex)")
print("4. Context multipliers: Enterprise (1.3x), Compliance (1.2x), Migration (1.4x), International (1.2x)")
print("="*80)

test_cases = [
    {
        "name": "Simple Website",
        "deliverables": ["Landing page", "Contact form"],
        "project_type": "Website",
        "user_input": "",
        "old_base": 100,  # 50 + 50
        "old_mult": 0.8,
        "old_hours": 80,
        "old_cost": "$6,400 - $9,600"
    },
    {
        "name": "Standard Web App",
        "deliverables": ["User authentication", "Email notifications", "File upload"],
        "project_type": "Custom Software",
        "user_input": "",
        "old_base": 300,  # 100 + 100 + 100
        "old_mult": 1.0,
        "old_hours": 300,
        "old_cost": "$24,000 - $36,000"
    },
    {
        "name": "Complex Dashboard App",
        "deliverables": ["Admin dashboard", "Analytics reporting", "Real-time chat"],
        "project_type": "Custom Software",
        "user_input": "",
        "old_base": 600,  # 200 + 200 + 200
        "old_mult": 1.0,
        "old_hours": 600,
        "old_cost": "$48,000 - $72,000"
    },
    {
        "name": "Multi-country E-commerce",
        "deliverables": ["Multi-currency support", "Multi-language support", "Local payment methods"],
        "project_type": "E-commerce",
        "user_input": "E-commerce for 5 countries. Multi-country deployment.",
        "old_base": 500,  # 200 + 200 + 100
        "old_mult": 1.2,
        "old_hours": 600,
        "old_cost": "$48,000 - $72,000"
    },
    {
        "name": "Enterprise ERP System",
        "deliverables": ["ERP accounting system", "Payroll management", "Inventory tracking"],
        "project_type": "SaaS",
        "user_input": "Enterprise system",
        "old_base": 600,  # 200 + 200 + 200 (no VERY_COMPLEX in old)
        "old_mult": 1.3,
        "old_hours": 780,
        "old_cost": "$62,400 - $93,600"
    },
    {
        "name": "Healthcare Compliance System",
        "deliverables": ["HIPAA compliant storage", "Patient management system", "Compliance reporting"],
        "project_type": "Custom Software",
        "user_input": "Healthcare system with HIPAA compliance",
        "old_base": 600,  # 200 + 200 + 200
        "old_mult": 1.0,  # No context multipliers in old
        "old_hours": 600,
        "old_cost": "$48,000 - $72,000"
    }
]

print("\n")
for i, test in enumerate(test_cases, 1):
    print(f"{i}. {test['name']}")
    print("   " + "-"*60)

    # Calculate NEW values
    new_hours = estimate_hours(test['deliverables'], test['project_type'], test['user_input'])
    new_cost = estimate_cost(new_hours)

    # Show comparison
    print(f"   BEFORE: {test['old_hours']} hrs | {test['old_cost']}")
    print(f"   AFTER:  {new_hours} hrs | {new_cost}")

    # Calculate increase
    hours_increase = ((new_hours - test['old_hours']) / test['old_hours']) * 100
    print(f"   CHANGE: +{hours_increase:.0f}%")

    # Show why
    if test['user_input'] and any(word in test['user_input'].lower() for word in ['enterprise', 'compliance', 'migration', 'multi-country', 'international']):
        print(f"   REASON: Context multipliers applied from user input")

    print()

print("="*80)
print("KEY INSIGHTS")
print("="*80)
print("✓ Simple projects (2-3 simple features): Minimal change (~0-20%)")
print("✓ Standard web apps (medium features): +50% increase")
print("✓ Complex apps (dashboards, analytics): +150% (VERY_COMPLEX tier)")
print("✓ Enterprise/Compliance: +100-300% (context multipliers)")
print("✓ E-commerce multi-country: +50-100% (complex features + context)")
print()
print("These increases reflect more realistic estimates for:")
print("- Enterprise-grade systems")
print("- Compliance requirements (HIPAA, GDPR, etc.)")
print("- Multi-tenant architectures")
print("- International/multi-country deployments")
print("- Legacy system migrations")
print("="*80)
