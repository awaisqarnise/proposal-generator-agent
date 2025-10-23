from typing import List, Optional


def _get_project_multiplier(project_type: Optional[str], user_input: str = "") -> float:
    """
    Get complexity multiplier based on project type and user input context.

    Base Multipliers:
    - E-commerce: 1.2x (complex integrations, payment security, inventory)
    - SaaS: 1.3x (multi-tenancy, subscriptions, complex architecture)
    - Mobile App: 1.1x (platform-specific considerations, testing)
    - Website: 0.8x (typically simpler, less backend complexity)
    - Custom Software: 1.0x (baseline)

    Context Multipliers (stacked on base):
    - Enterprise: 1.3x
    - Compliance (HIPAA, GDPR, etc.): 1.2x
    - Migration/Legacy: 1.4x
    - Multi-country/International: 1.2x

    Args:
        project_type: Type of project
        user_input: Original user input for context-aware multipliers

    Returns:
        Multiplier value
    """
    multiplier = 1.0

    # Base project type multiplier
    if project_type:
        project_type_lower = project_type.lower()

        if "e-commerce" in project_type_lower or "ecommerce" in project_type_lower:
            multiplier = 1.2
        elif "saas" in project_type_lower:
            multiplier = 1.3
        elif "mobile" in project_type_lower or "app" in project_type_lower:
            multiplier = 1.1
        elif "website" in project_type_lower:
            multiplier = 0.8
        elif "custom" in project_type_lower:
            multiplier = 1.0

    # Context-aware multipliers from user input
    if user_input:
        user_input_lower = user_input.lower()

        # Enterprise context
        if "enterprise" in user_input_lower:
            multiplier *= 1.3

        # Compliance context
        if any(word in user_input_lower for word in ["compliance", "hipaa", "gdpr", "sox", "pci"]):
            multiplier *= 1.2

        # Migration/Legacy context
        if any(word in user_input_lower for word in ["migration", "legacy"]):
            multiplier *= 1.4

        # International/Multi-country context
        if any(word in user_input_lower for word in ["multi-country", "international"]):
            multiplier *= 1.2

    return multiplier


