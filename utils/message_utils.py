from langmem.short_term import SummarizationNode, summarize_messages, asummarize_messages
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage, AIMessage
from typing import Any
from pydantic import BaseModel
from langgraph.utils.runnable import RunnableCallable

class TrimMessagesNode(RunnableCallable):
    def __init__(self, max_messages: int = 10, include_system: bool = True) -> None:
        self.max_messages = max_messages
        self.include_system = include_system
        super().__init__(self._func, self._afunc, name="trim_messages")

    def _func(self, input: dict[str, Any] | BaseModel)-> dict[str, Any]:
        return self._trim_messages(input)

    async def _afunc(self, input: dict[str, Any] | BaseModel)-> dict[str, Any]:
        return self._trim_messages(input)

    def _trim_messages(self, input):
        system_messages = [m for m in input["messages"] if m.type == "system"] if self.include_system else []
        other_messages = [m for m in input["messages"] if m.type != "system"]
        
        total_messages = len(other_messages)

        # If fewer than max_messages exist, take whatever is available
        if total_messages <= self.max_messages:
            return {"trimmed_messages": input["messages"]}

        start_idx = total_messages - self.max_messages
        last_n_messages = other_messages[start_idx:]

        # If first message isn’t human, move start_idx back while possible
        while start_idx > 0 and last_n_messages[0].type != "human":
            start_idx -= 1
            last_n_messages = other_messages[start_idx:start_idx + self.max_messages]

        return {"trimmed_messages": system_messages + last_n_messages}

class CustomSummarizationNode(SummarizationNode):
    def _func(self, input: dict[str, Any] | BaseModel) -> dict[str, Any]:
        
        print(input)
        messages, context = self._parse_input(input)

        # 🔹 Split messages
        preserved = [m for m in messages if isinstance(m, (SystemMessage, ToolMessage))]
        interaction = [m for m in messages if isinstance(m, (HumanMessage, AIMessage))]
        for message in interaction:
            if message.content.strip() == "":
                message.content = f"[Tool call]"
            if message.content.strip() == "":
                interaction.remove(message)

        print("\nInteraction: ", [message.content for message in interaction])

        # 🔹 Summarize only interaction messages
        result = summarize_messages(
            interaction,
            running_summary=context.get("running_summary"),
            model=self.model,
            max_tokens=self.max_tokens,
            max_tokens_before_summary=self.max_tokens_before_summary,
            max_summary_tokens=self.max_summary_tokens,
            token_counter=self.token_counter,
            initial_summary_prompt=self.initial_summary_prompt,
            existing_summary_prompt=self.existing_summary_prompt,
            final_prompt=self.final_prompt,
        )

        # 🔹 Combine preserved + summary result
        result.messages = preserved + result.messages  # preserve order: system/tool → summary

        return self._prepare_state_update(context, result)

    async def _afunc(self, input: dict[str, Any] | BaseModel) -> dict[str, Any]:
        
        print(input)
        messages, context = self._parse_input(input)

        # 🔹 Split messages
        preserved = [m for m in messages if isinstance(m, (SystemMessage, ToolMessage))]
        interaction = [m for m in messages if isinstance(m, (HumanMessage, AIMessage))]
        for message in interaction:
            if message.content.strip() == "":
                message.content = f"[Tool call]"
            if message.content.strip() == "":
                interaction.remove(message)

        print("\nInteraction: ", [message.content for message in interaction])

        result = await asummarize_messages(
            interaction,
            running_summary=context.get("running_summary"),
            model=self.model,
            max_tokens=self.max_tokens,
            max_tokens_before_summary=self.max_tokens_before_summary,
            max_summary_tokens=self.max_summary_tokens,
            token_counter=self.token_counter,
            initial_summary_prompt=self.initial_summary_prompt,
            existing_summary_prompt=self.existing_summary_prompt,
            final_prompt=self.final_prompt,
        )

        result.messages = preserved + result.messages

        return self._prepare_state_update(context, result)
