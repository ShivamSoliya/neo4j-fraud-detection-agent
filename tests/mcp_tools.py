"""
This script tests the MCP tools by retrieving and printing them.
"""

import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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