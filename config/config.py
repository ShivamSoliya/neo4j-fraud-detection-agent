import os
from dotenv import load_dotenv

load_dotenv(override=True) # Load environment variables from .env file

# Neo4j Connection Details (used by MCP servers if run via uvx)
# Ensure these match what you expect the MCP servers to use.
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD") # IMPORTANT: Update your .env
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE") # New, as used in client config

# Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Agent names
INTELLIGENCE_AGENT = os.getenv("INTELLIGENCE_AGENT")
FRAUD_DETECTOR_AGENT = os.getenv("FRAUD_DETECTOR_AGENT")

