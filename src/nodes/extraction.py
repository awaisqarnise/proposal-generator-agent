import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
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
    temperature=0.1,
    api_key=OPENAI_API_KEY
)
parser = JsonOutputParser()


def extraction_node(state: ProposalState) -> ProposalState:
    """
    Extract structured information from user input using OpenAI GPT-4.

    Extracts:
    - deliverables: List of project deliverables
    - timeline_hints: Timeline expectations or constraints
    - budget_hints: Budget expectations or constraints
    - tech_hints: Technology preferences or requirements

    Args:
        state: Current ProposalState with user_input

    Returns:
        Updated ProposalState with extracted fields populated
    """
    user_input = state.get("user_input", "")

    if not user_input:
        return {
            **state,
            "project_type": None,
            "deliverables": [],
            "timeline_hints": None,
            "budget_hints": None,
            "tech_hints": []
        }

    # Create extraction prompt
    extraction_prompt = f"""You are an expert at extracting structured information from project requirements. You excel at handling vague inputs by inferring context, identifying industries, extracting implicit technologies, and breaking down compound deliverables.

Analyze the following user input and extract key information into a JSON structure:

User Input:
{user_input}

HANDLING GUIDELINES:
1. **Input Clarity Check (CRITICAL)**: First, determine if the input makes enough sense to create a proposal:
   - ✓ MAKES SENSE: "app like Uber", "restaurant website", "e-commerce for clothes", "patient management system"
   - ✗ DOESN'T MAKE SENSE: "ordering app" (ordering what?), "tracking system" (tracking what?), "management software" (managing what?)
   - If input is TOO VAGUE to understand the core purpose, return ALL null/empty values to trigger clarifying questions
   - If input has SOME context (industry, comparison, or clear purpose), proceed with inference

2. **Vague but Understandable Inputs**: If input is minimal but makes sense (e.g., "need a website for my restaurant"), infer common features based on project type and industry

3. **Multiple Projects**: If multiple projects mentioned, focus on the PRIMARY/MAIN project

4. **Industry Detection**: Identify the industry from context clues, terminology, or explicit mentions

5. **Tech Stack Inference**: Extract technologies from context, not just explicit mentions (e.g., "payment with Stripe" → include "Stripe")

6. **Deliverable Splitting**: Break compound phrases into separate deliverables (e.g., "cart and checkout" → ["cart", "checkout"])

7. **Budget/Timeline/Tech Inference**: ALWAYS infer these UNLESS the input doesn't make sense (see #1)

INDUSTRY IDENTIFICATION:
Extract the industry if mentioned or strongly implied. Common industries:
- **Healthcare**: Keywords like "patient", "medical", "hospital", "clinic", "doctor", "EMR", "HIPAA", "diagnosis", "prescription", "telemedicine"
- **Fintech/Finance**: Keywords like "payment", "banking", "transaction", "wallet", "trading", "investment", "KYC", "compliance", "ledger", "loan", "mortgage"
- **E-commerce/Retail**: Keywords like "shop", "store", "product", "cart", "checkout", "inventory", "POS", "SKU", "marketplace", "vendor"
- **Education**: Keywords like "student", "course", "learning", "LMS", "teacher", "assessment", "grade", "curriculum", "school", "university"
- **Real Estate**: Keywords like "property", "listing", "agent", "rental", "lease", "mortgage", "MLS"
- **Food & Hospitality**: Keywords like "restaurant", "menu", "reservation", "hotel", "booking", "delivery", "recipe", "dining"
- **Transportation/Logistics**: Keywords like "shipping", "delivery", "tracking", "fleet", "route", "warehouse", "driver"
- **Entertainment/Media**: Keywords like "streaming", "video", "music", "content", "subscription", "playlist", "social media"
- **SaaS/Technology**: Keywords like "dashboard", "analytics", "tenant", "subscription", "API", "integration", "workflow"
- **Other**: If industry is mentioned but doesn't fit above categories, capture it as-is

TECHNOLOGY EXTRACTION (IMPROVED):
Extract technologies from BOTH explicit mentions AND contextual clues:
- Explicit: "using React and Node.js" → ["React", "Node.js"]
- Contextual: "payment with Stripe" → ["Stripe"]
- Contextual: "hosting on AWS" → ["AWS"]
- Contextual: "video calls" → ["WebRTC" or "video streaming technology"]
- Contextual: "real-time chat" → ["WebSocket" or "real-time messaging"]
- Contextual: "AI recommendations" → ["machine learning", "AI"]
- Contextual: "mobile app for iOS" → ["iOS", "Swift" or "React Native"]
- Common patterns: Authentication → ["OAuth", "JWT"], Payments → ["Stripe", "PayPal"], Cloud → ["AWS", "Azure", "GCP"]

DELIVERABLE SPLITTING RULES:
Break down compound phrases connected by "and", "with", or commas into separate deliverables:
- "cart and checkout" → ["shopping cart", "checkout"]
- "user profiles and settings" → ["user profiles", "user settings"]
- "search, filter, and sort" → ["search functionality", "filter functionality", "sort functionality"]
- "login/signup" or "login and signup" → ["login system", "signup system"]
- EXCEPTION: Keep technical compound terms together (e.g., "search and filter" CAN stay together if they're one feature)
- EXCEPTION: Keep "X with Y" together if Y describes X (e.g., "dashboard with analytics" → ["dashboard with analytics"])

PROJECT TYPE IDENTIFICATION:
- E-commerce: Keywords like "shop", "store", "cart", "marketplace", "products", "inventory", "checkout"
- SaaS: Keywords like "subscription", "tenant", "dashboard", "analytics", "saas", "cloud", "B2B software"
- Mobile App: Keywords like "iOS", "Android", "mobile app", "native app", "app store"
- Website: Keywords like "landing page", "corporate site", "portfolio", "blog", "website", "web presence"
- Custom Software: Keywords like "inventory system", "CRM", "internal tool", "management system", "enterprise software"

DELIVERABLE EXTRACTION (NOT project type):
- Extract specific features, functionalities, and components
- Split compound deliverables connected by "and" or commas into separate items
- Keep descriptive compound features together (e.g., "user authentication system" = 1 deliverable)
- DO NOT include the project type itself in deliverables
- Focus on actionable features
- For vague inputs, infer 3-5 industry-standard features based on project type AND industry

EXAMPLES:

Example 1 - Tech Stack Inference:
Input: "Need a payment system with Stripe for my online store"
{{
    "project_type": "E-commerce",
    "industry": "E-commerce",
    "deliverables": ["payment system", "product catalog", "shopping cart"],
    "timeline_hints": null,
    "budget_hints": null,
    "tech_hints": ["Stripe"]  ✓ (extracted Stripe from context)
}}

Example 2 - Deliverable Splitting:
Input: "Build a dashboard with cart and checkout features"
{{
    "project_type": "E-commerce",
    "industry": "E-commerce",
    "deliverables": ["dashboard", "shopping cart", "checkout"],  ✓ (split "cart and checkout")
    "timeline_hints": null,
    "budget_hints": null,
    "tech_hints": []
}}

Example 3 - Industry Detection:
Input: "Patient portal for viewing medical records and booking appointments"
{{
    "project_type": "Custom Software",
    "industry": "Healthcare",  ✓ (detected from "patient" and "medical")
    "deliverables": ["patient portal", "medical records viewing", "appointment booking"],
    "timeline_hints": null,
    "budget_hints": null,
    "tech_hints": ["HIPAA-compliant storage"]  ✓ (inferred security requirement)
}}

Example 4 - Vague Input with Industry Context:
Input: "Need a website for my restaurant"
{{
    "project_type": "Website",
    "industry": "Food & Hospitality",  ✓ (detected from "restaurant")
    "deliverables": ["menu display", "online reservation system", "contact form", "location map", "gallery"],  ✓ (inferred restaurant-specific features)
    "timeline_hints": null,
    "budget_hints": null,
    "tech_hints": []
}}

Example 5 - Multiple Tech Hints:
Input: "Real-time chat app with video calls hosted on AWS"
{{
    "project_type": "Mobile App",
    "industry": "SaaS",
    "deliverables": ["real-time chat", "video calling", "user authentication"],
    "timeline_hints": null,
    "budget_hints": null,
    "tech_hints": ["WebSocket", "WebRTC", "AWS"]  ✓ (WebSocket inferred from "real-time", WebRTC from "video", AWS explicit)
}}

Example 6 - Fintech Industry with Inferred Budget/Timeline:
Input: "Trading platform with real-time stock prices and portfolio tracking"
{{
    "project_type": "SaaS",
    "industry": "Fintech",  ✓ (detected from "trading" and "stock")
    "deliverables": ["real-time stock price feed", "portfolio tracking", "trading interface", "transaction history"],
    "timeline_hints": "4-6 months",  ✓ (inferred - complex SaaS with compliance needs)
    "budget_hints": "$80,000-$180,000",  ✓ (inferred - SaaS with fintech compliance, higher range)
    "tech_hints": ["real-time data streaming", "financial APIs", "React", "Node.js", "WebSocket", "secure authentication"]  ✓ (inferred from context + defaults)
}}

Example 7 - Simple Input with Full Inference:
Input: "Need a website for my restaurant"
{{
    "project_type": "Website",
    "industry": "Food & Hospitality",
    "deliverables": ["menu display", "online reservation system", "contact form", "location map", "gallery"],
    "timeline_hints": "3-4 weeks",  ✓ (inferred - simple website)
    "budget_hints": "$5,000-$15,000",  ✓ (inferred - basic website range)
    "tech_hints": ["React", "Node.js", "responsive design"]  ✓ (inferred - standard web stack)
}}

Example 8 - Uber-like App (MAKES SENSE):
Input: "I need an app like Uber"
{{
    "project_type": "Mobile App",
    "industry": "Transportation",
    "deliverables": ["real-time GPS tracking", "ride matching system", "payment integration", "driver and rider profiles", "rating system", "fare calculation"],
    "timeline_hints": "5-7 months",  ✓ (inferred - complex mobile app with real-time features)
    "budget_hints": "$80,000-$150,000",  ✓ (inferred - complex mobile app)
    "tech_hints": ["React Native", "real-time location tracking", "Google Maps API", "Stripe", "WebSocket", "Firebase"]  ✓ (inferred from ride-sharing context)
}}

Example 9 - Vague Input (DOESN'T MAKE SENSE):
Input: "I want ordering app"
{{
    "project_type": null,  ✓ (too vague - ordering what? food? products? services?)
    "industry": null,
    "deliverables": [],  ✓ (cannot infer without context)
    "timeline_hints": null,  ✓ (DO NOT infer if input doesn't make sense)
    "budget_hints": null,  ✓ (DO NOT infer if input doesn't make sense)
    "tech_hints": []  ✓ (DO NOT infer if input doesn't make sense)
}}

Extract the following information:
1. **project_type**: The overall project category (E-commerce, SaaS, Mobile App, Website, Custom Software, or null if unclear)
2. **industry**: The industry/sector this project serves (Healthcare, Fintech, E-commerce, Education, etc., or null if unclear)
3. **deliverables**: List of specific FEATURES only (NOT the project type). Split compound deliverables connected by "and"/"with".
4. **timeline_hints**: Timeline information - ALWAYS infer a reasonable timeline even if not explicitly mentioned:
   - If mentioned explicitly: use that (e.g., "need it in 3 months")
   - If NOT mentioned: Infer based on project complexity and industry standards:
     * Simple website/landing page: "2-4 weeks"
     * Mobile app with basic features: "2-3 months"
     * E-commerce platform: "3-4 months"
     * Complex SaaS/enterprise software: "4-6 months"
     * MVP versions: reduce timeline by 30-40%
   - Consider urgency keywords: "urgent" → shorter timeline, "long-term" → longer timeline
5. **budget_hints**: Budget information - ALWAYS infer a reasonable budget range even if not explicitly mentioned:
   - If mentioned explicitly: use that (e.g., "$50k budget")
   - If NOT mentioned: Infer based on project type, complexity, and industry:
     * Simple website: "$5,000-$15,000"
     * Mobile app (basic): "$20,000-$50,000"
     * E-commerce platform: "$30,000-$80,000"
     * SaaS platform: "$50,000-$150,000"
     * Enterprise software: "$100,000+"
     * Healthcare/Fintech (compliance heavy): Add 20-30% to ranges
   - Consider context: "startup" → lower range, "enterprise" → higher range, "MVP" → lower range
6. **tech_hints**: Technologies - ALWAYS suggest appropriate technologies even if not explicitly mentioned:
   - If mentioned explicitly: use those (e.g., "React", "AWS")
   - If NOT mentioned: Suggest industry-standard technologies based on project type:
     * Web apps: ["React" or "Vue.js", "Node.js", "PostgreSQL"]
     * Mobile apps: ["React Native" or "Flutter", "Firebase"]
     * E-commerce: ["React", "Node.js", "Stripe", "PostgreSQL"]
     * Healthcare: ["HIPAA-compliant hosting", "encrypted storage"]
     * Fintech: ["secure authentication", "payment gateway", "compliance tools"]
     * Real-time features: Add ["WebSocket", "Redis"]
   - Infer from features: payment → "Stripe/PayPal", video → "WebRTC", maps → "Google Maps API"

Return ONLY a valid JSON object with this exact structure - NO OTHER TEXT, NO EXPLANATIONS, NO PREAMBLE:
{{
    "project_type": "project category or null",
    "industry": "industry name or null",
    "deliverables": ["list", "of", "features"],
    "timeline_hints": "ALWAYS provide inferred or explicit timeline (NEVER null)",
    "budget_hints": "ALWAYS provide inferred or explicit budget range (NEVER null)",
    "tech_hints": ["ALWAYS provide inferred or explicit technologies (NEVER empty)"]
}}

DO NOT include the user input in your response. DO NOT add any explanatory text. Return ONLY the raw JSON object starting with {{ and ending with }}.

CRITICAL RULES:
- **ALWAYS infer timeline_hints** even if not mentioned - base it on project complexity
- **ALWAYS infer budget_hints** even if not mentioned - base it on project type and industry
- **ALWAYS suggest tech_hints** even if not mentioned - use industry-standard technologies
- First identify project_type and industry, then extract features as deliverables
- Split deliverables when multiple are mentioned together with "and" or commas (unless they form one cohesive feature)
- Extract technologies from context, not just explicit mentions
- Infer industry from keywords, terminology, or explicit mentions
- DO NOT include project type in deliverables list
- For vague inputs, infer 3-5 reasonable industry-standard features based on project type AND industry
- If multiple projects mentioned, extract info for the PRIMARY project only
- Recognize and expand industry-specific abbreviations (EMR, CRM, POS, LMS, etc.)
- Extract implicit features and technologies (e.g., "online store" implies "shopping cart", "product catalog")
- Look for context clues for timeline (words like "urgent", "soon", "Q1", "launch", "deadline")
- Look for context clues for budget (words like "small budget", "enterprise", "startup", "affordable")

YOUR RESPONSE MUST BE ONLY THE JSON OBJECT. DO NOT INCLUDE:
- The user input
- Any explanations or commentary
- Any text before or after the JSON
- Any markdown formatting or code blocks

Return ONLY the JSON object starting with {{ and ending with }}."""

    try:
        # Invoke the LLM
        response = llm.invoke(extraction_prompt)

        # Clean the response content - extract only the JSON object
        content = response.content.strip()

        # Find the first { and last } to extract just the JSON
        first_brace = content.find('{')
        last_brace = content.rfind('}')

        if first_brace != -1 and last_brace != -1:
            json_content = content[first_brace:last_brace + 1]
        else:
            json_content = content

        # Parse the JSON response
        parsed_data = parser.parse(json_content)

        # Validate that we got some data
        deliverables = parsed_data.get("deliverables", [])
        if not deliverables:
            print("Warning: No deliverables extracted from user input")

        # Update state with extracted information
        return {
            **state,
            "project_type": parsed_data.get("project_type"),
            "industry": parsed_data.get("industry"),
            "deliverables": deliverables,
            "timeline_hints": parsed_data.get("timeline_hints"),
            "budget_hints": parsed_data.get("budget_hints"),
            "tech_hints": parsed_data.get("tech_hints", [])
        }

    except KeyError as e:
        error_msg = f"Configuration Error: Missing API key - {str(e)}"
        print(f"Error during extraction: {error_msg}")
        return {
            **state,
            "project_type": None,
            "industry": None,
            "deliverables": [],
            "timeline_hints": None,
            "budget_hints": None,
            "tech_hints": [],
            "error": f"{error_msg}\n\nPlease ensure OPENAI_API_KEY is set in your .env file.",
            "is_complete": False
        }

    except TimeoutError as e:
        error_msg = "API Timeout: The OpenAI API request timed out"
        print(f"Error during extraction: {error_msg}")
        return {
            **state,
            "project_type": None,
            "industry": None,
            "deliverables": [],
            "timeline_hints": None,
            "budget_hints": None,
            "tech_hints": [],
            "error": f"{error_msg}\n\nThe service took too long to respond. Please try again in a moment.",
            "is_complete": False
        }

    except ValueError as e:
        # JSON parsing errors
        error_msg = f"Data Processing Error: Unable to understand the response format"
        print(f"Error during extraction: {error_msg} - {str(e)}")
        return {
            **state,
            "project_type": None,
            "industry": None,
            "deliverables": [],
            "timeline_hints": None,
            "budget_hints": None,
            "tech_hints": [],
            "error": f"{error_msg}\n\nThere was a problem processing the AI response. Please try again.",
            "is_complete": False
        }

    except Exception as e:
        error_msg = f"Unexpected Error: Extraction failed - {type(e).__name__}"
        print(f"Error during extraction: {error_msg}: {str(e)}")
        return {
            **state,
            "project_type": None,
            "industry": None,
            "deliverables": [],
            "timeline_hints": None,
            "budget_hints": None,
            "tech_hints": [],
            "error": f"{error_msg}\n\nSomething unexpected happened. Please check your input and try again.",
            "is_complete": False
        }
