from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class LoopState(TypedDict):
    draft: str
    attempts: int
    max_attempts: int
    done: bool


def refine_node(state: LoopState) -> dict:
    attempts = state["attempts"] + 1
    improved = f"Draft attempt {attempts}: clearer answer"
    done = attempts >= state["max_attempts"]
    return {"draft": improved, "attempts": attempts, "done": done}


def route_next(state: LoopState) -> str:
    return END if state["done"] else "refine"


def main() -> None:
    graph_builder = StateGraph(LoopState)
    graph_builder.add_node("refine", refine_node)
    graph_builder.add_edge(START, "refine")
    graph_builder.add_conditional_edges("refine", route_next)

    graph = graph_builder.compile()
    result = graph.invoke({"draft": "", "attempts": 0, "max_attempts": 3, "done": False})
    print(result)


if __name__ == "__main__":
    main()
