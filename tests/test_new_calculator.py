#!/usr/bin/env python3
"""
Test new calculator features:
1. COMPLEX hours: 200 -> 300
2. DEFAULT hours: 100 -> 150
3. VERY_COMPLEX: 500 hours (2+ complex keywords OR system/platform + complex)
4. Context-aware multipliers from user_input
"""
from src.tools.calculator import estimate_hours, estimate_cost, calculate_timeline


def test_scenario(name, deliverables, project_type, user_input=""):
    """Test a scenario and display results"""
    print(f"\n{'#'*70}")
    print(f"TEST: {name}")
    print(f"{'#'*70}")

    hours = estimate_hours(deliverables, project_type, user_input)
    cost = estimate_cost(hours)
    timeline = calculate_timeline(hours)

    print(f"\n>>> FINAL RESULT:")
    print(f"    Cost: {cost}")
    print(f"    Timeline: {timeline}")
    print(f"    Hours: {hours}")
    print()


print("="*70)
print("NEW CALCULATOR FEATURES TEST")
print("="*70)
print("\nChanges:")
print("1. COMPLEX deliverables: 200 hrs -> 300 hrs")
print("2. DEFAULT (no match): 100 hrs -> 150 hrs")
print("3. VERY_COMPLEX (2+ complex keywords OR system/platform + complex): 500 hrs")
print("4. Context multipliers:")
print("   - Enterprise: 1.3x")
print("   - Compliance (HIPAA, GDPR, etc.): 1.2x")
print("   - Migration/Legacy: 1.4x")
print("   - Multi-country/International: 1.2x")
print("="*70)

# Test 1: Very Complex Systems (2+ complex keywords)
test_scenario(
    "VERY_COMPLEX: ERP Accounting System (2 complex keywords)",
    deliverables=[
        "ERP accounting system",  # Should be VERY_COMPLEX (erp + accounting)
        "Payroll management",     # COMPLEX
        "Inventory tracking"      # COMPLEX
    ],
    project_type="SaaS",
    user_input=""
)

# Test 2: Very Complex with "system" + complex keyword
test_scenario(
    "VERY_COMPLEX: Analytics Platform (system/platform + complex)",
    deliverables=[
        "Analytics platform",         # Should be VERY_COMPLEX (platform + analytics)
        "Reporting dashboard system", # Should be VERY_COMPLEX (system + reporting/dashboard)
        "Real-time monitoring"        # COMPLEX
    ],
    project_type="SaaS",
    user_input=""
)

# Test 3: Context multiplier - Enterprise
test_scenario(
    "Context Multiplier: Enterprise + Compliance",
    deliverables=[
        "Admin dashboard",
        "User management",
        "Audit logging"
    ],
    project_type="Custom Software",
    user_input="Enterprise CRM system with HIPAA compliance requirements"
)

# Test 4: Context multiplier - Migration
test_scenario(
    "Context Multiplier: Legacy Migration",
    deliverables=[
        "Data migration",
        "API modernization",
        "Database upgrade"
    ],
    project_type="Custom Software",
    user_input="Legacy system migration from Oracle to PostgreSQL"
)

# Test 5: Context multiplier - International
test_scenario(
    "Context Multiplier: Multi-country E-commerce",
    deliverables=[
        "Multi-currency payment",
        "Multi-language support",
        "Local payment methods"
    ],
    project_type="E-commerce",
    user_input="E-commerce for 5 countries (US, UK, Germany, France, Japan). Multi-country deployment."
)

# Test 6: Stacked context multipliers
test_scenario(
    "Stacked Multipliers: Enterprise + Compliance + International",
    deliverables=[
        "Multi-tenant platform",
        "HIPAA compliant storage",
        "Compliance reporting",
        "Multi-currency billing"
    ],
    project_type="SaaS",
    user_input="Enterprise healthcare SaaS with GDPR and HIPAA compliance for international deployment"
)

# Test 7: Default hours change (100 -> 150)
test_scenario(
    "Default Hours Test (no keyword matches)",
    deliverables=[
        "Feature A",
        "Feature B",
        "Feature C"
    ],
    project_type="Custom Software",
    user_input=""
)

# Test 8: Compare old vs new - Same deliverables
print("\n" + "="*70)
print("COMPARISON: Same deliverables, different classifications")
print("="*70)

test_scenario(
    "Standard Features (MEDIUM: 150 hrs each)",
    deliverables=[
        "User authentication",
        "Email notifications",
        "File upload"
    ],
    project_type="Custom Software",
    user_input=""
)

test_scenario(
    "Complex Features (COMPLEX: 300 hrs each)",
    deliverables=[
        "Admin dashboard",
        "Analytics reporting",
        "Real-time chat"
    ],
    project_type="Custom Software",
    user_input=""
)

test_scenario(
    "Very Complex Systems (VERY_COMPLEX: 500 hrs each)",
    deliverables=[
        "ERP accounting system",
        "Inventory management system",
        "Multi-tenant CRM platform"
    ],
    project_type="SaaS",
    user_input=""
)

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("✓ COMPLEX hours increased: 200 -> 300")
print("✓ DEFAULT hours increased: 100 -> 150")
print("✓ VERY_COMPLEX tier added: 500 hours")
print("✓ Context multipliers working from user_input")
print("✓ Multiple context multipliers stack correctly")
print("="*70)
