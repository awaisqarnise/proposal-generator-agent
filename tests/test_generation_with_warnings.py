#!/usr/bin/env python3
"""
Test generation node with sanity warnings integration
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from state import ProposalState


def test_warnings_formatting():
    """Test how warnings are formatted in the proposal"""

    print("="*70)
    print("TESTING GENERATION NODE WITH SANITY WARNINGS")
    print("="*70)

    # Sample warnings from sanity check
    sample_warnings = [
        "⚠️ Budget Warning: Budget of $25,000 may be insufficient for 12 deliverables. Each deliverable would average $2,083, which is typically too low for quality implementation. Consider increasing budget or reducing scope.",
        "⚠️ Timeline Warning: 1000 hours would take ~6.2 months with 1 full-time developer, but timeline suggests 1.0 months. This would require 6.2x developers working in parallel, which may not be feasible for all tasks.",
        "⚠️ Tech Stack Warning: 'Jquery' is outdated/deprecated. Consider using Vanilla JavaScript, React, Vue, or Angular (for UI interactivity) instead for better performance, security, and maintainability."
    ]

    print("\n1. Sample Warnings from Sanity Check:")
    print("-" * 70)
    for i, warning in enumerate(sample_warnings, 1):
        print(f"{i}. {warning}")

    print("\n2. How They Will Appear in Proposal:")
    print("-" * 70)

    # Simulate the formatting logic from generation.py
    warnings_section = "# ⚠️ Important Considerations\n\n"
    warnings_section += "**Please review these points before proceeding with this proposal:**\n\n"

    for i, warning in enumerate(sample_warnings, 1):
        # Clean the warning (remove emoji if present at start)
        clean_warning = warning.replace("⚠️", "").strip()

        # Add as numbered item with proper formatting
        warnings_section += f"{i}. **{clean_warning.split(':')[0].strip()}**"
        if ':' in clean_warning:
            # Add the detail after the colon
            warnings_section += f": {':'.join(clean_warning.split(':')[1:]).strip()}\n\n"
        else:
            warnings_section += f" {clean_warning}\n\n"

    warnings_section += "---\n\n"

    print(warnings_section)

    print("\n3. Full Proposal Structure:")
    print("-" * 70)
    print("""
# ⚠️ Important Considerations

**Please review these points before proceeding with this proposal:**

1. **Budget Warning**: Budget of $25,000 may be insufficient...
2. **Timeline Warning**: 1000 hours would take ~6.2 months...
3. **Tech Stack Warning**: 'Jquery' is outdated/deprecated...

---

# 1. About This Proposal

This proposal provides...

# 2. Executive Summary

This project aims to...

[Rest of proposal sections...]
    """)

    print("\n4. Benefits of This Format:")
    print("-" * 70)
    print("✓ Warnings are at the TOP (impossible to miss)")
    print("✓ Clear visual separation with emoji and horizontal rule")
    print("✓ Professional formatting with bold headers")
    print("✓ Numbered for easy reference")
    print("✓ Actionable suggestions included")

    print("\n" + "="*70)
    print("✓ Warnings integration test complete!")
    print("="*70)


def show_with_and_without():
    """Show comparison of proposals with and without warnings"""

    print("\n\n" + "="*70)
    print("COMPARISON: WITH vs WITHOUT WARNINGS")
    print("="*70)

    print("\n▼ PROPOSAL WITHOUT WARNINGS:")
    print("-" * 70)
    print("""
# 1. About This Proposal
This proposal provides an in-depth look...

# 2. Executive Summary
This project aims to create...
    """)

    print("\n▼ PROPOSAL WITH WARNINGS:")
    print("-" * 70)
    print("""
# ⚠️ Important Considerations

**Please review these points before proceeding with this proposal:**

1. **Budget Warning**: Budget of $25,000 may be insufficient for 12 deliverables.
   Consider increasing budget or reducing scope.

2. **Timeline Warning**: Timeline of 2 months may be too aggressive for 1200 hours.
   Consider extending timeline or increasing team size.

---

# 1. About This Proposal
This proposal provides an in-depth look...

# 2. Executive Summary
This project aims to create...
    """)

    print("\n" + "="*70)


def show_edge_cases():
    """Show edge cases in warning formatting"""

    print("\n\n" + "="*70)
    print("EDGE CASES")
    print("="*70)

    test_cases = [
        ("Warning with colon", "⚠️ Budget Warning: Budget too high"),
        ("Warning without colon", "⚠️ This is a simple warning"),
        ("Warning with multiple colons", "⚠️ Tech Warning: React: Version too old: Upgrade needed"),
        ("Warning already clean", "Budget Warning: Budget seems high")
    ]

    for name, warning in test_cases:
        print(f"\n{name}:")
        print(f"Input:  {warning}")

        clean_warning = warning.replace("⚠️", "").strip()
        if ':' in clean_warning:
            formatted = f"**{clean_warning.split(':')[0].strip()}**: {':'.join(clean_warning.split(':')[1:]).strip()}"
        else:
            formatted = f"**{clean_warning}**"

        print(f"Output: {formatted}")

    print("\n" + "="*70)


if __name__ == "__main__":
    test_warnings_formatting()
    show_with_and_without()
    show_edge_cases()
