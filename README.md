# Proposal Generator Agent

An AI-powered proposal generator built with LangGraph and LangChain.

## Project Structure

```
proposal-generator-agent/
├── src/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes/
│   │   └── __init__.py
│   └── main.py
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

## Usage

```bash
python src/main.py
```
