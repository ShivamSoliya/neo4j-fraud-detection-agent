import asyncio
from langgraph.graph.graph import CompiledGraph
import logging
import uuid
from core.workflow import compile_fraud_detection_workflow

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def stream_messages(app: CompiledGraph, user_input: str, user_thread_id: uuid.UUID):
    full_response_content = ""

    async for message in app.astream(
        {"messages": [
            {"role": "user", 
            "content": user_input}
            ]}, 
            {"configurable": {
                "thread_id": str(user_thread_id)  # Convert UUID to string
            }},
            stream_mode="messages"):

            if message[0].content:
                full_response_content += message[0].content
    
    return full_response_content

async def run_fraud_detection_workflow():
    """
    Runs the fraud detection workflow.
    """
    app = await compile_fraud_detection_workflow()
    user_thread_id = uuid.uuid4()

    print("\n")
    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            print("Goodbye!\n")
            break

        full_response_content = await stream_messages(app, user_input, user_thread_id)

        print("Assistant: ", full_response_content)

if __name__ == "__main__":
    asyncio.run(run_fraud_detection_workflow())
