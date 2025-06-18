import sys
from pathlib import Path
import logging  
from typing import List
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool

# Add the project root directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

logger = logging.getLogger(__name__)

# Initialize MultiServerMCPClient once globally.
# This client will manage the lifecycle of the MCP servers.
# The 'env' variables are passed to the spawned server processes.
_mcp_client_instance = MultiServerMCPClient(
    {
        "neo4j-cypher": {
            "command": "uvx",
            "args": ["mcp-neo4j-cypher@0.2.3"], # Ensure this package is installed via pip
            "transport": "stdio",
            "env": {
                "NEO4J_URI": NEO4J_URI,
                "NEO4J_USERNAME": NEO4J_USERNAME,
                "NEO4J_PASSWORD": NEO4J_PASSWORD,
                "NEO4J_DATABASE": NEO4J_DATABASE
            }
        }
    }
)

async def get_all_mcp_tools() -> List[BaseTool]:
    """
    Retrieves all available LangChain tools from the initialized MultiServerMCPClient.
    """
    try:
        logger.info("Starting to get tools from MCP servers")
        logger.info(f"MCP client configuration: {_mcp_client_instance}")
        tools = await _mcp_client_instance.get_tools()
        logger.info(f"Successfully retrieved {len(tools)} tools from MCP servers.")
        return tools
    except Exception as e:
        logger.error(f"Failed to retrieve tools from MCP servers: {e}")
        logger.error(f"MCP client configuration: {_mcp_client_instance}")
        return []

# Note: The tools themselves (BaseTool objects) will be passed to the LLMs.
# The methods like execute_dynamic_query from the previous adapter are no longer directly called by agents; the LLM generates a tool call which ToolNode executes.
