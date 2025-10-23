# Generation Node - Sanity Warnings Integration

## Overview

Updated `src/nodes/generation.py` to automatically include sanity warnings at the **top** of generated proposals, ensuring critical issues are immediately visible before any other content.

## Changes Made

### 1. Extract Sanity Warnings from State

Added line 50 in generation.py:
```python
# Get sanity warnings
sanity_warnings = state.get("sanity_warnings")
```

### 2. Build Warnings Section

Lines 264-282: Create formatted warnings section if warnings exist:

```python
# Build warnings section at the TOP if warnings exist
warnings_section = ""
if sanity_warnings and len(sanity_warnings) > 0:
    warnings_section = "# ⚠️ Important Considerations\n\n"
    warnings_section += "**Please review these points before proceeding with this proposal:**\n\n"

    for i, warning in enumerate(sanity_warnings, 1):
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
```

### 3. Prepend to Proposal

Lines 284-294: Add warnings at the very top, before questions or proposal content:

```python
# If there are clarifying questions, add them after warnings
if has_questions:
    questions_section = "## Clarifying Questions\n\n..."
    proposal_text = warnings_section + questions_section + proposal_text
else:
    # Just warnings (if any) at the top
    proposal_text = warnings_section + proposal_text
```

## Formatting Logic

### Warning Transformation

**Input** (from sanity_check_node):
```
⚠️ Budget Warning: Budget of $25,000 may be insufficient for 12 deliverables.
```

**Output** (in proposal):
```
1. **Budget Warning**: Budget of $25,000 may be insufficient for 12 deliverables.
```

### Formatting Rules

1. **Remove leading emoji** - Strips `⚠️` from start
2. **Bold the category** - Everything before `:` becomes bold header
3. **Regular text for details** - Everything after `:` is regular text
4. **Numbered list** - Each warning gets a number
5. **Double line breaks** - Extra spacing for readability
6. **Horizontal rule** - `---` separator after all warnings

## Example Output

### Proposal with 3 Warnings

```markdown
# ⚠️ Important Considerations

**Please review these points before proceeding with this proposal:**

1. **Budget Warning**: Budget of $25,000 may be insufficient for 12 deliverables. Each deliverable would average $2,083, which is typically too low for quality implementation. Consider increasing budget or reducing scope.

2. **Timeline Warning**: 1000 hours would take ~6.2 months with 1 full-time developer, but timeline suggests 1.0 months. This would require 6.2x developers working in parallel, which may not be feasible for all tasks.

3. **Tech Stack Warning**: 'Jquery' is outdated/deprecated. Consider using Vanilla JavaScript, React, Vue, or Angular (for UI interactivity) instead for better performance, security, and maintainability.

---

# 1. About This Proposal

This proposal provides an in-depth look at a proposed E-commerce project...

# 2. Executive Summary

This project aims to create an E-commerce platform...
```

### Proposal without Warnings

If `sanity_warnings` is `None` or empty list, proposal starts normally:

```markdown
# 1. About This Proposal

This proposal provides an in-depth look...
```

## Document Structure Hierarchy

The final proposal structure is now:

1. **⚠️ Important Considerations** (if warnings exist)
2. **Clarifying Questions** (if questions exist)
3. **1. About This Proposal** (always)
4. **2. Executive Summary** (always)
5. ... rest of sections

## Edge Cases Handled

### Empty Warnings
```python
sanity_warnings = None  # or []
# Result: No warnings section added
```

### Single Warning
```python
sanity_warnings = ["⚠️ Budget Warning: Budget too high"]
# Result: Section with 1 warning
```

### Warning Without Colon
```python
sanity_warnings = ["⚠️ This is a simple warning"]
# Result: **This is a simple warning**
```

### Warning with Multiple Colons
```python
sanity_warnings = ["⚠️ Tech: React: Version too old: Upgrade"]
# Result: **Tech**: React: Version too old: Upgrade
```

