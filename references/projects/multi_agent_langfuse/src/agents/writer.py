from __future__ import annotations

from langchain_core.language_models import BaseChatModel

from state import WorkflowState



def writer_node(state: WorkflowState, llm: BaseChatModel, callbacks: list, prompt_resolver) -> dict:
    resolved = prompt_resolver(
        "writer",
        {
            "task": state["user_task"],
            "research_notes": state["research_notes"],
            "analysis_notes": state["analysis_notes"],
        },
    )

    msg = llm.invoke(
        resolved["messages"],
        config={
            "callbacks": callbacks,
            "metadata": {
                "agent": "writer",
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
    return {"draft": msg.content}
