from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class ReviewState(TypedDict):
    draft: str
    approved: bool
    final: str


def draft_node(state: ReviewState) -> dict:
    return {"draft": "This is a generated draft answer."}


def human_review_node(state: ReviewState) -> dict:
    # Local demo for Python scripts: manual CLI input simulates human approval.
    decision = input("Approve draft? (yes/no): ").strip().lower()
    return {"approved": decision == "yes"}


def finalize_node(state: ReviewState) -> dict:
    if state["approved"]:
        return {"final": state["draft"]}
    return {"final": "Draft rejected by reviewer."}


def main() -> None:
    graph_builder = StateGraph(ReviewState)
    graph_builder.add_node("draft", draft_node)
    graph_builder.add_node("human_review", human_review_node)
    graph_builder.add_node("finalize", finalize_node)

    graph_builder.add_edge(START, "draft")
    graph_builder.add_edge("draft", "human_review")
    graph_builder.add_edge("human_review", "finalize")
    graph_builder.add_edge("finalize", END)

    graph = graph_builder.compile()
    result = graph.invoke({"draft": "", "approved": False, "final": ""})

    print(result)


if __name__ == "__main__":
    main()
