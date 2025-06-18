from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from core.state import MessagesState # Use the extended MessagesState
from tools.mcp_tools import get_all_mcp_tools # Import the function to get tools
import logging
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class Neo4jGenericAgent:
    """
    LLM-driven agent for general database queries and modifications.
    It binds all available MCP tools to its LLM.
    """ 

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.model = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.1)

        # Tools are loaded async in main and passed, or loaded once here if synchronous
        # For simplicity in this agent's __init__, we'll assume tools are available later.
        self.tools = [] # Will be set externally or loaded async

        self.checkpointer = InMemorySaver() # Initialize the checkpointer

        with open("prompts/generic_llm_agent.prompt", "r") as f: # Load the system prompt
            self.system_prompt_template = f.read()

    async def initialize_tools(self):
        """Initializes and binds tools to the LLM. Call this once."""
        self.tools = await get_all_mcp_tools()
        if not self.tools:
            logger.warning("No MCP tools found for GenericLLMAgent.")
        else:
            logger.info(f"GenericLLMAgent initialized with {len(self.tools)} tools.")

    async def run(self, state: MessagesState) -> MessagesState:
        logger.info(f"Generic LLM Agent: Processing messages...")

        if not self.tools:
            await self.initialize_tools()

        neo4j_generic_agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=SystemMessage(content=self.system_prompt_template),
            checkpointer=self.checkpointer,
            name="neo4j_generic_agent",
        )

        return neo4j_generic_agent

neo4j_generic_agent = Neo4jGenericAgent()