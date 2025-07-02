# Neo4j Fraud Detection Agent

A LangGraph-based intelligent agent system for detecting fraud patterns in Neo4j graph databases.

## Features

- Two specialized agents:
  - Neo4j Fraud Detector Agent: Identifies potential fraud patterns
  - Neo4j Intelligence Agent: Analyzes graph data and patterns

- Message management:
  - Custom message trimming for efficient processing
  - Async message handling support

## Setup

1. Install dependencies using uv:
```bash
uv pip install .
```

2. Configure:
- Set up Neo4j connection details in `config/config.py`
- Configure API keys in `config/config.py`

3. Run:
```bash
uv run main.py
```

## Usage

Interact with the agents through the command line interface:
- Ask questions about your Neo4j graph
- Request fraud pattern analysis
- Get intelligent insights from your graph data

## Project Structure

```
langgraph_fraud_detection/
├── agents/           # Agent implementations
├── config/          # Configuration files
├── core/            # Core application logic
├── prompts/         # Prompt templates
├── tests/           # Test files
└── utils/           # Utility functions
```

## License

MIT License