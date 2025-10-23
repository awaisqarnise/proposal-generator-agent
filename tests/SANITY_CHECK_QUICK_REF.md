# Sanity Check - Quick Reference

## What It Does

Analyzes proposals and flags:
- 💰 Budget-scope mismatches
- ⏱️ Unrealistic timelines
- 🔧 Tech stack issues

## Usage

```python
from nodes.sanity_check import sanity_check_node

state = sanity_check_node(state)
warnings = state.get('sanity_warnings')
```

## Warning Triggers

### Budget
| Condition | Warning |
|-----------|---------|
| < 3 deliverables + > $80k budget | Budget too high |
| > 10 deliverables + < $30k budget | Budget too low |
| Budget < 60% of expected | Insufficient |
| Budget > 150% of expected | Too high |

### Timeline
| Condition | Warning |
|-----------|---------|
| > 800 hrs + < 2 months | Too aggressive |
| < 200 hrs + > 6 months | Too long |
| < 40% expected | Too aggressive |
| > 250% expected | Too long |

### Tech Stack
| Issue | Action |
|-------|--------|
| Flash, jQuery, AngularJS | Flag as outdated |
| React + Angular | Flag as conflicting |
| Node < 10, React < 16 | Flag as old version |
| Python 2, PHP 5 | Flag as deprecated |

## Quick Test

```bash
python test_sanity_check.py
```

## Integration (3 Options)

**Option 1: Add to Workflow**
```python
workflow.add_node("sanity_check", sanity_check_node)
workflow.add_edge("calculator", "sanity_check")
```

**Option 2: Check After Calculation**
```python
state = sanity_check_node(state)
if state['sanity_warnings']:
    # Handle warnings
```

**Option 3: Display Only**
```python
if result.get('sanity_warnings'):
    print("Warnings:", result['sanity_warnings'])
```

## Customize

**Budget thresholds:** `sanity_check.py` line ~120
**Timeline thresholds:** `sanity_check.py` line ~185
**Outdated tech list:** `sanity_check.py` line ~219

## Files

- `src/state.py` - Schema with sanity_warnings
- `src/nodes/sanity_check.py` - Implementation
- `test_sanity_check.py` - Test suite
- `SANITY_CHECK_FEATURE.md` - Full docs

## Example Output

```
⚠️  Found 3 warning(s):

1. Budget may be insufficient for 12 deliverables
2. Timeline too aggressive (needs 7.5 months, provided 2)
3. jQuery is outdated → Use React, Vue, or Angular
```

## Non-Blocking

✅ Never fails pipeline
✅ Returns warnings only
✅ Graceful error handling
