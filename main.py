import logging
import asyncio
from core.workflow import supervisor_workflow
from tools.mcp_tools import close_mcp_client # Import the closer
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_fraud_detection_workflow(user_query: str, uploaded_file_content: str = None):
    """
    Runs the fraud detection workflow for a given user query.
    Can also include uploaded file content for ingestion.
    """
    logger.info(f"--- Starting Fraud Detection for: '{user_query}' ---")

    app = supervisor_workflow.compile()
    logger.info("LangGraph workflow compiled.")

    async for state in app.astream(initial_state):
        # Print only the latest history entry for brevity in the console output
        latest_history = state.get('history')[-1] if state.get('history') else 'N/A'
        print(f"\n--- Current State --- (Agent: {state.get('current_agent')})")
        print(f"Latest Action/Status: {latest_history}")

        # Check for user confirmation prompt
        if state.get("current_agent") == "user_confirmation_stage" and state.get("awaiting_confirmation"):
            print(f"\nAI proposes the following database operation for execution:")
            print(f"```cypher\n{state.get('pending_tool_call_query')}\n```")
            response = input("Do you approve this operation? (yes/no): ").lower().strip()
            state["user_confirmation"] = "yes" if response == "yes" else "no"
            state["awaiting_confirmation"] = False # Reset flag after getting input
            # Send the updated state back into the graph to resume
            await app.aupdate(state)
            continue # Continue the async for loop

        # Print visualization HTML if available
        if state.get("visualization_html"):
            print("\n--- Visualization Generated ---")
            print("Please see the immersive document below for the visualization.")
            # Present the visualization in an immersive block
            print(f"http://googleusercontent.com/immersive_entry_chip/0")
            state["visualization_html"] = "" # Clear after displaying

        # Check for final response from LLM agent or supervisor
        if state.get("final_response"):
            print(f"\n--- Final Response ---")
            print(state["final_response"])
            break # Exit the loop if a final response is ready

        # Check for immediate END from LangGraph
        if "__end__" in state:
            print("\n--- Workflow Ended Directly ---")
            break

    # Final Summary (after loop finishes or breaks)
    final_state_after_loop = state

    print("\n--- Workflow Summary ---")
    print(f"Initial Query: {user_query}")
    print(f"Final Outcome: {final_state_after_loop.get('final_response', 'No explicit final response (check history).')}")
    print("\n--- Full Message History ---")
    for msg in final_state_after_loop['messages']:
        print(msg)
    print("\n--- Internal History/Logs ---")
    for entry in final_state_after_loop['history']:
        print(entry)
    print("----------------------------")


async def main():
    try:
        # Example Usage: Generic Agent - Querying data model (read-only, no confirmation needed)
        await run_fraud_detection_workflow("Show me the current graph data model.")
        await run_fraud_detection_workflow("Find all transactions involving account ABC123.")
        await run_fraud_detection_workflow("Visualize connections between John Doe and all his accounts.")

        # Example Usage: Generic Agent - Modifying data (requires user confirmation)
        print("\n=== Test Case: Create Node (requires confirmation) ===")
        await run_fraud_detection_workflow("Create a new person node named 'Jane Doe' with an email 'jane@example.com'.")
        print("\n=== Test Case: Add Relationship (requires confirmation) ===")
        await run_fraud_detection_workflow("Add a new relationship 'FOLLOWS' from Alice to Bob.")

        # Example Usage: Fraud Detection Agent - Analyzing (no file)
        print("\n=== Test Case: Detect Fraud (no file) ===")
        await run_fraud_detection_workflow("Detect fraud patterns in the database.")

        # Example Usage: Fraud Detection Agent - Ingesting file (requires user confirmation for data modeling)
        sample_csv_content = """
id,sender,receiver,amount,timestamp,ip_address
txn1,Alice,Bob,100,2023-01-01T10:00:00,192.168.1.1
txn2,Bob,Charlie,150,2023-01-01T10:05:00,192.168.1.2
txn3,Charlie,Alice,200,2023-01-01T10:10:00,192.168.1.1 # Alice and Charlie share IP
txn4,David,Eve,5000,2023-01-01T11:00:00,192.168.1.3 # High amount
"""
        print("\n=== Test Case: Ingest CSV for Fraud (requires confirmation) ===")
        await run_fraud_detection_workflow("Ingest this CSV file for fraud analysis.", uploaded_file_content=sample_csv_content)

        print("\n=== Test Case: Invalid Query Example ===")
        await run_fraud_detection_workflow("invalid query example to test error handling")

    except Exception as e:
        logger.error(f"An unhandled error occurred in main: {e}")
    finally:
        # Crucially, close the MultiServerMCPClient instance to shut down its managed servers
        await close_mcp_client()
        logger.info("Application finished. MultiServerMCPClient closed.")

if __name__ == "__main__":
    asyncio.run(main())