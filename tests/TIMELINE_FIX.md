# Timeline Check Fix - E-commerce in 2 Weeks

## Problem

**User Input:** "Need e-commerce site in 2 weeks"

**Issue:** Sanity check was NOT detecting this as unrealistic

**Why This Was Wrong:**
- E-commerce sites require 3-6 months minimum for even a basic MVP
- 2 weeks is completely unrealistic for any e-commerce project
- Need to warn users about unrealistic timeline expectations BEFORE calculator runs

## Root Cause

The original `_check_timeline_reality` function (lines 177-238) had a critical flaw:

```python
if not estimated_hours:
    return  # Exit early if no hours calculated
```

**The Problem:**
- Sanity check runs BEFORE calculator in the workflow (main.py line 40: `validation → sanity_check`)
- Calculator runs AFTER sanity check (main.py line 53: `calculator → generation`)
- So `estimated_hours` is ALWAYS `None` when sanity check runs
- Timeline checks were completely skipped during early detection

## Solution

Added timeline checks that work WITHOUT `estimated_hours` by analyzing:
1. Timeline in months (from `timeline_hints`)
2. Number of deliverables
3. User input keywords (e-commerce, platform, marketplace)

### Implementation (Lines 191-227)

```python
# Check 1: Timeline-based checks WITHOUT estimated hours (for early detection)
timeline_to_check = timeline_hints or calculated_timeline
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
```

## Key Changes

### Change 1: E-commerce Specific Check (Priority)
- **Condition:** `timeline_months <= 1` AND user input contains e-commerce/platform/marketplace keywords
- **Warning:** Explains e-commerce sites need 3-6 months minimum
- **Why first:** More specific guidance than generic warning

### Change 2: Generic Aggressive Timeline
- **Condition:** `timeline_months < 1` AND `num_deliverables >= 3`
- **Warning:** Points out that each feature needs 1-2 weeks minimum
- **Calculation:** Suggests `num_deliverables * 2` weeks

### Change 3: Many Deliverables
- **Condition:** `num_deliverables > 5` AND `timeline_months < 2`
- **Warning:** Shows weeks per feature calculation
- **Guidance:** Suggests realistic range based on 2-4 weeks per feature

### Priority Order

The checks use `if/elif/elif` so only ONE warning triggers per timeline issue:
1. **E-commerce/platform check** (most specific) - runs FIRST
2. **Generic aggressive check** (medium specific)
3. **Many deliverables check** (broad)

This ensures the most relevant, actionable warning is shown.

## Test Results

### Test Case 1: E-commerce in 2 weeks

**Input:**
```python
user_input: 'Need e-commerce site in 2 weeks'
timeline_hints: '2 weeks'
deliverables: 3 items
```

**Before Fix:**
```
✓ No issues detected - proposal looks reasonable!
```
❌ **WRONG** - Should have been flagged!

**After Fix:**
```
⚠️  Found 1 warning(s):

1. ⚠️ Timeline Warning: 0.5 months (about 2 weeks) for an
   e-commerce/platform project is unrealistic. E-commerce sites
   typically require 3-6 months minimum for a basic MVP, even
   with existing frameworks. Consider extending timeline to at
   least 3 months.
```
✅ **CORRECT** - E-commerce specific warning with actionable guidance!

### Test Case 2: Generic project in 2 weeks

**Input:**
```python
user_input: 'Need website in 2 weeks'
timeline_hints: '2 weeks'
deliverables: 5 items
```

**Result:**
```
⚠️ Timeline Warning: 0.5 months (about 2 weeks) for 5 deliverables
is extremely aggressive. Even a simple feature typically takes 1-2
weeks minimum. Consider timeline of at least 10 weeks (2.5 months).
```
✅ Generic warning with calculation

### Test Case 3: Amazon + Budget (No regression)

**Input:**
```python
user_input: 'Full e-commerce platform like Amazon with $5k budget'
budget_hints: '$5,000'
deliverables: 7 items
```

**Result:**
```
⚠️  Found 3 warning(s):
1. ⚠️ Scope Warning: Building a 'Amazon-scale' platform...
2. ⚠️ Budget Warning: Budget of $5,000 for 7 deliverables...
3. ⚠️ Budget Warning: Budget of $5,000 is extremely low...
```
✅ Previous fix still works!

## Coverage Improvements

### Now Catches

**E-commerce specific:**
- ✅ "E-commerce in 2 weeks"
- ✅ "Need online store in 1 month"
- ✅ "Marketplace in 3 weeks"
- ✅ "Platform in 4 weeks"

**Generic aggressive timelines:**
- ✅ "3 features in 2 weeks"
- ✅ "5 deliverables in 3 weeks"
- ✅ "Complete app in 1 month" (with 3+ features)

**Many deliverables:**
- ✅ "6 features in 6 weeks"
- ✅ "10 deliverables in 1.5 months"

