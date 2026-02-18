from __future__ import annotations

from langchain_core.language_models import BaseChatModel

from state import WorkflowState



def reviewer_node(state: WorkflowState, llm: BaseChatModel, callbacks: list, prompt_resolver) -> dict:
    resolved = prompt_resolver(
        "reviewer",
        {
            "task": state["user_task"],
            "draft": state["draft"],
        },
    )

    msg = llm.invoke(
        resolved["messages"],
        config={
            "callbacks": callbacks,
            "metadata": {
                "agent": "reviewer",
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

    text = msg.content or ""
    approved = "decision: approve" in text.lower()

    if approved:
        return {
            "approved": True,
            "review_feedback": text,
            "next_agent": "end",
            "final_answer": state["draft"],
        }

    # Clear draft so supervisor routes back to writer for a revision pass.
    return {
        "approved": False,
        "review_feedback": text,
        "next_agent": "writer",
        "draft": "",
    }
