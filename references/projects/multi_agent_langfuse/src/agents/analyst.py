from __future__ import annotations

from langchain_core.language_models import BaseChatModel

from state import WorkflowState
from tools.mock_tools import risk_scan



def analyst_node(state: WorkflowState, llm: BaseChatModel, callbacks: list, prompt_resolver) -> dict:
    risk_notes = risk_scan.invoke({"topic": state["user_task"]})
    resolved = prompt_resolver(
        "analysis",
        {
            "task": state["user_task"],
            "research_notes": state["research_notes"],
            "risk_notes": risk_notes,
        },
    )

    msg = llm.invoke(
        resolved["messages"],
        config={
            "callbacks": callbacks,
            "metadata": {
                "agent": "analysis",
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
    return {"analysis_notes": msg.content}
