# Proposal Generator Agent

A learning project demonstrating **LangGraph** fundamentals through a real-world AI-powered proposal generator.

## Purpose

This project is designed to teach the **basic building blocks of LangGraph** - how to create stateful multi-step AI workflows using nodes, edges, and state management.

The proposal generator use case (extracting requirements, calculating costs, generating proposals) is just an example to demonstrate these concepts in action. The business logic (cost calculations, timeline estimates, etc.) is simplified to keep the focus on **learning LangGraph patterns**.

**This is a learning resource, not a production tool.** Feel free to fork it, modify the business logic, or replace the use case entirely while keeping the LangGraph architecture.

## What You'll Learn

- **State Management**: How to define and pass state between nodes using TypedDict
- **Nodes**: Creating processing units that transform state
- **Edges**: Connecting nodes with conditional routing logic
- **Graph Building**: Composing nodes and edges into a complete workflow
- **LangChain Integration**: Using LangChain tools within LangGraph nodes
- **Testing**: Writing comprehensive tests for LangGraph workflows

## Tech Stack

- **LangGraph**: Stateful AI workflow framework
- **LangChain**: LLM orchestration and tooling
- **OpenAI GPT**: Language model for extraction and generation
- **Python 3.12+**: Programming language

## Project Structure

```
proposal-generator-agent/
├── src/
│   ├── main.py              # Graph definition and entry point
│   ├── state.py             # State TypedDict definition
│   ├── nodes/               # Processing nodes
│   │   ├── extraction.py    # Extract requirements from user input
│   │   ├── validation.py    # Validate completeness
│   │   ├── calculator.py    # Calculate costs and timeline
│   │   ├── sanity_check.py  # Detect unrealistic requirements
│   │   └── generation.py    # Generate final proposal
│   └── tools/
│       └── calculator.py    # Cost calculation logic
├── tests/                   # Test suite (15+ test cases)
├── docs/
│   └── learning.md          # Complete knowledge base
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md                # You are here
```

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/proposal-generator-agent.git
cd proposal-generator-agent
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate it:
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your OpenAI API Key
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=your-api-key-here
```

**Where to get an API key**: Sign up at [platform.openai.com](https://platform.openai.com) and create an API key in your account settings.

### 5. Test the Application

Before running, you can customize the test input in `src/main.py`:

**Open `src/main.py` and modify line 79:**
```python
"user_input": """Need e-commerce site in 2 weeks""",
```

Change this to your own project description. Examples:
```python
"user_input": """Build a mobile app for food delivery with user authentication, restaurant listings, and payment integration""",

"user_input": """Create a SaaS dashboard for analytics with real-time data visualization, user management, and API integration""",

"user_input": """Develop a healthcare patient portal with appointment scheduling, medical records, and telemedicine features""",
```

Then run:
```bash
python src/main.py
```

The system will walk through the workflow:
1. Extract requirements (project type, deliverables, timeline, budget, tech)
2. Validate completeness
3. Calculate costs and timeline
4. Check for unrealistic expectations
5. Generate a proposal

You'll see the complete output showing each step of the process!

## Understanding the Code

Start by reading these files in order:

1. **`src/state.py`** - Understand the state structure
2. **`src/main.py`** - See how the graph is built
3. **`src/nodes/extraction.py`** - See how a node works
4. **`docs/learning.md`** - Complete deep dive into the entire system

## Running Tests

```bash
# Run the full automated test suite (15 test cases)
python tests/automated_test_suite.py

# Run individual tests
python tests/test_timeline.py
python tests/test_sanity_check.py
```

## Contributing

This is an **open source learning project** and contributions are welcome! Whether you want to:

- Improve the documentation
- Add new test cases
- Enhance the business logic
- Fix bugs
- Add new features
- Create tutorials or examples

Feel free to open an issue or submit a pull request.

### Ideas for Contributions

- Add new node types (e.g., risk assessment, competitor analysis)
- Improve the calculator logic with ML-based estimation
- Add support for multiple languages
- Create a web interface
- Add more comprehensive test coverage
- Improve error handling
- Add logging and monitoring

## Contact

**Awais Qarni**
Email: awais.qarni87@gmail.com

If you have questions, suggestions, or just want to connect and discuss LangGraph, feel free to reach out!

## License

Open source - feel free to use this project for learning, teaching, or building your own LangGraph applications.

---

**Remember**: The goal is to learn LangGraph patterns. The proposal generator is just the vehicle for that learning. Fork it and build something amazing!
