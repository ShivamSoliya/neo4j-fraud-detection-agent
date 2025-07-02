import asyncio
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.neo4j_intelligence_agent import Neo4jIntelligenceAgent
import uuid

async def test_agent():
    neo4j_intelligence_agent = await Neo4jIntelligenceAgent().create_agent()

    user_thread_id = uuid.uuid4()

    full_response_content = []

    async for message in neo4j_intelligence_agent.astream(
        {"messages": [
            {"role": "user", 
            "content": "Show me current graph schema"}
            ]}, 
            {"configurable": {
                "thread_id": str(user_thread_id)  # Convert UUID to string
            }},
            stream_mode="messages"):

            full_response_content.append(message[0])
    
    return full_response_content

if __name__ == "__main__":
    print(asyncio.run(test_agent()))
    