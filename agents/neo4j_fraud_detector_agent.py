from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph
from langgraph_swarm import create_handoff_tool
from tools.mcp_tools import get_all_mcp_tools # Import the function to get tools
import logging
from config.config import GOOGLE_API_KEY, INTELLIGENCE_AGENT, FRAUD_DETECTOR_AGENT
from prompts.prompt import FRAUD_DETECTOR_PROMPT
from core.state import State
from utils.message_utils import TrimMessagesNode

logger = logging.getLogger(__name__)

class Neo4jFraudDetectorAgent:
    """
    LLM-driven agent specialized for fraud detection.
    It binds all available MCP tools to its LLM.
    """

    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set.")
        self.name = FRAUD_DETECTOR_AGENT  
        self.model = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.0-flash", temperature=0.1)
        self.system_prompt = FRAUD_DETECTOR_PROMPT
        self.tools = [] # Will be set externally or loaded async - Tools are loaded async in main and passed, or loaded once here if synchronous
        
    async def initialize_tools(self):
        """Initializes MCP tools"""
        self.tools = await get_all_mcp_tools()
        if not self.tools:
            logger.warning("No MCP tools found for Neo4jFraudDetectorAgent.")

        # Create a handoff tool to give control to the Intelligent Agent 
        transfer_to_intelligent_agent = create_handoff_tool(
            agent_name=INTELLIGENCE_AGENT,
            description="Transfer user to Intelligent Agent"
        )
        self.tools.append(transfer_to_intelligent_agent)

        logger.info(f"Neo4jFraudDetectorAgent initialized with {len(self.tools)} tools.")

    async def create_agent(self) -> CompiledGraph:
        # Initialize tools if not already initialized
        if not self.tools:
            await self.initialize_tools()

        # Initialize and compile the agent
        neo4j_fraud_detector_agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=SystemMessage(content=self.system_prompt),
            pre_model_hook=TrimMessagesNode(max_messages=5, include_system=True),
            state_schema=State,
            name=self.name,
        )

        return neo4j_fraud_detector_agent