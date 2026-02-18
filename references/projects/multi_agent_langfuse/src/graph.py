from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from agents.analyst import analyst_node
from agents.researcher import research_node
from agents.reviewer import reviewer_node
from agents.supervisor import supervisor_node
from agents.writer import writer_node
from config import AppConfig
from llm_factory import build_llm
from state import WorkflowState



def build_workflow(cfg: AppConfig, callbacks: list, prompt_resolver):
    llm = build_llm(cfg)

    builder = StateGraph(WorkflowState)

    builder.add_node("supervisor", lambda s: supervisor_node(s, llm, callbacks, cfg.max_steps))
    builder.add_node("research", lambda s: research_node(s, llm, callbacks, prompt_resolver))
    builder.add_node("analysis", lambda s: analyst_node(s, llm, callbacks, prompt_resolver))
    builder.add_node("writer", lambda s: writer_node(s, llm, callbacks, prompt_resolver))
    builder.add_node("reviewer", lambda s: reviewer_node(s, llm, callbacks, prompt_resolver))

    builder.add_edge(START, "supervisor")

    def route_from_supervisor(state: WorkflowState) -> str:
        return state["next_agent"]

    builder.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "research": "research",
            "analysis": "analysis",
            "writer": "writer",
            "reviewer": "reviewer",
            "end": END,
        },
    )

    builder.add_edge("research", "supervisor")
    builder.add_edge("analysis", "supervisor")
    builder.add_edge("writer", "supervisor")
    builder.add_edge("reviewer", "supervisor")

    return builder.compile()
