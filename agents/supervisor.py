from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph_supervisor import create_supervisor
from agents.neo4j_generic_agent import neo4j_generic_agent
from agents.neo4j_fraud_detector import neo4j_fraud_detector_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
import logging
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class SupervisorAgent:
    """
    Agent responsible for overseeing the entire process, making decisions,
    routing requests, and formulating the final response.
    """
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.model = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.1)

        with open("prompts/supervisor_router.prompt", "r") as f:
            self.router_prompt_template = f.read()

        self.checkpointer = InMemorySaver() # Initialize the checkpointer

    async def run(self) -> StateGraph:
        logger.info(f"Supervisor Agent: Processing messages...")

        supervisor_workflow = create_supervisor(
            agents=[neo4j_generic_agent, neo4j_fraud_detector_agent],
            model=self.model,
            prompt=SystemMessage(content=self.router_prompt_template),
            checkpointer=self.checkpointer,
            name="supervisor_agent",
        )

        return supervisor_workflow

supervisor_workflow = SupervisorAgent()