from langmem.short_term import SummarizationNode, summarize_messages, asummarize_messages
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage, AIMessage
from typing import Any
from pydantic import BaseModel

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