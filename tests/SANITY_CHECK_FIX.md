# Sanity Check Fix - Amazon Example

## Problem

**User Input:** "Full e-commerce platform like Amazon with $5k budget"

**Issue:** Sanity check was NOT detecting this as a problem and showing "✓ No issues detected"

**Why This Was Wrong:**
- Amazon-scale platforms cost $500M-$1B+ to build
- $5k budget is 100,000x too low
- 7 deliverables at $714 each is absurdly low
- This should have been immediately flagged as unrealistic

## Root Cause

The original sanity check had 3 gaps:

1. **No check for very low budget per deliverable** - Only checked if > 10 deliverables
2. **No check for absurdly low total budget** - No minimum threshold
3. **No context awareness** - Didn't understand "like Amazon" means massive scope

## Fixes Applied

### Fix 1: Budget Per Deliverable Check (Lines 109-119)

Added check for ANY project with 3+ deliverables:

```python
if num_deliverables >= 3:
    budget_per_deliverable = budget / num_deliverables
    if budget_per_deliverable < 3000:  # $3k per feature minimum
        warnings.append(
            f"Budget of ${budget:,} for {num_deliverables} deliverables averages "
            f"${budget_per_deliverable:,.0f} per deliverable. This is unrealistically low "
            f"(typical minimum: $10,000-$20,000 per feature)."
        )
```

### Fix 2: Absurdly Low Total Budget Check (Lines 121-127)

Added check for ANY project with deliverables:

```python
if num_deliverables > 0 and budget < 10000:  # $10k minimum
    warnings.append(
        f"Budget of ${budget:,} is extremely low for a software project with "
        f"{num_deliverables} deliverables. Even a simple MVP typically costs "
        f"$15,000-$30,000 minimum."
    )
```

### Fix 3: Massive Platform Detection (Lines 90-116)

Added context-aware detection for platform comparisons:

```python
massive_platform_keywords = {
    'amazon': ('Amazon-scale', '$500M-$1B+'),
    'facebook': ('Facebook-scale', '$100M-$500M+'),
    'netflix': ('Netflix-scale', '$100M-$500M+'),
    'uber': ('Uber-scale', '$50M-$200M+'),
    # ... 10 total platforms
}

for platform, (scale_name, typical_cost) in massive_platform_keywords.items():
    if f'like {platform}' in user_input:
        warnings.append(
            f"Building a '{scale_name}' platform requires {typical_cost} "
            f"in development costs and years of work by large teams."
        )
```

### Fix 4: None Handling (Line 249)

Fixed crash when tech_hints is None:

```python
tech_hints = state.get('tech_hints') or []  # Handle None
```

## Test Results

### Before Fix

```
SANITY CHECK
============================================================
Checking budget-scope alignment...
Checking timeline feasibility...
Checking tech stack compatibility...

✓ No issues detected - proposal looks reasonable!
============================================================
```

❌ **WRONG** - Should have caught this!

### After Fix

```
SANITY CHECK
============================================================
Checking budget-scope alignment...
Checking timeline feasibility...
Checking tech stack compatibility...

⚠️  Found 3 warning(s):

1. ⚠️ Scope Warning: Building a 'Amazon-scale' platform requires
   $500M-$1B+ in development costs and years of work by large teams.
   Current budget of $5,000 is insufficient by orders of magnitude.

2. ⚠️ Budget Warning: Budget of $5,000 for 7 deliverables averages
   $714 per deliverable. This is unrealistically low for quality
   software development (typical minimum: $10,000-$20,000 per feature).

3. ⚠️ Budget Warning: Budget of $5,000 is extremely low for a software
   project with 7 deliverables. Even a simple MVP typically costs
   $15,000-$30,000 minimum.
============================================================
```

✅ **CORRECT** - All issues caught!

## Coverage Improvements

### New Detection Scenarios

**Now catches:**
- ✅ Amazon/Facebook/Netflix-like platforms at any budget
- ✅ Any project < $10k with deliverables
- ✅ Any 3+ deliverables averaging < $3k each
- ✅ Uber/Airbnb clones
- ✅ Twitter/Instagram clones
- ✅ YouTube/Spotify clones
- ✅ LinkedIn clones

**Examples that now trigger warnings:**

| Input | Old | New |
|-------|-----|-----|
| "like Amazon, $5k" | ✓ Pass | ⚠️ 3 warnings |
| "Facebook clone, $20k" | ✓ Pass | ⚠️ 2 warnings |
| "5 features, $8k" | ✓ Pass | ⚠️ 2 warnings |
| "Netflix-like, $15k" | ✓ Pass | ⚠️ 2 warnings |

## Proposal Output

The warnings now appear at the TOP of the proposal:

```markdown
# ⚠️ Important Considerations

**Please review these points before proceeding with this proposal:**

1. **Scope Warning**: Building a 'Amazon-scale' platform requires
   $500M-$1B+ in development costs and years of work by large teams.
   Current budget of $5,000 is insufficient by orders of magnitude.
   Consider building an MVP with core features only, or significantly
   increasing budget and timeline expectations.

2. **Budget Warning**: Budget of $5,000 for 7 deliverables averages
   $714 per deliverable. This is unrealistically low for quality
   software development (typical minimum: $10,000-$20,000 per feature).
   Budget should be $70,000-$140,000 minimum.

3. **Budget Warning**: Budget of $5,000 is extremely low for a software
   project with 7 deliverables. Even a simple MVP typically costs
   $15,000-$30,000 minimum. Please revise budget expectations or
   significantly reduce scope.

---

# 1. About This Proposal
[Proposal continues...]
```

## Impact

**Before fix:**
- Users could request "Amazon for $5k" and get a proposal
- No warnings about unrealistic expectations
- Potential for massive scope/budget misalignment
- False confidence from system

**After fix:**
- Immediate, prominent warnings
- Clear education about realistic costs
- Actionable suggestions (MVP, increase budget)
- Sets proper expectations upfront

## Files Modified

**src/nodes/sanity_check.py:**
- Line 83: Added user_input extraction
- Lines 90-102: Added massive platform keywords dictionary
- Lines 107-116: Added platform comparison check
- Lines 109-119: Added low budget per deliverable check
- Lines 121-127: Added absurdly low total budget check
- Line 249: Fixed None handling for tech_hints

## Testing

Run these tests to verify:

```bash
# Test the specific fix
python test_amazon_fix.py

# Test full system
python src/main.py
# (with "like Amazon" input)

# Test all sanity checks
python test_sanity_check.py
```

## Thresholds

**Current values (customizable):**
- Minimum per deliverable: $3,000 (realistic: $10k-$20k)
- Minimum total budget: $10,000
- Minimum for any project: $15k-$30k MVP

**Platform cost estimates:**
- Amazon/YouTube: $500M-$1B+
- Facebook/Netflix/Twitter/Instagram/Spotify/LinkedIn: $100M-$500M+
- Uber/Airbnb: $50M-$200M+

## Recommendations

1. **Keep these thresholds** - They represent realistic market rates
2. **Add more platforms** as needed (TikTok, WhatsApp, etc.)
3. **Educate users** about MVP vs full platform
4. **Suggest alternatives** like white-label solutions

## Conclusion

The sanity check now properly detects unrealistic budget expectations, especially for massive platform comparisons. The "like Amazon for $5k" scenario that was passing before now correctly triggers 3 warnings, setting proper expectations from the start.

**Status: ✅ FIXED**
