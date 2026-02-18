from typing import Literal, TypedDict
from langgraph.graph import END, START, StateGraph


class RouteState(TypedDict):
    question: str
    route: Literal["math", "general"]
    answer: str


def route_node(state: RouteState) -> dict:
    text = state["question"].lower()
    if any(token in text for token in ["+", "-", "*", "/", "calculate"]):
        return {"route": "math"}
    return {"route": "general"}


def math_node(state: RouteState) -> dict:
    return {"answer": "Math path selected. Plug in a real calculator tool here."}


def general_node(state: RouteState) -> dict:
    return {"answer": "General path selected. Plug in an LLM response node here."}


def choose_next(state: RouteState) -> str:
    return state["route"]


def main() -> None:
    graph_builder = StateGraph(RouteState)
    graph_builder.add_node("route", route_node)
    graph_builder.add_node("math", math_node)
    graph_builder.add_node("general", general_node)

    graph_builder.add_edge(START, "route")
    graph_builder.add_conditional_edges("route", choose_next)
    graph_builder.add_edge("math", END)
    graph_builder.add_edge("general", END)

    graph = graph_builder.compile()

    out1 = graph.invoke({"question": "calculate 10*3", "route": "general", "answer": ""})
    out2 = graph.invoke({"question": "what is langgraph?", "route": "general", "answer": ""})

    print(out1)
    print(out2)


if __name__ == "__main__":
    main()
