import asyncio
from langgraph.graph.graph import CompiledGraph
import logging
import uuid
from core.workflow import compile_fraud_detection_workflow

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def stream_messages(app: CompiledGraph, user_input: str, user_thread_id: uuid.UUID):
    print("Assistant: ", end="")

    async for message in app.astream(
        {"messages": [
            {"role": "user", "content": user_input}
        ]},
        {"configurable": {"thread_id": str(user_thread_id)}},
        stream_mode="messages"
    ):
        msg = message[0]

        # Add normal content if present
        if msg.content and msg.type not in ("tool"):
            print(msg.content, end="")

        # Add tool call info if present
        func_call = msg.additional_kwargs.get("function_call")
        if func_call:
            func_name = func_call.get("name", "unknown_function")
            func_args = func_call.get("arguments", "{}")
            print(f"Tool call: {func_name} | args: {func_args}\n", end="")
        
        # Add tool result if this is a tool message
        if msg.type == "tool":
            print(f"Tool result: {msg.content}\n", end="")

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

        await stream_messages(app, user_input, user_thread_id)

if __name__ == "__main__":
    asyncio.run(run_fraud_detection_workflow())
