from typing import Literal, TypedDict
from langgraph.graph import END, START, StateGraph


class TeamState(TypedDict):
    task: str
    next_worker: Literal["researcher", "writer"]
    notes: str
    output: str


def supervisor_node(state: TeamState) -> dict:
    if "research" in state["task"].lower():
        return {"next_worker": "researcher"}
    return {"next_worker": "writer"}


def researcher_node(state: TeamState) -> dict:
    return {"notes": "Collected key facts and constraints."}


def writer_node(state: TeamState) -> dict:
    return {"output": f"Final response using notes: {state.get('notes', '')}"}


def route_after_supervisor(state: TeamState) -> str:
    return state["next_worker"]


def main() -> None:
    graph_builder = StateGraph(TeamState)
    graph_builder.add_node("supervisor", supervisor_node)
    graph_builder.add_node("researcher", researcher_node)
    graph_builder.add_node("writer", writer_node)

    graph_builder.add_edge(START, "supervisor")
    graph_builder.add_conditional_edges("supervisor", route_after_supervisor)
    graph_builder.add_edge("researcher", "writer")
    graph_builder.add_edge("writer", END)

    graph = graph_builder.compile()
    result = graph.invoke(
        {"task": "Research LangGraph adoption patterns", "next_worker": "writer", "notes": "", "output": ""}
    )

    print(result)


if __name__ == "__main__":
    main()
