from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class BasicState(TypedDict):
    text: str
    result: str


def uppercase_node(state: BasicState) -> dict:
    return {"result": state["text"].upper()}


def main() -> None:
    graph_builder = StateGraph(BasicState)
    graph_builder.add_node("uppercase", uppercase_node)
    graph_builder.add_edge(START, "uppercase")
    graph_builder.add_edge("uppercase", END)

    graph = graph_builder.compile()
    output = graph.invoke({"text": "hello langgraph", "result": ""})
    print(output)


if __name__ == "__main__":
    main()
