from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class ChildState(TypedDict):
    text: str
    transformed: str


class ParentState(TypedDict):
    input_text: str
    output_text: str


def child_transform_node(state: ChildState) -> dict:
    return {"transformed": state["text"].upper()}


def build_child_graph():
    child = StateGraph(ChildState)
    child.add_node("transform", child_transform_node)
    child.add_edge(START, "transform")
    child.add_edge("transform", END)
    return child.compile()


def run_child_node(state: ParentState) -> dict:
    child_graph = build_child_graph()
    result = child_graph.invoke({"text": state["input_text"], "transformed": ""})
    return {"output_text": result["transformed"]}


def main() -> None:
    parent = StateGraph(ParentState)
    parent.add_node("run_child", run_child_node)
    parent.add_edge(START, "run_child")
    parent.add_edge("run_child", END)

    graph = parent.compile()
    result = graph.invoke({"input_text": "subgraph demo", "output_text": ""})
    print(result)


if __name__ == "__main__":
    main()
