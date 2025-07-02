from langchain_core.messages import AIMessageChunk
from pprint import pprint

a_list = [(AIMessageChunk(content='Hello', additional_kwargs={}, response_metadata={'safety_ratings': []}, id='run--48fff1c7-667c-4676-bbca-5e84ac437c17', usage_metadata={'input_tokens': 742, 'output_tokens': 0, 'total_tokens': 742, 'input_token_details': {'cache_read': 0}}), {'thread_id': '102cf368-1982-41b5-b8a9-301ffa60d235', 'langgraph_step': 2, 'langgraph_node': 'agent', 'langgraph_triggers': ('branch:to:agent',), 'langgraph_path': ('__pregel_pull', 'agent'), 'langgraph_checkpoint_ns': 'agent:c1a696e2-b3f1-5d45-c743-2e9654dc1568', 'checkpoint_ns': 'agent:c1a696e2-b3f1-5d45-c743-2e9654dc1568', 'ls_provider': 'google_genai', 'ls_model_name': 'gemini-2.0-flash', 'ls_model_type': 'chat', 'ls_temperature': 0.1, 'LANGSMITH_ENDPOINT': 'https://api.smith.langchain.com', 'LANGSMITH_PROJECT': 'pr-elderly-undertaker-21', 'LANGSMITH_TRACING': 'true', 'revision_id': '18453e5-dirty'}), (AIMessageChunk(content=", I am the neo4j_intelligence_agent. I'm here to help", additional_kwargs={}, response_metadata={'safety_ratings': []}, id='run--48fff1c7-667c-4676-bbca-5e84ac437c17', usage_metadata={'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0, 'input_token_details': {'cache_read': 0}}), {'thread_id': '102cf368-1982-41b5-b8a9-301ffa60d235', 'langgraph_step': 2, 'langgraph_node': 'agent', 'langgraph_triggers': ('branch:to:agent',), 'langgraph_path': ('__pregel_pull', 'agent'), 'langgraph_checkpoint_ns': 'agent:c1a696e2-b3f1-5d45-c743-2e9654dc1568', 'checkpoint_ns': 'agent:c1a696e2-b3f1-5d45-c743-2e9654dc1568', 'ls_provider': 'google_genai', 'ls_model_name': 'gemini-2.0-flash', 'ls_model_type': 'chat', 'ls_temperature': 0.1, 'LANGSMITH_ENDPOINT': 'https://api.smith.langchain.com', 'LANGSMITH_PROJECT': 'pr-elderly-undertaker-21', 'LANGSMITH_TRACING': 'true', 'revision_id': '18453e5-dirty'}), (AIMessageChunk(content=' you understand and analyze your Neo4j graph database. I can process your requests, perform', additional_kwargs={}, response_metadata={'safety_ratings': []}, id='run--48fff1c7-667c-4676-bbca-5e84ac437c17', usage_metadata={'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0, 'input_token_details': {'cache_read': 0}}), {'thread_id': '102cf368-1982-41b5-b8a9-301ffa60d235', 'langgraph_step': 2, 'langgraph_node': 'agent', 'langgraph_triggers': ('branch:to:agent',), 'langgraph_path': ('__pregel_pull', 'agent'), 'langgraph_checkpoint_ns': 'agent:c1a696e2-b3f1-5d45-c743-2e9654dc1568', 'checkpoint_ns': 'agent:c1a696e2-b3f1-5d45-c743-2e9654dc1568', 'ls_provider': 'google_genai', 'ls_model_name': 'gemini-2.0-flash', 'ls_model_type': 'chat', 'ls_temperature': 0.1, 'LANGSMITH_ENDPOINT': 'https://api.smith.langchain.com', 'LANGSMITH_PROJECT': 'pr-elderly-undertaker-21', 'LANGSMITH_TRACING': 'true', 'revision_id': '18453e5-dirty'}), (AIMessageChunk(content=' graph analysis, identify patterns, and provide insights into your data. Just let me know what you need!\n', additional_kwargs={}, response_metadata={'finish_reason': 'STOP', 'model_name': 'gemini-2.0-flash', 'safety_ratings': []}, id='run--48fff1c7-667c-4676-bbca-5e84ac437c17', usage_metadata={'input_tokens': -91, 'output_tokens': 59, 'total_tokens': -32, 'input_token_details': {'cache_read': 0}}), {'thread_id': '102cf368-1982-41b5-b8a9-301ffa60d235', 'langgraph_step': 2, 'langgraph_node': 'agent', 'langgraph_triggers': ('branch:to:agent',), 'langgraph_path': ('__pregel_pull', 'agent'), 'langgraph_checkpoint_ns': 'agent:c1a696e2-b3f1-5d45-c743-2e9654dc1568', 'checkpoint_ns': 'agent:c1a696e2-b3f1-5d45-c743-2e9654dc1568', 'ls_provider': 'google_genai', 'ls_model_name': 'gemini-2.0-flash', 'ls_model_type': 'chat', 'ls_temperature': 0.1, 'LANGSMITH_ENDPOINT': 'https://api.smith.langchain.com', 'LANGSMITH_PROJECT': 'pr-elderly-undertaker-21', 'LANGSMITH_TRACING': 'true', 'revision_id': '18453e5-dirty'}), (AIMessageChunk(content='', additional_kwargs={'function_call': {'name': 'AgentOutput', 'arguments': '{"next_agent": "neo4j_intelligence_agent", "message": "Hello, I am the neo4j_intelligence_agent. I\'m here to help you understand and analyze your Neo4j graph database. I can process your requests, perform graph analysis, identify patterns, and provide insights into your data. Just let me know what you need!"}'}}), {'thread_id': '102cf368-1982-41b5-b8a9-301ffa60d235', 'langgraph_step': 3, 'langgraph_node': 'generate_structured_response', 'langgraph_triggers': ('branch:to:generate_structured_response',), 'langgraph_path': ('__pregel_pull', 'generate_structured_response'), 'langgraph_checkpoint_ns': 'generate_structured_response:3b30b928-ccd6-3f17-aacc-c98f690ca06f', 'checkpoint_ns': 'generate_structured_response:3b30b928-ccd6-3f17-aacc-c98f690ca06f', 'ls_provider': 'google_genai', 'ls_model_name': 'gemini-2.0-flash', 'ls_model_type': 'chat', 'ls_temperature': 0.1, 'LANGSMITH_ENDPOINT': 'https://api.smith.langchain.com', 'LANGSMITH_PROJECT': 'pr-elderly-undertaker-21', 'LANGSMITH_TRACING': 'true', 'revision_id': '18453e5-dirty'})]

# pprint(a_list)
# Iterate through each tuple in the list
for i, (ai_message_chunk, metadata_dict) in enumerate(a_list):
    print(f"--- Tuple {i+1} ---")

    # Access values from the AIMessageChunk object
    print(f"  AIMessageChunk Content: '{ai_message_chunk.content}'")
    print(f"  AIMessageChunk ID: '{ai_message_chunk.id}'")
    # You can access other attributes like additional_kwargs, response_metadata, usage_metadata, tool_calls, etc.
    # For example:
    if ai_message_chunk.additional_kwargs:
        print(f"  AIMessageChunk additional_kwargs: {ai_message_chunk.additional_kwargs}")
    if ai_message_chunk.tool_calls:
        print(f"  AIMessageChunk tool_calls: {ai_message_chunk.tool_calls}")

    # Access values from the metadata dictionary using keys
    print(f"  Metadata - thread_id: '{metadata_dict.get('thread_id')}'")
    print(f"  Metadata - langgraph_step: {metadata_dict.get('langgraph_step')}")
    print(f"  Metadata - ls_model_name: '{metadata_dict.get('ls_model_name')}'")
    print(f"  Metadata - LANGSMITH_PROJECT: '{metadata_dict.get('LANGSMITH_PROJECT')}'")

    # You can access any key present in the metadata_dict
    # To see all keys in a dictionary:
    # print(f"  All Metadata Keys: {metadata_dict.keys()}")

    # Example of accessing nested information, e.g., 'function_call' within 'additional_kwargs'
    if 'function_call' in ai_message_chunk.additional_kwargs:
        function_call_info = ai_message_chunk.additional_kwargs['function_call']
        print(f"  Function Call Name: {function_call_info.get('name')}")
        print(f"  Function Call Arguments: {function_call_info.get('arguments')}")

    print("\n")