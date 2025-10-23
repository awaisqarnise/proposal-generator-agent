# Workflow Optimization Note

## Current Flow (main.py)

```
extraction → validation → sanity_check → calculator → generation
```

## Issue with Current Flow

The **sanity_check** runs **before calculator**, which means:

❌ Can't check budget-hours mismatch (no `estimated_hours` yet)
❌ Can't check timeline-hours mismatch (no `estimated_hours` yet)
✅ Can check budget-scope based on deliverable count only
✅ Can check timeline hints vs deliverable count
✅ Can check tech stack issues

## Recommended Optimal Flow

```
extraction → validation → calculator → sanity_check → generation
```

### Benefits:

✅ All sanity checks can run (budget, timeline, tech)
✅ Can compare calculated hours with budget/timeline
✅ More accurate warnings
✅ Better budget-hours mismatch detection

## To Update main.py

Change lines 40-50 from:

```python
workflow.add_edge("validation", "sanity_check")

workflow.add_conditional_edges(
    "sanity_check",
    route_after_validation,
    {
        "generation": "calculator",
        "questions_only" : "questions_only"
    }
)

workflow.add_edge("calculator", "generation")
```

To:

```python
workflow.add_conditional_edges(
    "validation",
    route_after_validation,
    {
        "generation": "calculator",
        "questions_only" : "questions_only"
    }
)

workflow.add_edge("calculator", "sanity_check")
workflow.add_edge("sanity_check", "generation")
```

## Comparison

### Current Flow (sanity_check before calculator)

**Can Check:**
- Budget too high/low based on deliverable count
- Timeline mentioned in hints vs deliverable count
- Tech stack issues
- Outdated technologies

**Cannot Check:**
- Budget vs calculated hours mismatch
- Timeline vs calculated hours mismatch
- Whether timeline is realistic for estimated effort

### Optimal Flow (sanity_check after calculator)

**Can Check:**
- ✅ Everything from current flow, PLUS:
- ✅ Budget vs calculated hours mismatch
- ✅ Timeline vs calculated hours mismatch
- ✅ Realistic timeline assessment
- ✅ Required team size for timeline

## Current State Behavior

With the current flow, sanity_check will:

1. ✅ Detect if budget seems high for few deliverables
2. ✅ Detect if budget seems low for many deliverables
3. ❌ **Cannot** compare budget with estimated hours (hours not calculated yet)
4. ✅ Detect if timeline mentions weeks/months but many deliverables
5. ❌ **Cannot** calculate if timeline is realistic for hours (hours not calculated yet)
6. ✅ Detect outdated tech
7. ✅ Detect conflicting frameworks

## Recommendation

**Move sanity_check to after calculator** for best results.

The current placement still provides value but misses important checks that require calculated hours.

## Alternative: Partial Sanity Check

If the current flow must be maintained, consider:

1. **Early sanity check** (before calculator) - Tech stack issues only
2. **Late sanity check** (after calculator) - Budget/timeline issues

This would require creating two sanity check nodes:
- `sanity_check_tech` (before calculator)
- `sanity_check_estimates` (after calculator)

## Impact on Generation

Regardless of placement, the generation node will include any warnings that were detected. Moving sanity_check after calculator just means **more comprehensive warnings** will be available.

## Testing Both Flows

### Test Current Flow
```bash
python src/main.py
# Will see tech warnings, basic budget/timeline warnings
```

### Test Optimal Flow
Update main.py as shown above, then:
```bash
python src/main.py
# Will see all warnings including budget-hours mismatches
```

## Decision

The choice depends on requirements:

**Keep current flow if:**
- Want to flag issues as early as possible
- Tech stack issues are the primary concern
- Budget-hours comparison is less important

**Use optimal flow if:**
- Want comprehensive warnings
- Budget-hours mismatch detection is important
- Timeline feasibility based on hours is critical

## My Recommendation

**Switch to optimal flow** (sanity_check after calculator) because:

1. Budget-hours mismatch is crucial for setting expectations
2. Timeline feasibility requires knowing estimated hours
3. Tech warnings will still work fine after calculator
4. Minimal code change (just reorder edges)
5. More complete warning set for users

The user has already integrated sanity_check before calculator, so it will work but with reduced functionality for budget/timeline checks.
