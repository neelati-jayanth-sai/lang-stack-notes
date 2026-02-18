from __future__ import annotations

from langchain_core.language_models import BaseChatModel

from state import WorkflowState
from tools.mock_tools import quick_web_research



def research_node(state: WorkflowState, llm: BaseChatModel, callbacks: list, prompt_resolver) -> dict:
    tool_result = quick_web_research.invoke({"topic": state["user_task"]})
    resolved = prompt_resolver(
        "research",
        {
            "task": state["user_task"],
            "source_notes": tool_result,
        },
    )

    msg = llm.invoke(
        resolved["messages"],
        config={
            "callbacks": callbacks,
            "metadata": {
                "agent": "research",
                "workflow": "multi_agent_langfuse",
                "prompt_name": resolved["prompt_name"],
                "prompt_label": resolved["prompt_label"],
                "prompt_source": resolved["source"],
                "langfuse_session_id": state["langfuse_session_id"],
                "langfuse_user_id": state["langfuse_user_id"],
                "langfuse_tags": state["langfuse_tags"],
            },
        },
    )
    return {"research_notes": msg.content}
