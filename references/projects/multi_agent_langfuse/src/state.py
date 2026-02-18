from __future__ import annotations

from typing import Literal, TypedDict


class WorkflowState(TypedDict):
    user_task: str
    langfuse_session_id: str
    langfuse_user_id: str
    langfuse_tags: list[str]
    research_notes: str
    analysis_notes: str
    draft: str
    review_feedback: str
    approved: bool
    next_agent: Literal["research", "analysis", "writer", "reviewer", "end"]
    step_count: int
    final_answer: str
