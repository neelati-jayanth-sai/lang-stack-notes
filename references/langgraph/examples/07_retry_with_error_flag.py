from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class RetryState(TypedDict):
    tries: int
    max_tries: int
    last_error: str
    success: bool


def flaky_node(state: RetryState) -> dict:
    tries = state["tries"] + 1
    if tries < state["max_tries"]:
        return {"tries": tries, "last_error": "Transient error", "success": False}
    return {"tries": tries, "last_error": "", "success": True}


def choose_next(state: RetryState) -> str:
    if state["success"]:
        return "finish"
    if state["tries"] >= state["max_tries"]:
        return "finish"
    return "flaky"


def finish_node(state: RetryState) -> dict:
    return state


def main() -> None:
    graph_builder = StateGraph(RetryState)
    graph_builder.add_node("flaky", flaky_node)
    graph_builder.add_node("finish", finish_node)
    graph_builder.add_edge(START, "flaky")
    graph_builder.add_conditional_edges("flaky", choose_next)
    graph_builder.add_edge("finish", END)

    graph = graph_builder.compile()
    result = graph.invoke({"tries": 0, "max_tries": 3, "last_error": "", "success": False})
    print(result)


if __name__ == "__main__":
    main()
