import re
from typing import List, Optional
from state import ProposalState


def _extract_budget_number(budget_str: Optional[str]) -> Optional[int]:
    """
    Extract numeric budget value from budget string.

    Args:
        budget_str: Budget string like "$50,000 - $75,000" or "50k-75k"

    Returns:
        Average budget value in dollars, or None if can't parse
    """
    if not budget_str:
        return None

    # Remove currency symbols and spaces
    cleaned = budget_str.replace('$', '').replace(',', '').replace(' ', '').lower()

    # Find all numbers with optional k/m suffix
    pattern = r'(\d+(?:\.\d+)?)(k|m)?'
    matches = re.findall(pattern, cleaned)

    if not matches:
        return None

    values = []
    for num, suffix in matches:
        value = float(num)
        if suffix == 'k':
            value *= 1000
        elif suffix == 'm':
            value *= 1000000
        values.append(int(value))

    # Return average if range, or single value
    return sum(values) // len(values) if values else None


def _extract_timeline_months(timeline_str: Optional[str]) -> Optional[float]:
    """
    Extract timeline in months from timeline string.

    Args:
        timeline_str: Timeline string like "3 months", "6 weeks", "1.5 months"

    Returns:
        Timeline in months, or None if can't parse
    """
    if not timeline_str:
        return None

    timeline_lower = timeline_str.lower()

    # Look for weeks
    weeks_match = re.search(r'(\d+(?:\.\d+)?)\s*weeks?', timeline_lower)
    if weeks_match:
        weeks = float(weeks_match.group(1))
        return weeks / 4.0  # Convert to months

    # Look for months
    months_match = re.search(r'(\d+(?:\.\d+)?)\s*months?', timeline_lower)
    if months_match:
        return float(months_match.group(1))

    return None


def _check_budget_scope_mismatch(state: ProposalState, warnings: List[str]) -> None:
    """
    Check for budget-scope mismatches.

    Args:
        state: Current proposal state
        warnings: List to append warnings to
    """
    deliverables = state.get('deliverables', [])
    budget_hints = state.get('budget_hints')
    estimated_hours = state.get('estimated_hours')
    cost_range = state.get('cost_range')
    user_input = state.get('user_input', '').lower()

    if not deliverables:
        return

    num_deliverables = len(deliverables)

    # Check for unrealistic comparisons (like Amazon, Facebook, etc.)
    massive_platform_keywords = {
        'amazon': ('Amazon-scale', '$500M-$1B+'),
        'facebook': ('Facebook-scale', '$100M-$500M+'),
        'netflix': ('Netflix-scale', '$100M-$500M+'),
        'uber': ('Uber-scale', '$50M-$200M+'),
        'airbnb': ('Airbnb-scale', '$50M-$200M+'),
        'twitter': ('Twitter-scale', '$100M-$500M+'),
        'instagram': ('Instagram-scale', '$100M-$500M+'),
        'youtube': ('YouTube-scale', '$500M-$1B+'),
        'spotify': ('Spotify-scale', '$100M-$500M+'),
        'linkedin': ('LinkedIn-scale', '$100M-$500M+')
    }

    # Extract budget from hints or cost_range
    budget = _extract_budget_number(budget_hints) or _extract_budget_number(cost_range)

    # Check for massive platform comparisons
    for platform, (scale_name, typical_cost) in massive_platform_keywords.items():
        if f'like {platform}' in user_input or f'{platform}-like' in user_input or f'{platform} clone' in user_input:
            budget_msg = f"Current budget of ${budget:,}" if budget else "Any realistic budget"
            warnings.append(
                f"⚠️ Scope Warning: Building a '{scale_name}' platform requires {typical_cost} in development costs "
                f"and years of work by large teams. {budget_msg} is insufficient by orders of magnitude. "
                f"Consider building an MVP with core features only, or significantly increasing budget and timeline expectations."
            )
            break

    if budget:
        # Check if few deliverables but high budget
        if num_deliverables < 3 and budget > 80000:
            warnings.append(
                f"⚠️ Budget Warning: Budget of ${budget:,} seems high for only {num_deliverables} "
                f"deliverable{'s' if num_deliverables > 1 else ''}. Consider breaking down into more specific features "
                f"or verifying budget expectations."
            )

        # Check if many deliverables but low budget
        if num_deliverables > 10 and budget < 30000:
            warnings.append(
                f"⚠️ Budget Warning: Budget of ${budget:,} may be insufficient for {num_deliverables} deliverables. "
                f"Each deliverable would average ${budget // num_deliverables:,}, which is typically too low for "
                f"quality implementation. Consider increasing budget or reducing scope."
            )

        # NEW: Check for unrealistically low budget per deliverable (even if < 10 deliverables)
        if num_deliverables >= 3:
            budget_per_deliverable = budget / num_deliverables
            # If less than $3k per deliverable, it's likely too low
            if budget_per_deliverable < 3000:
                warnings.append(
                    f"⚠️ Budget Warning: Budget of ${budget:,} for {num_deliverables} deliverables averages "
                    f"${budget_per_deliverable:,.0f} per deliverable. This is unrealistically low for quality "
                    f"software development (typical minimum: $10,000-$20,000 per feature). Budget should be "
                    f"${num_deliverables * 10000:,}-${num_deliverables * 20000:,} minimum."
                )

        # NEW: Check for absurdly low total budget (< $10k for any project with deliverables)
        if num_deliverables > 0 and budget < 10000:
            warnings.append(
                f"⚠️ Budget Warning: Budget of ${budget:,} is extremely low for a software project with "
                f"{num_deliverables} deliverables. Even a simple MVP typically costs $15,000-$30,000 minimum. "
                f"Please revise budget expectations or significantly reduce scope."
            )

    # Check if estimated hours and budget don't align
    if estimated_hours and budget:
        try:
            hours = int(estimated_hours)
            # Assuming $80-120/hr average, use $100/hr for comparison
            expected_budget = hours * 100

            # If actual budget is less than 60% or more than 150% of expected
            if budget < expected_budget * 0.6:
                warnings.append(
                    f"⚠️ Budget-Hours Mismatch: Estimated {hours} hours suggests ~${expected_budget:,} budget, "
                    f"but provided budget is ${budget:,}. Budget may be insufficient for the estimated scope."
                )
            elif budget > expected_budget * 1.5:
                warnings.append(
                    f"⚠️ Budget-Hours Mismatch: Estimated {hours} hours suggests ~${expected_budget:,} budget, "
                    f"but provided budget is ${budget:,}. Budget seems higher than necessary, or scope may be underestimated."
                )
        except (ValueError, TypeError):
            pass


