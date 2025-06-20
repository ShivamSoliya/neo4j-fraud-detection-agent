from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from tools.mcp_tools import get_all_mcp_tools # Import the function to get tools
import logging
from config.config import GOOGLE_API_KEY
logger = logging.getLogger(__name__)

class Neo4jGenericAgent:
    """
    LLM-driven agent for general database queries and modifications.
    It binds all available MCP tools to its LLM.
    """ 

    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set.")
        self.model = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.0-flash", temperature=0.1)

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

    async def create_agent(self) -> StateGraph:
        """
        Initializes the agent and starts processing messages.
        Loads tools if they haven't been loaded yet.
        """
        if not self.tools:
            await self.initialize_tools()

        neo4j_generic_agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=SystemMessage(content=self.system_prompt_template),
            checkpointer=self.checkpointer,
            # interrupt_before=["write_neo4j_cypher"],
            name="neo4j_generic_agent",
        )

        return neo4j_generic_agent