def estimate_hours(deliverables: List[str], project_type: Optional[str] = None, user_input: str = "") -> int:
    """
    Estimate total hours based on deliverables, project type, and user context.

    Classification:
    - Simple deliverable: 40-60 hours (e.g., "login page", "contact form")
    - Medium deliverable: 80-120 hours, avg 150 (e.g., "payment integration", "search feature")
    - Complex deliverable: 150-250 hours, avg 300 (e.g., "admin dashboard", "analytics system")
    - Very Complex deliverable: 400-600 hours, avg 500 (e.g., "ERP system", "multi-tenant platform")

    Project type and context multipliers applied after base calculation.

    Args:
        deliverables: List of project deliverables
        project_type: Type of project (E-commerce, SaaS, Mobile App, Website, Custom Software)
        user_input: Original user input for context-aware multipliers

    Returns:
        Total estimated hours with project type and context multipliers applied
    """
    # Keywords to classify deliverables
    simple_keywords = [
        'login', 'signup', 'form', 'page', 'button', 'contact',
        'about', 'landing', 'static', 'simple', 'social'
    ]

    medium_keywords = [
        'payment', 'integration', 'api', 'search', 'filter',
        'cart', 'checkout', 'authentication', 'notification',
        'email', 'upload', 'download', 'profile',
    ]

    complex_keywords = [
        'dashboard', 'admin', 'analytics', 'reporting', 'real-time',
        'chat', 'video', ' ai ', 'machine learning', 'recommendation',
        'inventory', 'cms', 'management system', 'automation',
        # Enterprise systems
        'erp', 'crm', 'enterprise', 'sap', 'oracle',
        # Business management systems
        'inventory management', 'accounting', 'hr system', 'payroll',
        # Compliance and security
        'compliance', 'hipaa', 'gdpr', 'sox', 'pci',
        # Multi-tenant/international
        'multi-tenant', 'multi-currency', 'multi-language',
        # Supply chain and logistics
        'warehouse', 'logistics', 'supply chain',
        # Risk and security
        'fraud detection', 'risk management',
        # Legacy and migration
        'migration', 'legacy', 'modernization', 'refactor',
        # Cloud and infrastructure
        'cloud architecture', 'microservices', 'infrastructure'
    ]

    base_hours = 0

    print(f"\n{'='*60}")
    print(f"COST ESTIMATION DEBUG")
    print(f"{'='*60}")
    print(f"Total deliverables: {len(deliverables)}")
    print(f"Project type: {project_type or 'Unknown'}")
    print(f"\nAnalyzing each deliverable:")
    print(f"{'-'*60}")

    # Check if user context indicates MVP/basic/simple approach
    user_context_lower = user_input.lower() if user_input else ""
    is_mvp_context = any(word in user_context_lower for word in ['mvp', 'basic', 'simple', 'startup', 'early-stage', 'minimal'])

    for i, deliverable in enumerate(deliverables, 1):
        deliverable_lower = deliverable.lower()

        # Count how many complex keywords match
        matched_complex = [k for k in complex_keywords if k in deliverable_lower]
        matched_medium = [k for k in medium_keywords if k in deliverable_lower]
        matched_simple = [k for k in simple_keywords if k in deliverable_lower]

        # Check for very complex first (2+ complex keywords OR "system"/"platform" with complex keyword)
        has_system_or_platform = "system" in deliverable_lower or "platform" in deliverable_lower
        if len(matched_complex) >= 2 or (has_system_or_platform and len(matched_complex) >= 1):
            hours = 500
            complexity = "VERY_COMPLEX"
            matched_keywords = matched_complex
            # MVP context: downgrade VERY_COMPLEX to COMPLEX
            if is_mvp_context:
                hours = 300
                complexity = "COMPLEX (MVP context)"
            base_hours += hours
        # Then check for complex keywords
        elif len(matched_complex) > 0:
            hours = 300
            complexity = "COMPLEX"
            matched_keywords = matched_complex
            # MVP context: downgrade COMPLEX to MEDIUM
            if is_mvp_context:
                hours = 150
                complexity = "MEDIUM (MVP context)"
            base_hours += hours
        # Then check for medium keywords
        elif len(matched_medium) > 0:
            hours = 150
            complexity = "MEDIUM"
            matched_keywords = matched_medium
            base_hours += hours
        # Then check for simple keywords
        elif len(matched_simple) > 0:
            hours = 50
            complexity = "SIMPLE"
            matched_keywords = matched_simple
            base_hours += hours
        else:
            # Default to medium if no keywords match
            hours = 150
            complexity = "MEDIUM (default)"
            matched_keywords = ["no keywords matched"]
            base_hours += hours

        print(f"{i}. '{deliverable}'")
        print(f"   Complexity: {complexity}")
        print(f"   Matched: {', '.join(matched_keywords)}")
        print(f"   Hours: {hours}")
        print(f"   Running total: {base_hours} hours")
        print()

    # Apply project type and context multiplier
    multiplier = _get_project_multiplier(project_type, user_input)
    total_hours = int(base_hours * multiplier)

    print(f"{'-'*60}")
    print(f"Base hours (sum): {base_hours}")
    print(f"Project type: {project_type or 'Unknown'}")
    if user_input:
        print(f"User context: {user_input[:100]}..." if len(user_input) > 100 else f"User context: {user_input}")
    print(f"Multiplier: {multiplier:.2f}x")
    print(f"Total hours: {total_hours}")

    # Calculate costs for display
    min_cost = total_hours * 80
    max_cost = total_hours * 120
    print(f"Cost range: ${min_cost:,} - ${max_cost:,}")
    print(f"{'='*60}\n")

    return total_hours


def calculate_timeline(total_hours: int) -> str:
    """
    Calculate project timeline based on total hours.

    Assumptions:
    - 40 hours per week
    - 1 developer

    Args:
        total_hours: Total estimated hours

    Returns:
        Timeline string (e.g., "6 weeks" or "3 months")
    """
    if total_hours <= 0:
        return "Not enough information"

    # Calculate weeks (40 hours per week)
    weeks = total_hours / 40

    # If less than 8 weeks, return in weeks
    if weeks < 8:
        return f"{int(weeks)} weeks"
    else:
        # Convert to months (4 weeks = 1 month)
        months = weeks / 4
        return f"{round(months, 1)} months"


def estimate_cost(total_hours: int) -> str:
    """
    Estimate project cost based on total hours.

    Rate: $80-$120 per hour

    Args:
        total_hours: Total estimated hours

    Returns:
        Cost range string (e.g., "$40,000 - $60,000")
    """
    if total_hours <= 0:
        return "Not enough information"

    # Calculate cost range
    min_cost = total_hours * 80
    max_cost = total_hours * 120

    # Format with commas for thousands
    min_cost_formatted = f"${min_cost:,}"
    max_cost_formatted = f"${max_cost:,}"

    return f"{min_cost_formatted} - {max_cost_formatted}"