def _check_timeline_reality(state: ProposalState, warnings: List[str]) -> None:
    """
    Check for unrealistic timelines.

    Args:
        state: Current proposal state
        warnings: List to append warnings to
    """
    estimated_hours = state.get('estimated_hours')
    timeline_hints = state.get('timeline_hints')
    calculated_timeline = state.get('calculated_timeline')
    deliverables = state.get('deliverables', [])
    user_input = state.get('user_input', '').lower()

    # Check 1: Timeline-based checks WITHOUT estimated hours (for early detection)
    timeline_to_check = timeline_hints or calculated_timeline

    # If no timeline extracted, try to find timeline patterns in user_input
    if not timeline_to_check and user_input:
        import re
        # Look for patterns like "in X weeks", "in X months", "X week timeline"
        timeline_patterns = [
            r'in\s+(\d+)\s+(week|month|day)s?',
            r'(\d+)\s+(week|month|day)s?\s+(timeline|deadline|timeframe)',
            r'within\s+(\d+)\s+(week|month|day)s?'
        ]
        for pattern in timeline_patterns:
            match = re.search(pattern, user_input)
            if match:
                num = int(match.group(1))
                unit = match.group(2)
                if unit.startswith('week'):
                    timeline_to_check = f"{num} weeks"
                elif unit.startswith('month'):
                    timeline_to_check = f"{num} months"
                elif unit.startswith('day'):
                    timeline_to_check = f"{num} days"
                break

    if timeline_to_check and deliverables:
        timeline_months = _extract_timeline_months(timeline_to_check)
        num_deliverables = len(deliverables)

        if timeline_months:
            # Check for e-commerce/platform specific issues FIRST (more specific)
            user_input_lower = user_input.lower()
            is_ecommerce_or_platform = ('e-commerce' in user_input_lower or 'ecommerce' in user_input_lower or
                                       'platform' in user_input_lower or 'marketplace' in user_input_lower)

            # Unrealistic for e-commerce/complex projects (check first for specificity)
            if timeline_months <= 1 and is_ecommerce_or_platform:
                warnings.append(
                    f"⚠️ Timeline Warning: {timeline_months:.1f} months (about {int(timeline_months * 4)} weeks) "
                    f"for an e-commerce/platform project is unrealistic. E-commerce sites typically require "
                    f"3-6 months minimum for a basic MVP, even with existing frameworks. Consider extending "
                    f"timeline to at least 3 months."
                )

            # Very aggressive timeline for any significant project
            elif timeline_months < 1 and num_deliverables >= 3:
                warnings.append(
                    f"⚠️ Timeline Warning: {timeline_months:.1f} months (about {int(timeline_months * 4)} weeks) "
                    f"for {num_deliverables} deliverables is extremely aggressive. "
                    f"Even a simple feature typically takes 1-2 weeks minimum. "
                    f"Consider timeline of at least {num_deliverables * 2} weeks ({num_deliverables * 2 / 4:.1f} months)."
                )

            # Too short for many deliverables
            elif num_deliverables > 5 and timeline_months < 2:
                warnings.append(
                    f"⚠️ Timeline Warning: {num_deliverables} deliverables in {timeline_months:.1f} months "
                    f"is very tight. This allows only ~{timeline_months * 4 / num_deliverables:.1f} weeks per feature. "
                    f"Realistic timeline would be {num_deliverables * 2 / 4:.1f}-{num_deliverables * 4 / 4:.1f} months."
                )

    # Check 2: Hours-based checks (only if estimated_hours available)
    if not estimated_hours:
        return

    try:
        hours = int(estimated_hours)
    except (ValueError, TypeError):
        return

    # Check timeline hints
    timeline_to_check = timeline_hints or calculated_timeline
    if not timeline_to_check:
        return

    timeline_months = _extract_timeline_months(timeline_to_check)
    if not timeline_months:
        return

    # Assuming 40 hours/week, calculate expected months
    # 40 hrs/week * 4 weeks = 160 hrs/month for 1 developer
    expected_months = hours / 160.0

    # If estimated hours > 800 (5 months) and timeline mentions under 2 months
    if hours > 800 and timeline_months < 2:
        warnings.append(
            f"⚠️ Timeline Warning: {hours} hours would take ~{expected_months:.1f} months with 1 full-time developer, "
            f"but timeline suggests {timeline_months:.1f} months. This would require {expected_months / timeline_months:.1f}x "
            f"developers working in parallel, which may not be feasible for all tasks."
        )

    # If estimated hours < 200 (1.25 months) and timeline over 6 months
    elif hours < 200 and timeline_months > 6:
        warnings.append(
            f"⚠️ Timeline Warning: {hours} hours would take ~{expected_months:.1f} months, "
            f"but timeline suggests {timeline_months:.1f} months. Timeline seems longer than necessary, "
            f"unless there are external dependencies or part-time resources."
        )

    # General warning for significant mismatch
    elif timeline_months < expected_months * 0.4:
        warnings.append(
            f"⚠️ Timeline Warning: Timeline of {timeline_months:.1f} months may be too aggressive for "
            f"{hours} hours of work (expected ~{expected_months:.1f} months). Consider extending timeline "
            f"or increasing team size."
        )
    elif timeline_months > expected_months * 2.5:
        warnings.append(
            f"⚠️ Timeline Warning: Timeline of {timeline_months:.1f} months seems longer than necessary for "
            f"{hours} hours of work (expected ~{expected_months:.1f} months). Consider if there are specific "
            f"reasons for the extended timeline."
        )


