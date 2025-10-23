# Sanity Check Feature

## Overview

The sanity check node analyzes proposals for common issues and red flags, providing warnings to help catch problems early. It checks for budget-scope mismatches, unrealistic timelines, and tech stack issues.

## State Schema Update

Added to `src/state.py`:
```python
sanity_warnings: Optional[List[str]]
```

## Implementation

Created `src/nodes/sanity_check.py` with the following checks:

### 1. Budget-Scope Mismatch Detection

**Check 1: Budget Too High for Few Deliverables**
- Triggers when: < 3 deliverables AND budget > $80,000
- Example: 2 deliverables with $100k budget
- Warning: "Budget seems high for only X deliverables"

**Check 2: Budget Too Low for Many Deliverables**
- Triggers when: > 10 deliverables AND budget < $30,000
- Example: 12 deliverables with $25k budget
- Warning: "Budget may be insufficient... Each deliverable would average $X"

**Check 3: Budget-Hours Mismatch**
- Compares estimated hours with budget (using $100/hr average)
- Triggers when budget is < 60% or > 150% of expected budget
- Example: 1000 hours (expects ~$100k) but budget is $30k
- Warning: "Estimated X hours suggests ~$Y budget, but provided budget is $Z"

### 2. Timeline Reality Checks

**Check 1: Timeline Too Aggressive**
- Triggers when: > 800 hours AND timeline < 2 months
- Calculates expected months (assuming 40 hrs/week, 1 developer)
- Example: 1000 hours in 4 weeks (needs 6x developers)
- Warning: "Would require Xx developers working in parallel"

**Check 2: Timeline Too Long**
- Triggers when: < 200 hours AND timeline > 6 months
- Example: 150 hours over 8 months
- Warning: "Timeline seems longer than necessary"

**Check 3: General Timeline Mismatch**
- Timeline < 40% of expected: "Too aggressive"
- Timeline > 250% of expected: "Longer than necessary"

### 3. Tech Stack Issue Detection

**Outdated Technologies:**
- Flash → HTML5, WebGL, modern web standards
- jQuery → Vanilla JavaScript, React, Vue, Angular
- AngularJS → Angular (modern), React, Vue
- Bower → npm, yarn
- Grunt/Gulp → webpack, Vite
- Backbone/Knockout → React, Vue, Angular
- CoffeeScript → TypeScript, ES6+
- PHP 5 → PHP 8+, Node.js
- MySQL 5.5 → MySQL 8.0+, PostgreSQL
- Python 2 → Python 3.10+
- IE 11 → Modern browsers

**Conflicting Framework Choices:**
- Multiple frontend frameworks (React + Angular)
- Multiple databases (MySQL + PostgreSQL)
- Multiple Python frameworks (Django + Flask)
- Multiple Node.js frameworks (Express + Fastify)

**Old Versions:**
- Node.js < 10 → Node.js 18+/20+
- React < 16 → React 18+
- Angular < 12 → Angular 15+
- Vue < 2 → Vue 3+

## Usage

```python
from nodes.sanity_check import sanity_check_node

# After calculations, before generation
state = sanity_check_node(state)

# Check for warnings
if state.get('sanity_warnings'):
    for warning in state['sanity_warnings']:
        print(warning)
```

## Example Output

### Budget Too High
```
⚠️ Budget Warning: Budget of $100,000 seems high for only 2 deliverables.
Consider breaking down into more specific features or verifying budget expectations.

⚠️ Budget-Hours Mismatch: Estimated 100 hours suggests ~$10,000 budget,
but provided budget is $100,000. Budget seems higher than necessary, or
scope may be underestimated.
```

### Timeline Too Aggressive
```
⚠️ Timeline Warning: 1000 hours would take ~6.2 months with 1 full-time developer,
but timeline suggests 1.0 months. This would require 6.2x developers working in
parallel, which may not be feasible for all tasks.
```

### Outdated Tech
```
⚠️ Tech Stack Warning: 'Jquery' is outdated/deprecated. Consider using
Vanilla JavaScript, React, Vue, or Angular (for UI interactivity) instead
for better performance, security, and maintainability.
```

### Conflicting Frameworks
```
⚠️ Tech Stack Warning: Multiple frontend frameworks detected (react and angular).
This may indicate confusion in requirements. Typically, projects use one primary
framework for frontend frameworks. Please clarify which framework should be used.
```

