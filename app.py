import streamlit as st
import asyncio
from agents.supervisor import SupervisorAgent
from langgraph.graph import StateGraph
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('langchain_mcp_adapters').setLevel(logging.WARNING)
logging.getLogger('mcp').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def run_fraud_detection_workflow() -> StateGraph:
    """
    Runs the fraud detection workflow.
    """
    logger.info("Starting fraud detection workflow...")
    supervisor_agent = SupervisorAgent()
    supervisor_workflow = await supervisor_agent.run()
    app = supervisor_workflow.compile()
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

async def get_response(app, prompt):
    try:
        # Create a placeholder for the assistant message
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Stream responses
            full_response = ""
            async for token in app.astream(
                {"messages": [{"role": "user", "content": prompt}]},
                stream_mode="messages"
            ):
                if isinstance(token, tuple) and len(token) > 0:
                    message_chunk = token[0]
                    if hasattr(message_chunk, 'content'):
                        # Skip internal agent messages
                        content = message_chunk.content
                        if any(keyword in content.lower() for keyword in [
                            "transferring back to", 
                            "successfully transferred back to",
                            "ok. i'm back under your control",
                            "[]"
                        ]):
                            continue
                        
                        # Update the response with the new chunk
                        full_response += content
                        # Update the placeholder with the full response so far
                        message_placeholder.markdown(full_response)
                        
                        # Add the complete message to chat history when finished
                        if hasattr(message_chunk, 'response_metadata') and \
                           isinstance(message_chunk.response_metadata, dict) and \
                           'finish_reason' in message_chunk.response_metadata:
                            # Clean up the final response
                            cleaned_response = full_response.strip()
                            if cleaned_response:
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": cleaned_response
                                })
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        st.error("An error occurred while processing your message.")
        # Add error message to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": "An error occurred while processing your message."
        })


async def main():
    # Create workflow
    app = await run_fraud_detection_workflow()
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Streamlit UI
    st.title("Fraud Detection Chatbot")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response from the LangGraph app
        await get_response(app, prompt)

if __name__ == "__main__":
    asyncio.run(main())
