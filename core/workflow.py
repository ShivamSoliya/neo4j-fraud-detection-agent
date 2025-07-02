from agents.neo4j_intelligence_agent import Neo4jIntelligenceAgent
from agents.neo4j_fraud_detector_agent import Neo4jFraudDetectorAgent
from langgraph.graph.graph import CompiledGraph
from langgraph.checkpoint.memory import InMemorySaver
import logging
from langgraph_swarm import create_swarm

logger = logging.getLogger(__name__)


async def compile_fraud_detection_workflow() -> CompiledGraph:
    """
    Creates the fraud detection workflow.
    """
    logger.info("Starting fraud detection workflow...")
    
    # Initialize and run the agents
    neo4j_fraud_detector_agent = await Neo4jFraudDetectorAgent().create_agent()
    
    neo4j_intelligence_agent = await Neo4jIntelligenceAgent().create_agent()
    
    fraud_detection_workflow = create_swarm(
        agents=[neo4j_intelligence_agent, neo4j_fraud_detector_agent],
        default_active_agent="neo4j_intelligence_agent"
    )

    app = fraud_detection_workflow.compile(
        checkpointer=InMemorySaver()
    )
    logger.info("LangGraph workflow compiled.")
    
    try:
        # Save workflow graph as PNG
        graph_image = app.get_graph().draw_mermaid_png()
        graph_filename = "workflow_graph.png"
        with open(graph_filename, "wb") as f:
            f.write(graph_image)
        print(f"\nGraph image saved to {graph_filename}")
    except Exception as e:
        logger.warning(f"Could not save graph image: {e}")
    
    return app