### Multiple Issues
Example with 12 deliverables, $20k budget, 2 month timeline, outdated tech:
```
⚠️  Found 7 warning(s):

1. Budget may be insufficient for 12 deliverables
2. Budget-Hours Mismatch (needs ~$120k, provided $20k)
3. Timeline too aggressive (needs 7.5 months, provided 2 months)
4. jQuery is outdated
5. AngularJS is outdated
6. Backbone is outdated
7. PHP 5 is outdated
```

### No Issues
```
✓ No issues detected - proposal looks reasonable!
```

## Test Results

All test scenarios passed:

✅ Budget too high (2 deliverables, $100k) → Detected
✅ Budget too low (12 deliverables, $25k) → Detected
✅ Budget-hours mismatch (1000 hrs, $30k budget) → Detected
✅ Budget-hours mismatch (100 hrs, $150k budget) → Detected
✅ Timeline too aggressive (1000 hrs in 4 weeks) → Detected
✅ Timeline too long (150 hrs in 8 months) → Detected
✅ Outdated tech (Flash, jQuery, PHP 5) → Detected
✅ Conflicting frameworks (React + Angular) → Detected
✅ Multiple issues (budget + timeline + tech) → All detected
✅ Reasonable project (no issues) → No false positives
✅ Python 2, Node.js 8 detection → Works
✅ Budget from cost_range → Extracts correctly

## Helper Functions

### `_extract_budget_number(budget_str)`
Extracts numeric budget from strings:
- "$50,000 - $75,000" → 62,500
- "50k-75k" → 62,500
- Handles k/m suffixes
- Returns average if range

### `_extract_timeline_months(timeline_str)`
Converts timeline to months:
- "3 months" → 3.0
- "6 weeks" → 1.5
- "1.5 months" → 1.5

### `_check_budget_scope_mismatch(state, warnings)`
Checks all budget-related issues

### `_check_timeline_reality(state, warnings)`
Checks all timeline-related issues

### `_check_tech_stack_issues(state, warnings)`
Checks all tech stack issues

## Integration

To integrate into the workflow:

1. **Add to main.py graph:**
```python
from nodes.sanity_check import sanity_check_node

# Add node
workflow.add_node("sanity_check", sanity_check_node)

# Add edge after calculator, before generation
workflow.add_edge("calculator", "sanity_check")
workflow.add_edge("sanity_check", "generation")
```

2. **Update generation node to include warnings:**
```python
# In generation_node, check for warnings
sanity_warnings = state.get('sanity_warnings')
if sanity_warnings:
    # Include warnings in proposal or display separately
    warnings_section = "\n\n## Potential Concerns\n\n"
    for warning in sanity_warnings:
        warnings_section += f"- {warning}\n"
```

## Error Handling

The sanity check node is designed to never fail the pipeline:
- All checks are wrapped in try-except
- If an error occurs, adds a single warning about the error
- Returns state with warnings (or error message)
- Pipeline continues even if sanity check fails

## Customization

To adjust thresholds:

**Budget checks:**
```python
# Line ~120: Change thresholds
if num_deliverables < 3 and budget > 80000:  # Adjust 3 and 80000
if num_deliverables > 10 and budget < 30000:  # Adjust 10 and 30000
```

**Timeline checks:**
```python
# Line ~185: Change thresholds
if hours > 800 and timeline_months < 2:  # Adjust 800 and 2
if hours < 200 and timeline_months > 6:  # Adjust 200 and 6
```

**Tech stack:**
```python
# Line ~219: Add/remove outdated tech
outdated_tech = {
    'your_tech': 'modern_alternative',
    ...
}
```

## Files Modified/Created

1. **src/state.py** - Added `sanity_warnings` field
2. **src/nodes/sanity_check.py** - New file with all sanity check logic
3. **test_sanity_check.py** - Comprehensive test suite

## Benefits

- ✅ Catches unrealistic expectations early
- ✅ Provides actionable suggestions
- ✅ Helps identify scope/budget misalignment
- ✅ Flags outdated/problematic tech choices
- ✅ Improves proposal quality
- ✅ Reduces back-and-forth with clients
- ✅ Sets realistic expectations
- ✅ Non-blocking (warnings only, doesn't fail pipeline)
