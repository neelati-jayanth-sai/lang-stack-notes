from __future__ import annotations

from langchain_core.language_models import BaseChatModel

from state import WorkflowState



def supervisor_node(state: WorkflowState, llm: BaseChatModel, callbacks: list, max_steps: int) -> dict:
    step_count = state["step_count"] + 1

    if step_count >= max_steps:
        return {"next_agent": "end", "step_count": step_count}

    if not state["research_notes"]:
        return {"next_agent": "research", "step_count": step_count}
    if not state["analysis_notes"]:
        return {"next_agent": "analysis", "step_count": step_count}
    if not state["draft"]:
        return {"next_agent": "writer", "step_count": step_count}
    if not state["approved"]:
        return {"next_agent": "reviewer", "step_count": step_count}

    return {"next_agent": "end", "step_count": step_count}
