from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class EventState(TypedDict):
    text: str
    result: str


def process_node(state: EventState) -> dict:
    return {"result": state["text"].title()}


def main() -> None:
    graph_builder = StateGraph(EventState)
    graph_builder.add_node("process", process_node)
    graph_builder.add_edge(START, "process")
    graph_builder.add_edge("process", END)

    graph = graph_builder.compile()

    for event in graph.stream({"text": "langgraph event stream", "result": ""}):
        print(event)


if __name__ == "__main__":
    main()
