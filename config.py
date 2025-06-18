import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Neo4j Connection Details (used by MCP servers if run via uvx)
# Ensure these match what you expect the MCP servers to use.
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "your_neo4j_password") # IMPORTANT: Update your .env
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j") # New, as used in client config

# OpenAI (or other LLM) API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
