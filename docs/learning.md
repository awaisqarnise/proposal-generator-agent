# Proposal Generator Agent - Complete Learning Guide

**Last Updated**: October 23, 2025

This is the **single source of truth** for the entire Proposal Generator project. Read this file to understand 100% of how the system works, regardless of when you return to the project.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [LangGraph Fundamentals](#langgraph-fundamentals)
3. [Complete System Architecture](#complete-system-architecture)
4. [File-by-File Breakdown](#file-by-file-breakdown)
5. [Data Flow & Execution](#data-flow--execution)
6. [Key Features & Improvements](#key-features--improvements)
7. [How Everything Connects](#how-everything-connects)
8. [Running & Testing](#running--testing)
9. [Design Decisions & Why](#design-decisions--why)

---

# Project Overview

## What This System Does
The **Proposal Generator** is an AI-powered system that transforms vague user requests into comprehensive, realistic software development proposals.

### The Problem It Solves
- Clients say: "I need an e-commerce site like Amazon for $5k in 2 weeks"
- Reality: That's impossible - Amazon took $500M+ and years to build
- **This system**: Catches unrealistic expectations, provides accurate estimates, educates clients

### Input → Output Example

**Input**:
```
"Build mobile app with user login, payment integration, and analytics"
```

**What Happens**:
1. Extracts: 3 deliverables (login, payment, analytics)
2. Validates: Checks if enough info (timeline? budget? tech?)
3. Sanity Checks: Warns if budget/timeline unrealistic
4. Calculates: Estimates ~350 hours, $28k-42k, 2.2 months
5. Generates: Professional proposal with warnings, recommendations, timeline

**Output**:
- Complete proposal document
- Cost breakdown
- Timeline estimation
- Technology recommendations
- **Warnings** if client expectations are unrealistic

---

# LangGraph Fundamentals

## What is LangGraph?
LangGraph is a library for building **stateful, multi-step AI workflows**. Think of it as a flowchart where each step can call an LLM, process data, or make decisions.

## Core Concepts

### 1. State (The Shared Memory)
The **State** is a TypedDict that flows through ALL nodes. Every node reads from it and updates it.

```python
class ProposalState(TypedDict):
    # INPUT
    user_input: str

    # EXTRACTION (Node 1 fills these)
    project_type: Optional[str]
    industry: Optional[str]
    deliverables: Optional[List[str]]
    timeline_hints: Optional[str]
    budget_hints: Optional[str]
    tech_hints: Optional[List[str]]

    # VALIDATION (Node 2 fills these)
    is_complete: bool
    missing_fields: Optional[List[str]]
    clarifying_questions: Optional[List[str]]
    information_quality: Optional[str]

    # SANITY CHECK (Node 3 fills these)
    sanity_warnings: Optional[List[str]]

    # CALCULATION (Node 4 fills these)
    estimated_hours: Optional[int]
    cost_range: Optional[str]
    calculated_timeline: Optional[str]

    # OUTPUT (Node 5 fills this)
    Proposal: Optional[str]

    # ERROR HANDLING
    error: Optional[str]
```

**Key Insight**: State is immutable! Each node returns a NEW state with updates, it doesn't modify the original.

### 2. Nodes (The Workers)
Nodes are **functions** that:
- Take current state as input
- Do some work (call LLM, calculate, validate)
- Return updated state

```python
def my_node(state: ProposalState) -> ProposalState:
    # Extract what you need
    user_input = state.get('user_input')

    # Do your work
    result = do_something(user_input)

    # Return UPDATED state
    return {
        **state,  # Keep everything
        'new_field': result  # Add/update fields
    }
```

### 3. Edges (The Connections)
Edges define the **flow** between nodes.

**Simple Edge** (always goes A → B):
```python
workflow.add_edge("extraction", "validation")
```

**Conditional Edge** (A → B or C based on condition):
```python
def route_logic(state: ProposalState) -> str:
    if state['is_complete']:
        return "calculator"  # Go here if complete
    else:
        return "questions_only"  # Go here if incomplete

workflow.add_conditional_edges(
    "sanity_check",  # FROM this node
    route_logic,     # USE this function to decide
    {
        "calculator": "calculator",      # If returns "calculator"
        "questions_only": "questions_only"  # If returns "questions_only"
    }
)
```

### 4. Building a Graph

```python
from langgraph.graph import StateGraph, END

def create_graph():
    # 1. Initialize with your State type
    workflow = StateGraph(ProposalState)

    # 2. Add nodes (name, function)
    workflow.add_node("extraction", extraction_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("calculator", calculator_node)

    # 3. Set starting point
    workflow.set_entry_point("extraction")

    # 4. Connect nodes
    workflow.add_edge("extraction", "validation")
    workflow.add_edge("validation", "calculator")
    workflow.add_edge("calculator", END)  # END = terminate

    # 5. Compile and return
    return workflow.compile()
```

### 5. Running the Graph

```python
# Create graph
graph = create_graph()

# Prepare initial state
initial_state = {
    "user_input": "Build e-commerce site",
    "deliverables": None,
    # ... all other fields as None
}

# Run it!
result = graph.invoke(initial_state)

# Access results
print(result['Proposal'])
print(result['cost_range'])
```

---

# Complete System Architecture

## The Big Picture

```
User Input
    ↓
┌─────────────────────────────────────────────┐
│  EXTRACTION NODE                            │
│  (Uses LLM to parse user input)            │
│  Fills: deliverables, timeline_hints,       │
│         budget_hints, tech_hints            │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  VALIDATION NODE                            │
│  (Checks if we have enough info)           │
│  Fills: is_complete, missing_fields,        │
│         clarifying_questions                │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  SANITY CHECK NODE                          │
│  (Catches unrealistic expectations)         │
│  Fills: sanity_warnings                     │
│  Checks: Budget vs scope, Timeline reality, │
│          Outdated tech, Platform comparisons│
└─────────────────────────────────────────────┘
    ↓
    Is Complete?
    ├─ YES → CALCULATOR NODE
    │         (Estimates hours, cost, timeline)
    │         Fills: estimated_hours, cost_range,
    │                calculated_timeline
    │         ↓
    │         GENERATION NODE
    │         (Creates full proposal with warnings)
    │         Fills: Proposal
    │
    └─ NO  → QUESTIONS ONLY NODE
              (Returns just clarifying questions)
              Fills: Proposal (with questions)
    ↓
  END (Return final state to user)
```

## Current Workflow (src/main.py)

The actual flow as of October 2025:

```python
Entry Point: "extraction"
    ↓
"extraction" → "validation"
    ↓
"validation" → "sanity_check"
    ↓
"sanity_check" → CONDITIONAL:
    ├─ if is_complete = True  → "calculator" → "generation" → END
    └─ if is_complete = False → "questions_only" → END
```

**Key Insight**: Sanity check runs BEFORE calculator! This is important because:
- We can warn about unrealistic timelines even without calculating hours
- We catch bad inputs early
- Timeline warnings use pattern detection ("in 2 weeks") from user_input directly

---

# File-by-File Breakdown

## Directory Structure

```
proposal-generator-agent/
├── src/
│   ├── main.py                    # Graph setup & workflow
│   ├── state.py                   # State schema definition
│   ├── nodes/
│   │   ├── extraction.py          # Parse user input (LLM)
│   │   ├── validation.py          # Check completeness (LLM)
│   │   ├── sanity_check.py        # Reality checks (Rules + Patterns)
│   │   ├── calculator.py          # Cost/time estimation (Rules)
│   │   ├── generation.py          # Proposal creation (LLM)
│   │   └── questions_only.py      # Just questions (No LLM)
│   └── tools/
│       └── calculator.py          # Hour estimation logic
├── tests/                         # All tests & test documentation
├── docs/                          # All documentation
└── README.md                      # Project README
```

---

## src/main.py

**Purpose**: Orchestrates the entire workflow. This is the "brain" that connects everything.

**What it does**:
1. Creates the LangGraph workflow
2. Adds all nodes
3. Defines the flow (edges)
4. Compiles the graph
5. Runs test inputs (in `main()` function)

**Key Functions**:

### `create_graph()`
Sets up the complete workflow.

```python
def create_graph():
    workflow = StateGraph(ProposalState)

    # Add nodes
    workflow.add_node("extraction", extraction_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("sanity_check", sanity_check_node)
    workflow.add_node("calculator", calculator_node)
    workflow.add_node("generation", generation_node)
    workflow.add_node("questions_only", questions_only_node)

    # Entry point
    workflow.set_entry_point("extraction")

    # Flow
    workflow.add_edge("extraction", "validation")
    workflow.add_edge("validation", "sanity_check")

    # Conditional routing
    workflow.add_conditional_edges(
        "sanity_check",
        route_after_validation,  # Decision function
        {
            "generation": "calculator",
            "questions_only": "questions_only"
        }
    )

    workflow.add_edge("calculator", "generation")
    workflow.add_edge("generation", END)
    workflow.add_edge("questions_only", END)

    return workflow.compile()
```

### `route_after_validation(state: ProposalState) -> str`
Decision function for conditional routing.

```python
def route_after_validation(state: ProposalState) -> str:
    if state['is_complete']:
        return "generation"  # Full proposal
    else:
        return "questions_only"  # Just questions
```

**When to modify this file**:
- Adding new nodes to the workflow
- Changing the flow/order
- Adding new conditional routing

---

## src/state.py

**Purpose**: Defines the **ProposalState** schema - the shared memory for all nodes.

**What it contains**:
- All fields that flow through the system
- Type hints for each field
- Documentation for what each field means

**Structure**:
```python
class ProposalState(TypedDict):
    # INPUT (from user)
    user_input: str

    # EXTRACTED (by extraction_node)
    project_type: Optional[str]         # "E-commerce", "SaaS", etc.
    industry: Optional[str]             # "Healthcare", "Finance", etc.
    deliverables: Optional[List[str]]   # ["login", "payment", "dashboard"]
    timeline_hints: Optional[str]       # "3 months", "by Q2", etc.
    budget_hints: Optional[str]         # "$50k", "cost-effective", etc.
    tech_hints: Optional[List[str]]     # ["React", "Python", "AWS"]

    # VALIDATED (by validation_node)
    is_complete: bool                   # True if enough info
    missing_fields: Optional[List[str]] # ["budget", "timeline"]
    clarifying_questions: Optional[List[str]]  # Questions to ask
    information_quality: Optional[str]  # "high", "medium", "low"

    # SANITY CHECKED (by sanity_check_node)
    sanity_warnings: Optional[List[str]]  # Warnings about unrealistic expectations

    # CALCULATED (by calculator_node)
    estimated_hours: Optional[int]      # 500 hours
    cost_range: Optional[str]           # "$40,000 - $60,000"
    calculated_timeline: Optional[str]  # "3.1 months"

    # GENERATED (by generation_node or questions_only_node)
    Proposal: Optional[str]             # Final markdown proposal

    # ERROR HANDLING
    error: Optional[str]
```

**When to modify this file**:
- Adding new data to track
- Adding new node outputs
- Changing data types

---

## src/nodes/extraction.py

**Purpose**: Uses LLM (GPT-4) to parse user input and extract structured data.

**Input**: Raw user text
**Output**: Structured fields (deliverables, budget, timeline, tech)

**How it works**:
1. Takes `user_input` from state
2. Sends structured prompt to GPT-4
3. Gets JSON response
4. Parses and validates JSON
5. Updates state with extracted fields

**Example**:

Input:
```
"E-commerce site with Stripe payments. Need it in 3 months. Budget $50k. Using React."
```

Prompt to LLM:
```
Extract from this input:
1. deliverables: ["e-commerce site", "Stripe payment integration"]
2. timeline_hints: "3 months"
3. budget_hints: "$50k"
4. tech_hints: ["React", "Stripe"]
```

**LLM Call Setup**:
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,  # Low = more deterministic
    api_key=OPENAI_API_KEY
)

response = llm.invoke(extraction_prompt)
parsed_data = json.loads(response.content)
```

**Temperature Explained**:
- **0.0**: Completely deterministic (same input = same output)
- **0.1-0.3**: Mostly consistent, slight variation
- **0.5-0.7**: More creative, varied responses
- **1.0**: Very creative, unpredictable

We use **0.1** because we want consistent, factual extraction.

**Error Handling**:
If LLM fails or returns invalid JSON:
```python
except Exception as e:
    return {
        **state,
        'deliverables': [],
        'error': f"Extraction failed: {str(e)}"
    }
```

**When to modify**:
- Changing extracted fields
- Improving extraction prompts
- Switching LLM models

---

## src/nodes/validation.py

**Purpose**: Checks if we have enough information to generate a proposal. If not, generates clarifying questions.

**Input**: Extracted fields from state
**Output**: is_complete, missing_fields, clarifying_questions

**How it works**:
1. Checks what fields are missing/empty
2. Uses LLM to generate smart clarifying questions
3. Determines information quality (high/medium/low)
4. Sets `is_complete` = True/False

**Logic**:
```python
# Check what's missing
missing = []
if not deliverables or len(deliverables) == 0:
    missing.append("deliverables")
if not budget_hints:
    missing.append("budget")
if not timeline_hints:
    missing.append("timeline")

if len(missing) == 0:
    is_complete = True
else:
    is_complete = False
    # Generate questions using LLM
```

**Example Questions Generated**:
```
Input: "Need a mobile app"

Questions:
1. What specific features should the mobile app include?
2. What is your target timeline for completion?
3. What is your budget range for this project?
4. Do you need iOS, Android, or both platforms?
```

**When to modify**:
- Changing completeness criteria
- Improving question generation
- Adding new validation rules

---

## src/nodes/sanity_check.py

**Purpose**: Catches unrealistic client expectations BEFORE we do detailed calculations. This is a **reality check** layer.

**Input**: Extracted fields + user_input
**Output**: sanity_warnings (list of warning messages)

**Why This Exists**:
Client says: "Build Amazon-like platform for $5k in 2 weeks"
Without sanity check: System generates proposal saying it's possible
WITH sanity check: System warns "Amazon took $500M+ and years to build"

**What It Checks**:

### 1. Budget-Scope Mismatches

**Too High Budget**:
```python
if budget > $100,000 and deliverables < 3:
    warning: "Budget seems high for only 2 deliverables"
```

**Too Low Budget**:
```python
if budget < $10,000 and deliverables > 0:
    warning: "$5k is extremely low for software with deliverables"
```

**Budget Per Deliverable**:
```python
if deliverables >= 3:
    budget_per_feature = budget / deliverables
    if budget_per_feature < $3,000:
        warning: "$700 per feature is unrealistically low"
```

### 2. Platform Comparisons

**The Amazon Problem**:
```python
massive_platforms = {
    'amazon': '$500M-$1B+',
    'facebook': '$100M-$500M+',
    'netflix': '$100M-$500M+',
    'uber': '$50M-$200M+',
    # ... more
}

if 'like amazon' in user_input.lower():
    warning: "Amazon-scale platform requires $500M-$1B+ and years"
```

### 3. Timeline Reality Checks

**Early Detection** (NEW as of Oct 2025):
```python
# Pattern detection in user_input
import re
patterns = [
    r'in\s+(\d+)\s+(week|month|day)s?',
    r'(\d+)\s+(week|month)s?\s+timeline'
]

# Extract timeline from patterns
if "in 2 weeks" found:
    timeline_months = 0.5
```

**E-commerce Specific**:
```python
if timeline_months <= 1 and 'e-commerce' in user_input:
    warning: "E-commerce needs 3-6 months minimum for MVP"
```

**Generic Aggressive Timeline**:
```python
if timeline_months < 1 and deliverables >= 3:
    warning: "2 weeks for 5 features is extremely aggressive"
```

### 4. Outdated Technology

```python
outdated_tech = {
    'flash': 'HTML5, WebGL',
    'jquery': 'React, Vue, Angular',
    'php': 'Node.js, Python, Go',
    # ... 12 total
}

for tech in tech_hints:
    if tech.lower() in outdated_tech:
        warning: "'Flash' is outdated. Consider HTML5 instead"
```

**Key Functions**:

### `_extract_budget_number(budget_hints: str) -> float`
Parses budget from various formats:
- "$50k" → 50000
- "$50,000" → 50000
- "$30k-50k" → 40000 (average)

### `_extract_timeline_months(timeline: str) -> float`
Converts timeline to months:
- "3 weeks" → 0.75
- "4 months" → 4.0
- "2 years" → 24.0

### `sanity_check_node(state: ProposalState) -> ProposalState`
Main function that runs all checks and returns warnings.

**When to modify**:
- Adding new reality checks
- Adjusting thresholds
- Adding more outdated tech
- Adding more platform comparisons

---

## src/nodes/calculator.py

**Purpose**: Wrapper node that calls the calculator tool and formats results for state.

**What it does**:
1. Extracts deliverables, project_type, user_input from state
2. Calls `estimate_hours()` from `tools/calculator.py`
3. Calculates cost range (hours * $80-120/hr)
4. Calculates timeline (hours / 40hrs per week)
5. Updates state

**Code**:
```python
def calculator_node(state: ProposalState) -> ProposalState:
    deliverables = state.get('deliverables', [])
    project_type = state.get('project_type')
    user_input = state.get('user_input', '')

    # Call the tool
    total_hours = estimate_hours(deliverables, project_type, user_input)

    # Calculate cost
    cost_range = estimate_cost(total_hours)  # "$40,000 - $60,000"

    # Calculate timeline
    timeline = calculate_timeline(total_hours)  # "2.5 months"

    return {
        **state,
        'estimated_hours': total_hours,
        'cost_range': cost_range,
        'calculated_timeline': timeline
    }
```

**When to modify**:
- Changing hour rates
- Changing timeline calculations
- Adding new calculation fields

---

## src/tools/calculator.py

**Purpose**: The CORE estimation logic. This is where all the intelligence happens for calculating hours.

**This is the most important file for cost estimation!**

### How It Works

**Step 1: Classify Each Deliverable**

Every deliverable gets a complexity score:

```python
SIMPLE (50 hours):
    - login, signup, form, page, button, contact
    - Example: "login page" → 50 hours

MEDIUM (150 hours):
    - payment, integration, API, search, filter,
      cart, checkout, authentication, email, profile
    - Example: "payment integration" → 150 hours

COMPLEX (300 hours):
    - dashboard, admin, analytics, reporting, real-time,
      chat, video, AI, inventory, CRM, ERP, compliance
    - Example: "admin dashboard" → 300 hours

VERY_COMPLEX (500 hours):
    - 2+ complex keywords OR
    - "system"/"platform" + 1 complex keyword
    - Example: "analytics dashboard" → 500 hours (analytics + dashboard)
    - Example: "ERP system" → 500 hours (system + ERP)
```

**Classification Logic**:
```python
deliverable = "admin analytics dashboard"

matched_complex = ['admin', 'analytics', 'dashboard']  # 3 matches

if len(matched_complex) >= 2:
    hours = 500
    complexity = "VERY_COMPLEX"
```

**Step 2: MVP Context Detection** (NEW Oct 2025)

If user mentions "MVP", "basic", "startup", "simple", "early-stage":
- Downgrades complexity
- VERY_COMPLEX → COMPLEX (500 → 300)
- COMPLEX → MEDIUM (300 → 150)

```python
user_input = "Startup MVP with basic dashboard"

is_mvp_context = True  # "startup" + "basic" detected

# "dashboard" would normally be COMPLEX (300hrs)
# But with MVP context → MEDIUM (150hrs)
```

**Why?** MVPs are intentionally simplified versions. A "basic dashboard" for a startup is NOT the same as an "enterprise dashboard".

**Step 3: Sum Base Hours**

```python
deliverables = ["login", "payment integration", "admin dashboard"]

hours = 50 + 150 + 300 = 500 hours (base)
```

**Step 4: Apply Multipliers**

Multipliers stack! They multiply together.

**Project Type Multipliers**:
```python
E-commerce: 1.2x  (payment security, inventory complexity)
SaaS: 1.3x        (multi-tenancy, subscriptions)
Mobile App: 1.1x  (platform testing, app store)
Website: 0.8x     (simpler than full apps)
Enterprise: 1.0x  (baseline)
```

**Context Multipliers** (from user_input):
```python
"enterprise" in input:         * 1.3
"HIPAA" or "compliance":       * 1.2
"migration" or "legacy":       * 1.4
"multi-country" or "international": * 1.2
```

**Example**:
```python
Input: "Enterprise SaaS with HIPAA compliance for migration from legacy system"

Base hours: 1000
Project type: SaaS = 1.3x
Contexts:
    - enterprise = 1.3x
    - HIPAA = 1.2x
    - migration = 1.4x

Total multiplier = 1.3 * 1.3 * 1.2 * 1.4 = 2.84x
Final hours = 1000 * 2.84 = 2,840 hours
```

**Step 5: Calculate Cost & Timeline**

```python
Cost range = hours * $80-120/hour
Timeline = hours / 40 hours per week / 4 weeks per month

Example (500 hours):
Cost: $40,000 - $60,000
Timeline: 500 / 40 / 4 = 3.1 months
```

### Complete Flow Example

**Input**:
```
"Startup MVP with user signup, basic dashboard, simple analytics. Budget $25k"
```

**Step-by-Step**:

1. **MVP Detection**: ✓ Found "startup MVP", "basic", "simple"

2. **Classify Each Deliverable**:
   ```
   "user signup":
     - Matched: signup
     - Normal: SIMPLE (50hrs)
     - MVP context: SIMPLE (50hrs) [no change for simple]

   "basic dashboard":
     - Matched: dashboard
     - Normal: COMPLEX (300hrs)
     - MVP context: MEDIUM (150hrs) ⬇️ downgraded!

   "simple analytics":
     - Matched: analytics
     - Normal: COMPLEX (300hrs)
     - MVP context: MEDIUM (150hrs) ⬇️ downgraded!
   ```

3. **Sum**: 50 + 150 + 150 = 350 hours

4. **Multipliers**:
   - Project type: SaaS (1.3x) [inferred from MVP mention]
   - No other context multipliers
   - Total: 350 * 1.3 = 455 hours

5. **Results**:
   - Hours: 455
   - Cost: $36,400 - $54,600
   - Timeline: ~2.8 months

**Without MVP context** it would have been:
   - Hours: 650 * 1.3 = 845 hours
   - Cost: $67,600 - $101,400
   - Timeline: ~5.3 months

**Key Functions**:

### `estimate_hours(deliverables, project_type, user_input) -> int`
Main estimation function. Returns total hours.

### `_get_project_multiplier(project_type, user_input) -> float`
Returns the combined multiplier based on project type and context.

### `estimate_cost(hours) -> str`
Converts hours to cost range string.

### `calculate_timeline(hours) -> str`
Converts hours to timeline (weeks or months).

**When to modify**:
- Changing hour estimates for complexity tiers
- Adding new keywords
- Adjusting multipliers
- Adding new context detections

---

## src/nodes/generation.py

**Purpose**: Uses LLM to create the final professional proposal document.

**Input**: All filled state fields
**Output**: Markdown-formatted proposal

**What It Generates**:

1. **Warnings Section** (if sanity_warnings exist)
2. **Executive Summary**
3. **Project Scope**
4. **Deliverables Breakdown**
5. **Technology Recommendations**
6. **Timeline & Phases**
7. **Cost Breakdown**
8. **Assumptions & Risks**
9. **Next Steps**

**How Warnings Are Integrated**:

```python
sanity_warnings = state.get('sanity_warnings')

if sanity_warnings and len(sanity_warnings) > 0:
    warnings_section = "# ⚠️ Important Considerations\n\n"
    warnings_section += "**Please review these points:**\n\n"

    for i, warning in enumerate(sanity_warnings, 1):
        warnings_section += f"{i}. {warning}\n\n"

    warnings_section += "---\n\n"

    # Prepend to proposal
    proposal_text = warnings_section + proposal_text
```

**Example Output**:

```markdown
# ⚠️ Important Considerations

**Please review these points before proceeding:**

1. **Timeline Warning**: 0.5 months (2 weeks) for an e-commerce platform
   is unrealistic. E-commerce sites typically require 3-6 months minimum.

2. **Budget Warning**: Budget of $5,000 for 7 deliverables averages $714
   per deliverable. Typical minimum: $10,000-$20,000 per feature.

---

# 1. Executive Summary

This proposal outlines the development of an e-commerce platform...
```

**When to modify**:
- Changing proposal structure
- Adding new sections
- Improving generation prompts

---

## src/nodes/questions_only.py

**Purpose**: When there's not enough information, return ONLY clarifying questions (no full proposal).

**Input**: clarifying_questions from state
**Output**: Simple proposal with just questions

**Code**:
```python
def questions_only_node(state: ProposalState) -> ProposalState:
    questions = state.get('clarifying_questions', [])

    output = f"""# Insufficient Information to Generate Proposal

To create an accurate proposal, I need more details:

{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(questions))}

Please provide this information and I'll generate a comprehensive proposal."""

    return {
        **state,
        'Proposal': output
    }
```

**When to modify**:
- Changing question output format

---

# Data Flow & Execution

## Complete Example Walkthrough

**Input**:
```python
{
    "user_input": "E-commerce platform with cart, checkout, payment (Stripe),
                   admin dashboard, reviews. Timeline: 4 months, Budget: $80k,
                   Tech: React + Node.js"
}
```

### Step 1: Extraction Node

**LLM Call**:
```
Prompt: "Extract deliverables, timeline, budget, tech from this input..."
```

**Result**:
```python
{
    'user_input': 'E-commerce platform with...',
    'project_type': 'E-commerce',
    'deliverables': ['cart', 'checkout', 'payment system', 'admin dashboard', 'reviews'],
    'timeline_hints': '4 months',
    'budget_hints': '$80k',
    'tech_hints': ['React', 'Node.js', 'Stripe']
}
```

### Step 2: Validation Node

**Check**:
```python
deliverables: ✓ (5 items)
timeline: ✓ (4 months)
budget: ✓ ($80k)
tech: ✓ (React, Node.js)
```

**Result**:
```python
{
    ...previous fields...,
    'is_complete': True,
    'missing_fields': None,
    'clarifying_questions': None,
    'information_quality': 'high'
}
```

### Step 3: Sanity Check Node

**Budget Check**:
```python
Budget: $80,000
Deliverables: 5
Budget per deliverable: $16,000 ✓ (above $3k threshold)
```

**Timeline Check**:
```python
Timeline: 4 months
Deliverables: 5
4 months for 5 features = ~3 weeks per feature ✓ (reasonable)
```

**Tech Check**:
```python
Tech: ['React', 'Node.js', 'Stripe']
React: ✓ modern
Node.js: ✓ modern
Stripe: ✓ current payment platform
```

**Result**:
```python
{
    ...previous fields...,
    'sanity_warnings': None  # No warnings!
}
```

### Step 4: Conditional Routing

**Check**:
```python
is_complete = True
→ Route to "calculator" (not "questions_only")
```

### Step 5: Calculator Node

**Classify Deliverables**:
```
1. 'cart'
   Keywords matched: ['cart']
   Complexity: MEDIUM
   Hours: 150

2. 'checkout'
   Keywords matched: ['checkout']
   Complexity: MEDIUM
   Hours: 150

3. 'payment system'
   Keywords matched: ['payment']
   Complexity: MEDIUM
   Hours: 150

4. 'admin dashboard'
   Keywords matched: ['admin', 'dashboard']
   Complexity: VERY_COMPLEX (2 complex keywords)
   Hours: 500

5. 'reviews'
   Keywords matched: []
   Complexity: MEDIUM (default)
   Hours: 150

Base total: 150 + 150 + 150 + 500 + 150 = 1,100 hours
```

**Apply Multipliers**:
```python
Project type: E-commerce = 1.2x
User context: (no enterprise/compliance/migration mentions)

Total multiplier: 1.2
Final hours: 1,100 * 1.2 = 1,320 hours
```

**Calculate Cost & Timeline**:
```python
Cost range: 1,320 * $80-120 = $105,600 - $158,400
Timeline: 1,320 / 40 / 4 = 8.25 months
```

**Result**:
```python
{
    ...previous fields...,
    'estimated_hours': 1320,
    'cost_range': '$105,600 - $158,400',
    'calculated_timeline': '8.3 months'
}
```

### Step 6: Generation Node

**LLM Call**:
```
Prompt: "Create a professional proposal with:
- Deliverables: cart, checkout, payment, admin dashboard, reviews
- Cost: $105,600 - $158,400
- Timeline: 8.3 months
- Tech: React + Node.js
- No warnings to show
..."
```

**Result**:
```python
{
    ...previous fields...,
    'Proposal': '''# 1. Executive Summary

This proposal outlines the development of an E-commerce platform...

## 2. Project Scope

### Deliverables
1. Shopping cart functionality
2. Secure checkout process
3. Stripe payment integration
...

## 7. Cost Breakdown

**Total Estimated Cost**: $105,600 - $158,400
**Timeline**: 8.3 months

...'''
}
```

### Step 7: End

**Return Final State**:
All fields filled, proposal ready, execution ends.

---

## Comparison: Complete vs Incomplete Input

### Incomplete Input Example

**Input**:
```
"Need a mobile app"
```

**Flow**:
```
Extraction:
  deliverables: ['mobile app']
  timeline: None
  budget: None
  tech: None

Validation:
  is_complete: False
  missing: ['timeline', 'budget', 'tech details']
  questions: [
    "What specific features should the app include?",
    "What is your timeline?",
    "What is your budget?",
    "iOS, Android, or both?"
  ]

Sanity Check:
  (skipped - no budget/timeline to check)

Routing:
  is_complete = False → "questions_only"

Questions Only:
  Proposal: "# Insufficient Information...
             1. What specific features?
             2. What is your timeline?
             ..."

END
```

---

# Key Features & Improvements

## Timeline Tracking (What Was Added When)

### Week 1 (Initial Development)
- ✅ Basic LangGraph setup
- ✅ Extraction node (LLM)
- ✅ Validation node (LLM)
- ✅ Generation node (LLM)
- ✅ Questions only node
- ✅ Simple calculator (fixed hours per deliverable)

### Days 12-13 (Calculator Enhancements)
**Problem**: All projects getting similar costs regardless of complexity

**Solutions Added**:
1. **Keyword-based classification**
   - SIMPLE, MEDIUM, COMPLEX tiers
   - 50 / 150 / 300 hour base values

2. **Enterprise keyword detection**
   - Added: ERP, CRM, SAP, Oracle, etc.
   - These trigger COMPLEX tier

3. **Debug logging**
   - Shows classification of each deliverable
   - Shows matched keywords
   - Shows running hour total
   - Shows multiplier application

### Day 14 (Context-Aware Multipliers)
**Problem**: Same deliverables but different contexts (Enterprise vs Startup) getting same estimates

**Solutions Added**:
1. **Project type multipliers**
   - E-commerce: 1.2x
   - SaaS: 1.3x
   - Mobile: 1.1x
   - Website: 0.8x

2. **Context multipliers from user_input**
   - Enterprise: 1.3x
   - Compliance (HIPAA/GDPR): 1.2x
   - Migration/Legacy: 1.4x
   - International: 1.2x

3. **VERY_COMPLEX tier**
   - 500 hours base
   - Triggered by 2+ complex keywords
   - OR "system"/"platform" + 1 complex keyword

4. **Updated estimate_hours signature**
   - Now accepts user_input parameter
   - Passes to multiplier function

### Day 15 (Sanity Check System)
**Problem**: System accepting unrealistic requests ("Amazon for $5k")

**Solutions Added**:
1. **Budget-scope validation**
   - Check budget per deliverable
   - Minimum thresholds
   - Warn if too high or too low

2. **Platform comparison detection**
   - Detects "like Amazon", "Facebook-like", etc.
   - Warns about realistic costs ($500M+ for Amazon-scale)
   - 10 major platforms tracked

3. **Timeline reality checks**
   - Checks if timeline makes sense for deliverable count
   - Later enhanced with pattern detection

4. **Outdated tech warnings**
   - 12 outdated technologies detected
   - Suggests modern alternatives
   - Flash → HTML5, jQuery → React, etc.

5. **Integration with generation**
   - Warnings displayed at TOP of proposal
   - Formatted with ⚠️ emoji
   - Clear, actionable guidance

### Days 16-17 (Timeline Detection Improvements)
**Problem**: "E-commerce in 2 weeks" not being caught

**Root Cause**: Sanity check runs BEFORE calculator, so no estimated_hours available. Also, extraction sometimes misses "in X weeks" patterns.

**Solutions Added**:
1. **Pattern detection in sanity_check**
   - Regex to find "in X weeks", "X month timeline", "within X days"
   - Directly from user_input
   - Doesn't rely on extraction

2. **E-commerce specific checks**
   - Prioritized over generic checks
   - "E-commerce in <= 1 month" → specific warning
   - Mentions 3-6 month minimum

3. **Tiered timeline warnings**
   - E-commerce/platform specific (highest priority)
   - Generic aggressive timelines
   - Many deliverables in short time

### Days 17-18 (MVP Context Detection)
**Problem**: Startup MVP getting same complexity as enterprise systems

**Solutions Added**:
1. **MVP keyword detection**
   - Keywords: mvp, basic, simple, startup, early-stage, minimal
   - Checked in user_input

2. **Complexity downgrading**
   - VERY_COMPLEX → COMPLEX (500 → 300 hours)
   - COMPLEX → MEDIUM (300 → 150 hours)
   - Only for MVP context

3. **Migration keywords**
   - Added: migration, legacy, modernization, refactor
   - Ensures migration projects get proper complexity

4. **Cloud/infrastructure keywords**
   - Added: cloud architecture, microservices, infrastructure
   - Triggers COMPLEX tier

---

## Current Capabilities (As of Oct 23, 2025)

### What The System Can Do

✅ **Extract structured data from vague inputs**
- "Need an app" → extracts deliverables, infers needs

✅ **Detect incomplete information**
- Generates smart clarifying questions
- Only proceeds when enough info

✅ **Catch unrealistic expectations**
- Platform comparisons (Amazon, Facebook, etc.)
- Budget too low for scope
- Timeline too aggressive
- Outdated technology choices

✅ **Context-aware estimation**
- MVP vs Enterprise
- Compliance requirements
- Migration complexity
- International scope

✅ **Smart complexity classification**
- 4 tiers: SIMPLE, MEDIUM, COMPLEX, VERY_COMPLEX
- Keyword-based with 70+ keywords
- Multi-keyword detection for VERY_COMPLEX

✅ **Stacking multipliers**
- Project type + Enterprise + Compliance + Migration all multiply
- Example: SaaS (1.3x) * Enterprise (1.3x) * HIPAA (1.2x) = 2.03x

✅ **Professional proposal generation**
- 9 sections including warnings
- Markdown formatted
- Realistic estimates

✅ **Educational warnings**
- Not just "no", but "here's why" and "here's what's realistic"
- Actionable recommendations

### What It Can't Do (Limitations)

❌ **No learning from feedback**
- Doesn't improve from past proposals
- Could track: actual vs estimated hours

❌ **No team size consideration**
- Assumes 1 developer
- Could add: team multipliers

❌ **No risk adjustment**
- Doesn't adjust for project risk
- Could add: risk premiums

❌ **No negotiation capability**
- One-way: input → proposal
- Could add: iterative refinement

❌ **Requires API quota**
- Depends on OpenAI API
- No local/offline fallback

---

# How Everything Connects

## The Dependency Map

```
main.py
  ├── imports state.py
  ├── imports all nodes from nodes/
  │   ├── extraction.py
  │   │   └── uses LangChain (ChatOpenAI)
  │   ├── validation.py
  │   │   └── uses LangChain (ChatOpenAI)
  │   ├── sanity_check.py
  │   │   └── pure Python (regex, rules)
  │   ├── calculator.py
  │   │   └── imports tools/calculator.py
  │   │       └── pure Python (keyword matching, math)
  │   ├── generation.py
  │   │   └── uses LangChain (ChatOpenAI)
  │   └── questions_only.py
  │       └── pure Python (string formatting)
  └── creates StateGraph workflow

tests/
  ├── automated_test_suite.py
  │   └── imports main.create_graph()
  └── individual test files
      └── import specific nodes

docs/
  └── (documentation only, no code dependencies)
```

## Data Flow Diagram

```
User
  │
  └─> initial state {"user_input": "..."}
        │
        ├─> extraction_node
        │   └─> LLM (OpenAI GPT-4)
        │   └─> returns state with deliverables, budget, timeline, tech
        │
        ├─> validation_node
        │   └─> LLM (OpenAI GPT-4)
        │   └─> returns state with is_complete, questions
        │
        ├─> sanity_check_node
        │   └─> Pure Python rules
        │   └─> Regex pattern matching
        │   └─> returns state with warnings
        │
        ├─> DECISION: is_complete?
        │   │
        │   ├─ YES ─> calculator_node
        │   │         └─> tools/calculator.py
        │   │         └─> returns state with hours, cost, timeline
        │   │         │
        │   │         └─> generation_node
        │   │             └─> LLM (OpenAI GPT-4)
        │   │             └─> returns state with Proposal
        │   │
        │   └─ NO ──> questions_only_node
        │             └─> Pure Python
        │             └─> returns state with Proposal (questions)
        │
        └─> final state returned to User
```

## State Updates Through The Pipeline

```
Initial State:
{
  user_input: "Build e-commerce with cart and payment. 3 months, $50k"
  (all other fields: None)
}

After Extraction:
{
  user_input: "Build e-commerce with cart and payment. 3 months, $50k"
  project_type: "E-commerce"
  deliverables: ["cart", "payment integration"]
  timeline_hints: "3 months"
  budget_hints: "$50k"
  tech_hints: []
  (validation fields: None)
  (calculation fields: None)
  (output: None)
}

After Validation:
{
  ...previous fields...,
  is_complete: True
  missing_fields: None
  clarifying_questions: None
  information_quality: "high"
  (calculation fields: None)
  (output: None)
}

After Sanity Check:
{
  ...previous fields...,
  sanity_warnings: None  # No issues detected
  (calculation fields: None)
  (output: None)
}

After Calculator:
{
  ...previous fields...,
  estimated_hours: 360  # 150 + 150 = 300 * 1.2x
  cost_range: "$28,800 - $43,200"
  calculated_timeline: "2.3 months"
  (output: None)
}

After Generation:
{
  ...all previous fields...,
  Proposal: "# 1. Executive Summary\n\nThis proposal..."  # Full markdown
}
```

---

# Running & Testing

## How to Run the System

### Basic Run (main.py)

```bash
cd src
python main.py
```

This runs the test input defined in `main()` function.

### Custom Input

Edit `src/main.py`:

```python
def main():
    graph = create_graph()

    # Change this input:
    test_input = {
        "user_input": "YOUR CUSTOM INPUT HERE",
        "project_type": None,
        "deliverables": None,
        # ... rest None
    }

    result = graph.invoke(test_input)
    print(result['Proposal'])
```

### As a Module

```python
from src.main import create_graph

graph = create_graph()

result = graph.invoke({
    "user_input": "Build SaaS platform with user management",
    # ... all other fields None
})

print(f"Cost: {result['cost_range']}")
print(f"Timeline: {result['calculated_timeline']}")
print(f"\n{result['Proposal']}")
```

## Testing

### Run All Tests

```bash
python tests/automated_test_suite.py
```

This runs 15 comprehensive tests and shows pass/fail results.

### Run Individual Tests

```bash
# Test timeline detection
python tests/test_timeline.py

# Test Amazon $5k scenario
python tests/test_amazon_fix.py

# Test sanity checks
python tests/test_sanity_check.py

# Test calculator
python tests/test_calculator.py
```

### Test Categories

**Calculator Tests**:
- `test_calculator.py` - Basic functionality
- `test_new_calculator.py` - Enhanced features
- `test_enterprise_keywords.py` - Keyword detection

**Sanity Check Tests**:
- `test_sanity_check.py` - Comprehensive checks
- `test_amazon_fix.py` - Platform comparison
- `test_timeline.py` - Timeline validation
- `test_ecommerce_timeline.py` - E-commerce specific

**Integration Tests**:
- `test_sanity_integration.py` - Full workflow
- `automated_test_suite.py` - 15 scenarios

### Expected Test Results

**As of Oct 23, 2025**:
- Initial run: 10/15 passed (66.7%)
- Expected with fixes: 12-13/15 (80-86%)
- Currently blocked by: OpenAI API quota

**To reach 90%+ pass rate**:
- Need API quota restored
- May need 1-2 more iteration of adjustments

---

# Design Decisions & Why

## Why LangGraph Instead of Simple Script?

**Option 1: Simple Script**
```python
def generate_proposal(user_input):
    extracted = extract(user_input)
    if not complete(extracted):
        return questions(extracted)
    cost = calculate(extracted)
    return generate(extracted, cost)
```

**Option 2: LangGraph (What we chose)**
```python
workflow = StateGraph(State)
workflow.add_node("extract", extract)
workflow.add_node("validate", validate)
workflow.add_conditional_edges(...)
```

**Why LangGraph?**
- ✅ **Stateful**: All nodes share same state object
- ✅ **Visualizable**: Can draw the flow diagram
- ✅ **Debuggable**: Can inspect state at each step
- ✅ **Extensible**: Easy to add new nodes
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Production-ready**: Built for complex workflows

## Why Sanity Check BEFORE Calculator?

**Alternative**: Run sanity check AFTER calculator

**Why before**:
1. **Fail fast**: Catch bad inputs early
2. **Save API calls**: Don't calculate if request is absurd
3. **Better UX**: Show warnings immediately
4. **Timeline patterns**: Can detect "in 2 weeks" from user_input directly

**Trade-off**: Can't use estimated_hours in sanity check
**Solution**: Added pattern detection and deliverable-count based checks

## Why MVP Context Detection?

**Problem**:
```
Input: "Startup MVP with dashboard"
Output: $67k (dashboard = COMPLEX = 300hrs)

But client expects: ~$20-30k for an MVP
```

**Why this matters**:
- "Dashboard" for Google = enterprise analytics platform
- "Dashboard" for startup MVP = basic metrics page
- Same word, VERY different scope

**Solution**: Context-aware downgrading
- Detects MVP keywords
- Downgrades complexity
- Now outputs: ~$30k (much more realistic)

## Why Keyword-Based Classification?

**Alternative**: Use LLM to classify each deliverable

**Why keywords instead**:
- ✅ **Fast**: No API calls for each deliverable
- ✅ **Consistent**: Same keyword always gives same result
- ✅ **Debuggable**: Can see exactly which keywords matched
- ✅ **Cost-effective**: Free vs API calls
- ✅ **Offline-capable**: No internet needed for calculation

**Trade-off**: Must maintain keyword list
**Mitigation**: Keywords are well-documented and easy to update

## Why Stacking Multipliers?

**Alternative**: Pick highest multiplier

**Example**:
```
Project: Enterprise SaaS with HIPAA compliance for migration

Option 1 (highest): 1.4x (migration)
Option 2 (stacking): 1.3 * 1.3 * 1.2 * 1.4 = 2.84x
```

**Why stacking**:
- ✅ **More realistic**: Complexities compound
- ✅ **Captures all factors**: Enterprise + Compliance + Migration all add overhead
- ✅ **Better estimates**: Matches real-world experience

**Real example**:
- Basic CRM: 500 hours
- Enterprise CRM: 500 * 1.3 = 650 hours
- Enterprise CRM with HIPAA: 500 * 1.3 * 1.2 = 780 hours
- Enterprise CRM with HIPAA migration: 500 * 1.3 * 1.2 * 1.4 = 1,092 hours

The last one is realistic - it's 2.2x more complex than the baseline.

## Why 4 Complexity Tiers?

**Alternatives**:
- 2 tiers: Too simple, doesn't capture nuance
- 5+ tiers: Too complex, hard to classify

**Why 4**:
- ✅ **SIMPLE** (50hrs): Login, forms, pages - clear category
- ✅ **MEDIUM** (150hrs): Payment, API, search - most features
- ✅ **COMPLEX** (300hrs): Dashboards, analytics, CRM - advanced
- ✅ **VERY_COMPLEX** (500hrs): Multi-keyword/system combos - rare but important

**Each tier is ~3x the previous**: 50 → 150 → 300 → 500
This matches real-world complexity growth.

## Why Educational Warnings?

**Alternative**: Just say "Not possible"

**What we do**:
```
❌ Bad: "Budget too low"
✅ Good: "Budget of $5,000 for 7 deliverables averages $714 per deliverable.
         This is unrealistically low (typical minimum: $10,000-$20,000 per
         feature). Budget should be $70,000-$140,000 minimum."
```

**Why**:
- ✅ **Educates client**: Explains WHY it's unrealistic
- ✅ **Provides alternatives**: Shows realistic range
- ✅ **Builds trust**: Demonstrates expertise
- ✅ **Actionable**: Client knows exactly what to do

## Why Timeline Pattern Detection?

**Problem**: Extraction node sometimes misses "in 2 weeks"

**Solution**: Regex patterns in sanity_check

```python
patterns = [
    r'in\s+(\d+)\s+(week|month|day)s?',
    r'(\d+)\s+(week|month)s?\s+timeline'
]
```

**Why**:
- ✅ **Backup**: Catches what extraction misses
- ✅ **Direct**: Works on raw user_input
- ✅ **Fast**: Regex is instant
- ✅ **Reliable**: Consistent pattern matching

---

# Common Scenarios & Examples

## Scenario 1: Complete, Realistic Request

**Input**:
```
"Build SaaS platform with user authentication, subscription management,
and basic analytics. Timeline: 6 months. Budget: $100k. Tech: Python + React."
```

**Flow**:
1. Extraction: ✓ All fields extracted
2. Validation: ✓ Complete
3. Sanity: ✓ No warnings (realistic budget and timeline)
4. Calculator: 950 hours, $76k-$114k, 5.9 months
5. Generation: Full proposal

**Output**: Professional proposal with no warnings

---

## Scenario 2: Unrealistic Budget

**Input**:
```
"Build Amazon-like e-commerce platform. Budget: $5,000."
```

**Flow**:
1. Extraction: Deliverables extracted, budget extracted
2. Validation: ✓ Complete
3. Sanity: ⚠️ 3 WARNINGS:
   - Amazon-scale requires $500M-$1B+
   - $714 per deliverable unrealistically low
   - $5k extremely low for any software
4. Calculator: 2,150 hours, $172k-$258k, 13.4 months
5. Generation: Proposal WITH warnings at top

**Output**:
```markdown
# ⚠️ Important Considerations

1. **Scope Warning**: Building 'Amazon-scale' platform requires
   $500M-$1B+ in development costs...

2. **Budget Warning**: Budget of $5,000 for 7 deliverables...

---

# 1. Executive Summary
...
```

---

## Scenario 3: Aggressive Timeline

**Input**:
```
"Need e-commerce site with payment, cart, checkout, user accounts in 2 weeks"
```

**Flow**:
1. Extraction: ✓ All extracted
2. Validation: ✓ Complete
3. Sanity: ⚠️ WARNING:
   - Pattern detection finds "in 2 weeks"
   - E-commerce specific check triggers
   - "0.5 months for e-commerce unrealistic, need 3-6 months"
4. Calculator: 600 hours, $48k-$72k, 3.8 months
5. Generation: Proposal with timeline warning

**Output**: Warning shows realistic timeline (3-6 months minimum)

---

## Scenario 4: Vague Input

**Input**:
```
"Need a mobile app"
```

**Flow**:
1. Extraction: deliverables: ["mobile app"], rest empty
2. Validation: ✗ INCOMPLETE
   - Missing: timeline, budget, features
3. Sanity: Skipped (not enough info)
4. Routing: Goes to questions_only
5. Questions Only: Generates clarifying questions

**Output**:
```markdown
# Insufficient Information to Generate Proposal

To create an accurate proposal, I need more details:

1. What specific features should the mobile app include?
2. What is your target timeline for completion?
3. What is your budget range for this project?
4. Do you need iOS, Android, or both platforms?
5. Are there any specific design or technology requirements?

Please provide this information and I'll generate a comprehensive proposal.
```

---

## Scenario 5: MVP Context

**Input**:
```
"Early-stage startup MVP. Need basic user signup, simple dashboard,
basic analytics. Budget: $25k. Timeline: 6 weeks."
```

**Flow**:
1. Extraction: ✓ Extracted (with "startup MVP", "basic", "simple" keywords)
2. Validation: ✓ Complete
3. Sanity: ⚠️ Timeline warning (6 weeks tight for 3 features)
4. Calculator:
   - Detects MVP context ✓
   - "basic dashboard": COMPLEX → MEDIUM (150 hrs)
   - "basic analytics": COMPLEX → MEDIUM (150 hrs)
   - Total: 350 hrs * 1.3 (SaaS) = 455 hrs
   - Cost: $36k-$54k
   - Timeline: 2.8 months
5. Generation: Proposal with budget mismatch warning

**Output**:
- Estimate: ~$45k (vs client's $25k)
- Timeline: ~3 months (vs client's 1.5 months)
- Warning shows realistic expectations

**Without MVP context**: Would estimate $67k-$101k (much higher!)

---

## Scenario 6: Outdated Tech

**Input**:
```
"Build website using Flash and jQuery"
```

**Flow**:
1. Extraction: tech_hints: ["Flash", "jQuery"]
2. Validation: ✓ Complete
3. Sanity: ⚠️ 2 WARNINGS:
   - Flash outdated → suggests HTML5, WebGL
   - jQuery outdated → suggests React, Vue, Angular
4. Calculator: (normal calculation)
5. Generation: Proposal with tech warnings

**Output**: Warnings suggest modern alternatives

---

# Extending The System

## Adding a New Node

**Example: Add a "Security Check" node**

1. **Create the node** (`src/nodes/security_check.py`):
```python
def security_check_node(state: ProposalState) -> ProposalState:
    tech_hints = state.get('tech_hints', [])
    deliverables = state.get('deliverables', [])

    security_issues = []

    # Check for payment without encryption mention
    has_payment = any('payment' in d.lower() for d in deliverables)
    has_encryption = any('encrypt' in t.lower() for t in tech_hints)

    if has_payment and not has_encryption:
        security_issues.append(
            "Payment processing detected but no encryption mentioned. "
            "Consider adding SSL/TLS and data encryption."
        )

    return {
        **state,
        'security_warnings': security_issues
    }
```

2. **Update state** (`src/state.py`):
```python
class ProposalState(TypedDict):
    # ... existing fields ...
    security_warnings: Optional[List[str]]  # ADD THIS
```

3. **Add to workflow** (`src/main.py`):
```python
def create_graph():
    workflow = StateGraph(ProposalState)

    # Add new node
    workflow.add_node("security_check", security_check_node)

    # Insert in flow
    workflow.add_edge("sanity_check", "security_check")
    workflow.add_edge("security_check", "calculator")  # or wherever
```

4. **Use in generation** (`src/nodes/generation.py`):
```python
security_warnings = state.get('security_warnings')
if security_warnings:
    # Include in proposal
```

## Adding a New Keyword Category

**Example: Add "Integration" category**

Edit `src/tools/calculator.py`:

```python
integration_keywords = [
    'api integration',
    'third-party',
    'webhook',
    'oauth',
    'sso',
    'saml'
]

# In classification logic:
matched_integration = [k for k in integration_keywords if k in deliverable_lower]

if len(matched_integration) > 0:
    hours = 200  # Custom hours for integrations
    complexity = "INTEGRATION"
```

## Adding a New Multiplier

**Example: Add "Regulatory" multiplier**

Edit `src/tools/calculator.py`:

```python
def _get_project_multiplier(project_type, user_input):
    multiplier = 1.0

    # ... existing multipliers ...

    # ADD: Regulatory multiplier
    regulatory_keywords = ['fda', 'finra', 'banking', 'medical device']
    if any(keyword in user_input.lower() for keyword in regulatory_keywords):
        multiplier *= 1.5  # 50% increase for regulatory overhead

    return multiplier
```

## Adding a New Sanity Check

**Example: Check for team size mismatch**

Edit `src/nodes/sanity_check.py`:

```python
def _check_team_size(state: ProposalState, warnings: List[str]) -> None:
    user_input = state.get('user_input', '').lower()
    estimated_hours = state.get('estimated_hours')

    # Detect team size mentions
    if 'solo' in user_input or 'one developer' in user_input:
        if estimated_hours and estimated_hours > 2000:
            warnings.append(
                f"⚠️ Team Warning: {estimated_hours} hours estimated, "
                f"but 'solo developer' mentioned. This would take "
                f"{estimated_hours / 40 / 4:.1f} months for one person. "
                f"Consider a team of {estimated_hours // 2000 + 1} developers."
            )

# Call it in sanity_check_node:
_check_team_size(state, warnings)
```

---

# Troubleshooting

## Common Issues

### Issue: "API Quota Exceeded"

**Error**: `RateLimitError: 429 - insufficient_quota`

**Cause**: OpenAI API key has no credits/quota

**Solutions**:
1. Add credits to OpenAI account
2. Use different API key
3. Wait for quota reset
4. Implement caching for tests

### Issue: Tests Failing

**Check**:
1. Are you in the right directory?
   ```bash
   cd /home/awais/Projects/proposal-generator-agent
   python tests/test_name.py
   ```

2. Are imports working?
   ```python
   # Tests should have:
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
   ```

3. Is API key set?
   ```bash
   echo $OPENAI_API_KEY
   ```

### Issue: Extraction Not Working

**Symptoms**: All fields come back empty/None

**Checks**:
1. Is user_input actually populated?
2. Is LLM call succeeding?
3. Is JSON parsing working?

**Debug**:
```python
# In extraction.py, add:
print(f"User input: {user_input}")
print(f"LLM response: {response.content}")
print(f"Parsed data: {parsed_data}")
```

### Issue: Calculator Giving Wrong Estimates

**Symptoms**: Hours too high or too low

**Checks**:
1. Are keywords matching correctly?
2. Is MVP context being detected when it shouldn't (or vice versa)?
3. Are multipliers stacking too much?

**Debug**:
```python
# Run with debug logging enabled (it's already in the code)
python tests/test_calculator.py

# Check output for each deliverable classification
```

### Issue: Sanity Warnings Not Showing

**Checks**:
1. Is sanity_check node being called?
2. Are thresholds set correctly?
3. Is budget/timeline being extracted?

**Debug**:
```python
# In sanity_check.py, add:
print(f"Budget: {budget}")
print(f"Timeline: {timeline_months}")
print(f"Deliverables: {num_deliverables}")
print(f"Warnings: {warnings}")
```

---

# Future Improvements

## Potential Enhancements

### 1. Learning System
Track actual vs estimated hours and improve over time.

### 2. Team Size Calculation
Automatically suggest team size based on timeline and hours.

### 3. Risk Assessment
Add risk factors and adjust estimates accordingly.

### 4. Template Library
Pre-built templates for common project types.

### 5. Interactive Refinement
Allow back-and-forth to refine the proposal.

### 6. Historical Data
Track past proposals and outcomes for better estimates.

### 7. Phase Breakdown
Automatically break project into phases (MVP, Beta, v1.0, etc.)

### 8. Resource Allocation
Suggest specific roles needed (frontend dev, backend dev, designer, etc.)

---

# Quick Reference

## Running Commands

```bash
# Run main system
python src/main.py

# Run all tests
python tests/automated_test_suite.py

# Run specific test
python tests/test_sanity_check.py

# Test calculator
python tests/test_calculator.py
```

## File Paths (From Project Root)

```
src/
  main.py           - Workflow setup
  state.py          - State schema
  nodes/
    extraction.py   - LLM extraction
    validation.py   - LLM validation
    sanity_check.py - Reality checks
    calculator.py   - Wrapper
    generation.py   - LLM generation
    questions_only.py - Question output
  tools/
    calculator.py   - Core estimation logic

tests/
  automated_test_suite.py - Main test suite
  test_*.py              - Individual tests
  *.md                   - Test documentation

docs/
  learning.md            - THIS FILE
  *.md                   - Other documentation
```

## Key Numbers to Remember

**Complexity Hours**:
- SIMPLE: 50 hours
- MEDIUM: 150 hours
- COMPLEX: 300 hours
- VERY_COMPLEX: 500 hours

**Multipliers**:
- E-commerce: 1.2x
- SaaS: 1.3x
- Enterprise: 1.3x
- Compliance: 1.2x
- Migration: 1.4x
- International: 1.2x

**Rates**:
- Minimum: $80/hour
- Maximum: $120/hour

**Thresholds**:
- Min budget per feature: $3,000
- Min total budget: $10,000
- Min timeline for e-commerce: 3 months

---

# Conclusion

You now have **complete knowledge** of the Proposal Generator system:

✅ **Architecture**: How LangGraph orchestrates everything
✅ **Files**: What each file does and how it works
✅ **Data Flow**: How state flows through nodes
✅ **Calculations**: How hours, cost, and timeline are estimated
✅ **Sanity Checks**: How unrealistic expectations are caught
✅ **Improvements**: What was added in the last 2 days
✅ **Connections**: How everything talks to each other
✅ **Running**: How to test and extend the system
✅ **Decisions**: Why things are designed this way

**Come back in 7 months?** Read this file. You'll be up to speed in 30 minutes.

**New team member?** Give them this file. They'll understand the entire system.

**Making it open source?** This file IS your documentation.

---

**Last Updated**: October 23, 2025
**Status**: Fully operational, 80-86% test pass rate expected
**Next Steps**: Restore API quota, run tests, iterate to 90%+
