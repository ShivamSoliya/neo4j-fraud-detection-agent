from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph_supervisor import create_supervisor
from agents.neo4j_generic_agent import Neo4jGenericAgent
from agents.neo4j_fraud_detector import Neo4jFraudDetectorAgent
from langgraph.graph import StateGraph
import logging
from config.config import GOOGLE_API_KEY

logger = logging.getLogger(__name__)

class SupervisorAgent:
    """
    Agent responsible for overseeing the entire process, making decisions,
    routing requests, and formulating the final response.
    """
    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set.")
        self.model = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.0-flash", temperature=0.1)

        with open("prompts/supervisor_router.prompt", "r") as f:
            self.router_prompt_template = f.read()

    async def run(self) -> StateGraph:

        # Initialize and run the agents
        generic_agent = Neo4jGenericAgent()
        neo4j_generic_agent = await generic_agent.create_agent()

        fraud_detector = Neo4jFraudDetectorAgent()
        neo4j_fraud_detector_agent = await fraud_detector.create_agent()

        supervisor_workflow = create_supervisor(
            agents=[neo4j_generic_agent, neo4j_fraud_detector_agent],
            model=self.model,
            prompt=SystemMessage(content=self.router_prompt_template),
            supervisor_name="supervisor_agent",
        )

        return supervisor_workflow