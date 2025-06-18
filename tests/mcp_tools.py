import sys
from pathlib import Path
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from tools.mcp_tools import *

async def main():
    try:
        logger.info("Starting test of MCP tools")
        tools = await get_all_mcp_tools()
        logger.info(f"Retrieved {len(tools)} tools")
        print(f"Retrieved {len(tools)} tools")
        print(tools)
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main())