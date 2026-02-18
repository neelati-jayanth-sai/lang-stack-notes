from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot_node(state: ChatState) -> dict:
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(state["messages"])
    return {"messages": [response]}


def main() -> None:
    load_dotenv()

    graph_builder = StateGraph(ChatState)
    graph_builder.add_node("chatbot", chatbot_node)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph = graph_builder.compile()
    output = graph.invoke({"messages": [("human", "Give one line on LangGraph") ]})

    print(output["messages"][-1].content)


if __name__ == "__main__":
    main()
