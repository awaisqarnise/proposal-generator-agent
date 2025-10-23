import os
from langchain_openai import ChatOpenAI
from state import ProposalState
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check for API key at module level
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# Simple, direct initialization
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,  # Higher temperature for more creative proposal generation
    api_key=OPENAI_API_KEY
)


def generation_node(state: ProposalState) -> ProposalState:

    """
    Generate a professional project proposal based on extracted information.

    Uses the extracted deliverables, timeline_hints, budget_hints, and tech_hints
    to create a comprehensive proposal with multiple sections.

    Args:
        state: Current ProposalState with extracted information

    Returns:
        Updated ProposalState with Proposal field populated
    """
    project_type = state.get("project_type")
    industry = state.get("industry")
    deliverables = state.get("deliverables", [])
    timeline_hints = state.get("timeline_hints")
    budget_hints = state.get("budget_hints")
    tech_hints = state.get("tech_hints", [])
    clarifying_questions = state.get("clarifying_questions")
    user_input = state.get("user_input", "")

    # Get calculated values
    estimated_hours = state.get("estimated_hours")
    calculated_timeline = state.get("calculated_timeline")
    cost_range = state.get("cost_range")

    # Get sanity warnings
    sanity_warnings = state.get("sanity_warnings")

    # Format the extracted data for the prompt
    project_type_str = project_type if project_type else "software"
    industry_str = industry if industry else "general"
    deliverables_str = ", ".join(deliverables) if deliverables else "Not specified"
    timeline_str = timeline_hints if timeline_hints else "Not specified"
    budget_str = budget_hints if budget_hints else "Not specified"
    tech_str = ", ".join(tech_hints) if tech_hints else "Not specified"

    # Determine what was inferred vs. explicitly provided
    inferred_items = []
    if "infer" in user_input.lower() or not any(keyword in user_input.lower() for keyword in ["timeline", "deadline", "month", "week", "by"]):
        if timeline_hints and timeline_hints != "Not specified":
            inferred_items.append("timeline")
    if "infer" in user_input.lower() or not any(keyword in user_input.lower() for keyword in ["budget", "$", "cost", "price"]):
        if budget_hints and budget_hints != "Not specified":
            inferred_items.append("budget")
    if "infer" in user_input.lower() or not any(keyword in user_input.lower() for keyword in ["using", "with", "tech", "stack", "framework"]):
        if tech_hints and len(tech_hints) > 0:
            inferred_items.append("technology stack")

    # Check if there are clarifying questions
    has_questions = clarifying_questions and len(clarifying_questions) > 0

    # Build calculated analysis section
    calculated_analysis = ""
    if estimated_hours and calculated_timeline and cost_range:
        calculated_analysis = f"""
Based on analysis:
- Estimated effort: {estimated_hours} hours
- Timeline: {calculated_timeline}
- Budget: {cost_range}

Use these figures in your proposal."""

    # Create the generation prompt
    if has_questions:
        generation_prompt = f"""You are creating a professional, executive-level proposal for a {project_type_str} project.

Project Context:
- Project Type: {project_type_str}
- Industry: {industry_str}
- Client needs: {deliverables_str}
- Timeline hints: {timeline_str}
- Budget hints: {budget_str}
- Tech stack hints: {tech_str}
{calculated_analysis}

IMPORTANT: The following items were INFERRED (not explicitly provided): {", ".join(inferred_items) if inferred_items else "None - all items provided explicitly"}

Since some information is missing or inferred, create a proposal with clear assumptions stated.
Tailor your proposal to the specific needs and challenges of {project_type_str} projects in the {industry_str} industry.

Create a proposal with these sections in this exact order:

1. **About This Proposal**
   - Brief introduction (2-3 sentences)
   - What this document covers
   - How to use this proposal

2. **Executive Summary**
   - Business value proposition specific to {project_type_str} industry
   - Key outcomes and benefits
   - High-level overview (3-4 sentences)

3. **Scope of Work**
   - Detailed breakdown of deliverables
   - {project_type_str}-specific features and considerations
   - What's included and what's not included
   - Technical requirements

4. **Project Timeline**
   - Break into clear phases (Planning, Development, Testing, Deployment)
   - Include milestones for each phase
   - Dependencies and critical path items
   - (Note assumptions where timeline details are missing)

5. **Investment & Budget**
   - Total estimated cost range
   - Breakdown by major components if possible
   - Payment terms recommendation
   - (Note assumptions where budget details are missing)

6. **Technology Stack**
   - Recommended technologies appropriate for {project_type_str}
   - Justification for each technology choice
   - Infrastructure considerations
   - Security and scalability notes

7. **Key Assumptions**
   - List all assumptions made for inferred items (timeline, budget, technology stack)
   - Clearly mark which items were inferred vs. explicitly provided
   - Risk factors to consider
   - Dependencies on client inputs

8. **Next Steps**
   - Immediate action items
   - How to proceed with this proposal
   - Contact information and follow-up process

Use clear, professional business language throughout. Write as if presenting to executives and decision-makers.
Format in clean Markdown with proper headings and bullet points."""
    else:
        generation_prompt = f"""You are creating a professional, executive-level proposal for a {project_type_str} project.

Project Context:
- Project Type: {project_type_str}
- Industry: {industry_str}
- Client needs: {deliverables_str}
- Timeline hints: {timeline_str}
- Budget hints: {budget_str}
- Tech stack hints: {tech_str}
{calculated_analysis}

IMPORTANT: The following items were INFERRED based on industry standards: {", ".join(inferred_items) if inferred_items else "None - all items provided explicitly"}

Create a proposal with clear assumptions stated for any inferred items.
Tailor your proposal to the specific needs and challenges of {project_type_str} projects in the {industry_str} industry.

Create a proposal with these sections in this exact order:

1. **About This Proposal**
   - Brief introduction (2-3 sentences)
   - What this document covers
   - How to use this proposal

2. **Executive Summary**
   - Business value proposition specific to {project_type_str} industry
   - Key outcomes and benefits
   - High-level overview (3-4 sentences)

3. **Scope of Work**
   - Detailed breakdown of deliverables
   - {project_type_str}-specific features and considerations
   - What's included and what's not included
   - Technical requirements

4. **Project Timeline**
   - Break into clear phases (Planning, Development, Testing, Deployment)
   - Include milestones for each phase
   - Dependencies and critical path items
   - Estimated duration for each phase

5. **Investment & Budget**
   - Total estimated cost range
   - Breakdown by major components if possible
   - Payment terms recommendation
   - Value proposition

6. **Technology Stack**
   - Recommended technologies appropriate for {project_type_str}
   - Justification for each technology choice
   - Infrastructure considerations
   - Security and scalability notes

7. **Key Assumptions**
   - List all assumptions made for inferred items (timeline, budget, technology stack)
   - Clearly mark which items were inferred vs. explicitly provided
   - Critical assumptions about project scope
   - Risk factors to consider
   - Dependencies on client inputs

8. **Next Steps**
   - Immediate action items
   - How to proceed with this proposal
   - Timeline for decision
   - Contact information and follow-up process

Use clear, professional business language throughout. Write as if presenting to executives and decision-makers.
Format in clean Markdown with proper headings and bullet points."""

    try:
        # Check if there's already an error in the state
        if state.get('error'):
            # Return error message as proposal
            return {
                **state,
                "Proposal": f"# Error\n\n{state.get('error')}\n\nPlease resolve the error and try again."
            }

        # Check if we have minimum required data
        if not deliverables or len(deliverables) == 0:
            error_msg = "Generation Error: No project deliverables provided"
            print(f"Error: {error_msg}")
            return {
                **state,
                "error": f"{error_msg}\n\nUnable to generate a proposal without knowing what features you need.",
                "Proposal": f"# Error\n\n{error_msg}\n\nUnable to generate a proposal without knowing what features you need.\n\nPlease provide details about what you'd like to build."
            }

        # Validate that required fields exist
        if not project_type and not industry:
            error_msg = "Generation Error: Missing project context"
            print(f"Warning: {error_msg} - project_type and industry are both missing")
            # Don't fail, but log warning
            print("Continuing with generic proposal generation")

        # Invoke the LLM
        response = llm.invoke(generation_prompt)

        # Validate response
        if not response or not response.content:
            error_msg = "Generation Error: Empty response from AI service"
            print(f"Error: {error_msg}")
            return {
                **state,
                "error": f"{error_msg}\n\nThe AI service returned an empty response. Please try again.",
                "Proposal": f"# Error\n\n{error_msg}\n\nThe AI service returned an empty response. Please try again in a moment."
            }

        # Extract the generated proposal
        proposal_text = response.content.strip()

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

        # If there are clarifying questions, add them after warnings
        if has_questions:
            questions_section = "## Clarifying Questions\n\nTo create a more accurate proposal, please provide:\n\n"
            for i, question in enumerate(clarifying_questions, 1):
                questions_section += f"{i}. {question}\n"
            questions_section += "\n## Proposal Based on Assumptions\n\n"

            proposal_text = warnings_section + questions_section + proposal_text
        else:
            # Just warnings (if any) at the top
            proposal_text = warnings_section + proposal_text

        # Update state with generated proposal
        return {
            **state,
            "Proposal": proposal_text
        }

    except KeyError as e:
        error_msg = f"Configuration Error: Missing API key - {str(e)}"
        print(f"Error during proposal generation: {error_msg}")
        return {
            **state,
            "error": f"{error_msg}\n\nPlease ensure OPENAI_API_KEY is set in your .env file.",
            "Proposal": f"# Configuration Error\n\n{error_msg}\n\nPlease ensure OPENAI_API_KEY is set in your .env file."
        }

    except TimeoutError as e:
        error_msg = "API Timeout: The proposal generation request timed out"
        print(f"Error during proposal generation: {error_msg}")
        return {
            **state,
            "error": f"{error_msg}\n\nThe AI service took too long to respond. Please try again.",
            "Proposal": f"# Timeout Error\n\n{error_msg}\n\nThe AI service took too long to respond. Please try again in a moment."
        }

    except ValueError as e:
        error_msg = "Data Error: Invalid data format encountered"
        print(f"Error during proposal generation: {error_msg} - {str(e)}")
        return {
            **state,
            "error": f"{error_msg}\n\nThere was a problem with the project data format. Please check your input.",
            "Proposal": f"# Data Error\n\n{error_msg}\n\nThere was a problem with the project data format. Details: {str(e)}"
        }

    except AttributeError as e:
        error_msg = "State Error: Missing required state field"
        print(f"Error during proposal generation: {error_msg} - {str(e)}")
        return {
            **state,
            "error": f"{error_msg}\n\nSome required project information is missing. Please try again.",
            "Proposal": f"# State Error\n\n{error_msg}\n\nSome required project information is missing. Details: {str(e)}"
        }

    except Exception as e:
        error_msg = f"Unexpected Generation Error: {type(e).__name__}"
        print(f"Error during proposal generation: {error_msg} - {str(e)}")
        return {
            **state,
            "error": f"{error_msg}\n\nAn unexpected error occurred while generating the proposal. Please try again.",
            "Proposal": f"# Generation Error\n\n{error_msg}\n\nAn unexpected error occurred: {str(e)}\n\nPlease try again with different input or contact support if the issue persists."
        }