## Visual Design

### Why This Format Works

✅ **Top placement** - First thing users see
✅ **Clear header** - Emoji + "Important Considerations" stands out
✅ **Bold categories** - Easy to scan warning types
✅ **Professional** - Not alarmist, just informative
✅ **Actionable** - Each warning includes suggestions
✅ **Separated** - Horizontal rule creates visual break
✅ **Numbered** - Easy to reference in discussions

## Integration Flow

```
User Input
    ↓
Extraction Node
    ↓
Validation Node
    ↓
Sanity Check Node  ← Creates sanity_warnings
    ↓
Calculator Node
    ↓
Generation Node    ← Adds warnings to top of proposal
    ↓
Final Proposal
```

## Testing

Run the test suite:
```bash
python test_generation_with_warnings.py
```

Output shows:
1. How warnings are formatted
2. Comparison with/without warnings
3. Edge case handling

## Backward Compatibility

✅ **Fully compatible** - If no warnings, proposal is unchanged
✅ **No breaking changes** - Only adds content when warnings exist
✅ **Optional** - Works with or without sanity_check_node

## Benefits

### For Users
- 🔍 Immediate visibility of issues
- 📋 Clear action items before committing
- 🎯 Professional presentation
- ✅ Better decision making

### For Developers
- 🔧 Easy to maintain
- 📝 Simple formatting logic
- 🧪 Testable
- 🔄 Reusable pattern

## Example Use Cases

### Case 1: Budget Too Low
```
# ⚠️ Important Considerations

1. **Budget Warning**: Budget of $20,000 may be insufficient for 12 deliverables.
   Consider increasing budget or reducing scope.
```
**Action**: Client can adjust budget or reduce features before proposal finalization

### Case 2: Outdated Tech
```
# ⚠️ Important Considerations

1. **Tech Stack Warning**: 'jQuery' is outdated/deprecated.
   Consider using React, Vue, or Angular instead.
```
**Action**: Team can modernize tech choices before starting work

### Case 3: Timeline Unrealistic
```
# ⚠️ Important Considerations

1. **Timeline Warning**: 1000 hours would take ~6 months with 1 developer,
   but timeline suggests 2 months. Consider extending timeline or adding team members.
```
**Action**: Realistic timeline can be negotiated upfront

## Code Location

**File**: `src/nodes/generation.py`
**Lines**:
- 50: Extract warnings from state
- 264-282: Build warnings section
- 284-294: Prepend to proposal

## Related Files

- `src/nodes/sanity_check.py` - Generates warnings
- `test_generation_with_warnings.py` - Tests formatting
- `SANITY_CHECK_FEATURE.md` - Full sanity check docs

## Customization

### Change Header Text
Line 267:
```python
warnings_section = "# ⚠️ Important Considerations\n\n"
# Change to:
warnings_section = "# 🚨 Risk Assessment\n\n"
```

### Change Intro Text
Line 268:
```python
warnings_section += "**Please review these points before proceeding:**\n\n"
```

### Change Separator
Line 282:
```python
warnings_section += "---\n\n"
# Change to:
warnings_section += "***\n\n"  # or remove entirely
```

### Remove Emoji
Line 272:
```python
clean_warning = warning.replace("⚠️", "").strip()
# Add more emoji removals:
clean_warning = warning.replace("⚠️", "").replace("🚨", "").strip()
```

## Future Enhancements

Potential improvements:

1. **Severity Levels** - Color code by severity (info/warning/critical)
2. **Clickable Links** - Link to docs for tech alternatives
3. **Collapsible** - Make warnings collapsible in UI
4. **Summary Count** - "3 warnings detected" at top
5. **Filter by Category** - Separate sections for budget/timeline/tech

## Conclusion

The generation node now seamlessly integrates sanity warnings into proposals, ensuring critical issues are surfaced prominently without disrupting the existing proposal flow. This provides immediate value to users while maintaining professional presentation standards.