def _check_tech_stack_issues(state: ProposalState, warnings: List[str]) -> None:
    """
    Check for tech stack issues.

    Args:
        state: Current proposal state
        warnings: List to append warnings to
    """
    tech_hints = state.get('tech_hints') or []
    user_input = state.get('user_input', '').lower()

    if not tech_hints and not user_input:
        return

    # Combine tech hints and user input for analysis
    tech_text = ' '.join([str(t).lower() for t in tech_hints]) + ' ' + user_input

    # Outdated technologies
    outdated_tech = {
        'flash': 'HTML5, WebGL, or modern web standards',
        'jquery': 'Vanilla JavaScript, React, Vue, or Angular (for UI interactivity)',
        'angular.js': 'Angular (modern version), React, or Vue',
        'angularjs': 'Angular (modern version), React, or Vue',
        'bower': 'npm or yarn (for package management)',
        'grunt': 'webpack, Vite, or npm scripts',
        'gulp': 'webpack, Vite, or npm scripts',
        'backbone': 'React, Vue, or Angular',
        'knockout': 'React, Vue, or Angular',
        'coffeescript': 'TypeScript or modern JavaScript (ES6+)',
        'php 5': 'PHP 8+ or Node.js',
        'mysql 5.5': 'MySQL 8.0+ or PostgreSQL',
        'python 2': 'Python 3.10+ (Python 2 is deprecated)',
        'ie 11': 'Modern browsers (Edge, Chrome, Firefox, Safari)'
    }

    for old_tech, modern_alt in outdated_tech.items():
        if old_tech in tech_text:
            warnings.append(
                f"⚠️ Tech Stack Warning: '{old_tech.title()}' is outdated/deprecated. "
                f"Consider using {modern_alt} instead for better performance, security, and maintainability."
            )

    # Conflicting framework choices
    conflicting_pairs = [
        (['react', 'reactjs'], ['angular', 'vue', 'vuejs'], 'frontend frameworks'),
        (['angular'], ['vue', 'vuejs'], 'frontend frameworks'),
        (['mysql', 'mariadb'], ['postgresql', 'postgres'], 'relational databases'),
        (['django'], ['flask', 'fastapi'], 'Python web frameworks'),
        (['express'], ['fastify', 'koa'], 'Node.js frameworks')
    ]

    for group1, group2, category in conflicting_pairs:
        has_group1 = any(tech in tech_text for tech in group1)
        has_group2 = any(tech in tech_text for tech in group2)

        if has_group1 and has_group2:
            found1 = [t for t in group1 if t in tech_text]
            found2 = [t for t in group2 if t in tech_text]
            warnings.append(
                f"⚠️ Tech Stack Warning: Multiple {category} detected ({', '.join(found1)} and {', '.join(found2)}). "
                f"This may indicate confusion in requirements. Typically, projects use one primary framework for {category}. "
                f"Please clarify which framework should be used."
            )

    # Check for missing complementary tech
    if 'react' in tech_text or 'vue' in tech_text or 'angular' in tech_text:
        if 'typescript' not in tech_text and 'javascript' not in tech_text:
            # Don't warn if it's already implied by framework mention
            pass

    # Warn about very old versions if mentioned
    version_patterns = [
        (r'node\s*(?:js)?\s*[v]?([0-9]+)', 10, 'Node.js', 'Node.js 18+ or 20+ (LTS)'),
        (r'react\s*[v]?([0-9]+)', 16, 'React', 'React 18+'),
        (r'angular\s*[v]?([0-9]+)', 12, 'Angular', 'Angular 15+'),
        (r'vue\s*[v]?([0-9]+)', 2, 'Vue', 'Vue 3+')
    ]

    for pattern, min_version, tech_name, modern_version in version_patterns:
        match = re.search(pattern, tech_text)
        if match:
            version = int(match.group(1))
            if version < min_version:
                warnings.append(
                    f"⚠️ Tech Stack Warning: {tech_name} {version} is outdated. "
                    f"Consider upgrading to {modern_version} for better features, performance, and security."
                )


