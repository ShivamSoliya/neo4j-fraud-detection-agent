from typing import List, Dict, Any, TypedDict, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState as LangGraphMessagesState # Alias to avoid name collision

class MessagesState(LangGraphMessagesState):
    """
    Extends LangGraph's MessagesState to include additional fields
    for fraud detection workflow and user confirmation.
    """
    # 'messages' field is inherited from LangGraphMessagesState
    messages: List[BaseMessage]
    user_confirmation: Literal["yes", "no", None] # User's response for acceptance
    pending_tool_call_query: str # The Cypher/SQL query from the tool call awaiting confirmation
    awaiting_confirmation: bool # Flag to indicate if we're waiting for user input
    error: str # Store any errors encountered during the process
    db_schema_context: str # Context retrieved from MCP (if needed for LLM insight)
    uploaded_file_content: str # Content of an uploaded file (e.g., CSV)
    current_agent: Literal["generic_llm", "fraud_llm", "supervisor", "user_confirmation", "initial", "tool_execution"] # Tracks current agent/stage
    visualization_html: str # HTML content for visualizing graph data
    # We remove 'generated_cypher', 'query_language', 'db_results', 'fraud_analysis_result', 'decision'
    # as they will either be part of the 'messages' history or dynamically processed.
    # We might add 'final_response' if supervisor needs to craft a final summary
    final_response: str