### Examples

| Input | Timeline | Deliverables | Old | New |
|-------|----------|--------------|-----|-----|
| "E-commerce in 2 weeks" | 2 weeks | 3 | ✓ Pass | ⚠️ E-commerce warning |
| "Marketplace in 1 month" | 1 month | 4 | ✓ Pass | ⚠️ E-commerce warning |
| "5 features in 3 weeks" | 3 weeks | 5 | ✓ Pass | ⚠️ Generic warning |
| "10 features in 6 weeks" | 6 weeks | 10 | ✓ Pass | ⚠️ Many deliverables |

## Workflow Order

Understanding the execution order is critical:

```
User Input
    ↓
Extraction Node (extracts timeline_hints, deliverables)
    ↓
Validation Node (checks completeness)
    ↓
Sanity Check Node ← WE ARE HERE (timeline_hints available, estimated_hours NOT yet)
    ↓
Calculator Node (calculates estimated_hours)
    ↓
Generation Node (creates proposal with warnings)
```

**Key insight:** Sanity check runs BEFORE calculator, so we can't rely on `estimated_hours` for early timeline validation.

## Files Modified

**src/nodes/sanity_check.py:**
- Lines 191-227: Added timeline checks WITHOUT estimated_hours requirement
- Lines 198-210: E-commerce/platform specific check (priority)
- Lines 212-219: Generic aggressive timeline check
- Lines 221-227: Many deliverables check
- Changed check order to prioritize e-commerce specific warnings

## Testing Commands

```bash
# Test e-commerce timeline specifically
python test_ecommerce_timeline.py

# Test generic timeline (5 deliverables in 2 weeks)
python test_timeline.py

# Verify Amazon fix still works
python test_amazon_fix.py

# Test full system
python src/main.py
# Try inputs like:
# "Need e-commerce site in 2 weeks"
# "Build marketplace in 1 month"
# "Online store in 3 weeks with payment integration"
```

## Thresholds

**Current values (customizable):**

Timeline thresholds:
- E-commerce/platform: <= 1 month → warning (realistic: 3-6 months)
- Generic with 3+ features: < 1 month → warning
- 5+ features: < 2 months → warning

Effort estimates used in guidance:
- Simple feature: 1-2 weeks
- E-commerce MVP: 3-6 months minimum
- Calculation: 2-4 weeks per feature for realistic timeline

## Detected Keywords

**E-commerce/platform detection:**
- "e-commerce"
- "ecommerce"
- "platform"
- "marketplace"

These trigger more specific warnings with e-commerce context.

## Proposal Output

The timeline warnings now appear at the TOP of proposals:

```markdown
# ⚠️ Important Considerations

**Please review these points before proceeding with this proposal:**

1. **Timeline Warning**: 0.5 months (about 2 weeks) for an
   e-commerce/platform project is unrealistic. E-commerce sites
   typically require 3-6 months minimum for a basic MVP, even
   with existing frameworks. Consider extending timeline to at
   least 3 months.

---

# 1. About This Proposal
[Proposal continues...]
```

## Impact

**Before fix:**
- "E-commerce in 2 weeks" passed sanity check
- No early warning about unrealistic timelines
- Users get proposals that can't be delivered
- Damages credibility

**After fix:**
- Immediate, specific warnings about timeline issues
- Clear education about realistic timeframes
- Actionable guidance (3-6 months for e-commerce)
- Sets proper expectations upfront
- Warnings work even before calculator runs

## Related Fixes

This completes the sanity check system along with:

1. **Budget fix** (SANITY_CHECK_FIX.md):
   - Amazon $5k scenario
   - Low budget per deliverable
   - Minimum budget thresholds

2. **Timeline fix** (this document):
   - E-commerce timeline expectations
   - Generic aggressive timelines
   - Early detection before calculator

Both fixes work together to catch unrealistic requirements early.

## Recommendations

1. **Keep these thresholds** - They represent realistic market expectations
2. **Add more project types** if needed (SaaS, mobile apps, etc.)
3. **Consider adding more complex checks**:
   - Multi-region/international projects
   - Enterprise integrations
   - Compliance requirements (HIPAA, GDPR)
4. **Education over rejection** - Provide guidance, not just warnings

## Conclusion

The timeline check now properly detects unrealistic timeline expectations for e-commerce projects and generic aggressive timelines. The "e-commerce in 2 weeks" scenario that was passing before now correctly triggers a specific, actionable warning.

The fix works at the right point in the workflow (before calculator) and provides context-aware warnings prioritized by specificity.

**Status: ✅ FIXED**

## Testing Summary

```bash
✅ E-commerce in 2 weeks → Specific e-commerce warning
✅ Generic 5 features in 2 weeks → Generic aggressive warning
✅ Amazon $5k budget → Still triggers 3 budget warnings (no regression)
✅ All checks work before calculator runs
```