def sanity_check_node(state: ProposalState) -> ProposalState:
    """
    Perform sanity checks on the proposal state to flag potential issues.

    Checks for:
    1. Budget-scope mismatches (too high/low for scope, mismatch with hours)
    2. Timeline reality issues (too aggressive or too long)
    3. Tech stack issues (outdated tech, conflicting choices)

    Args:
        state: Current ProposalState

    Returns:
        Updated ProposalState with sanity_warnings populated
    """
    print("\n" + "="*60)
    print("SANITY CHECK")
    print("="*60)

    warnings: List[str] = []

    try:
        # Check for budget-scope mismatches
        print("Checking budget-scope alignment...")
        _check_budget_scope_mismatch(state, warnings)

        # Check for timeline reality
        print("Checking timeline feasibility...")
        _check_timeline_reality(state, warnings)

        # Check for tech stack issues
        print("Checking tech stack compatibility...")
        _check_tech_stack_issues(state, warnings)

        if warnings:
            print(f"\n⚠️  Found {len(warnings)} warning(s):")
            for i, warning in enumerate(warnings, 1):
                print(f"\n{i}. {warning}")
        else:
            print("\n✓ No issues detected - proposal looks reasonable!")

        print("="*60 + "\n")

        return {
            **state,
            'sanity_warnings': warnings if warnings else None
        }

    except Exception as e:
        print(f"Error during sanity check: {str(e)}")
        # Don't fail the entire pipeline if sanity check fails
        return {
            **state,
            'sanity_warnings': [f"⚠️ Sanity check encountered an error: {str(e)}"]
        }
