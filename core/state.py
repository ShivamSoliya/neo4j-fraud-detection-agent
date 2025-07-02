from typing import Any
from langchain_core.messages import BaseMessage
from langgraph.prebuilt.chat_agent_executor import AgentState

class State(AgentState):
    """
    State of the agent

    Inherited class with predefined attributes:
    ``` python
        class AgentState(TypedDict):
            The state of the agent.

            messages: Annotated[Sequence[BaseMessage], add_messages]
            is_last_step: IsLastStep
            remaining_steps: RemainingSteps
    ```
    Additional attributes:
    """
    context: dict[str, Any]
    llm_input_messages: list[BaseMessage]
    active_agent: str # This key will store the summarized messages, intended for the LLM input. It does not need the 'add_messages' reducer if SummarizationNode overwrites it.