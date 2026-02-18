from __future__ import annotations

from dataclasses import dataclass
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def search_kb(query: str) -> str:
    """Search a tiny mock knowledge base."""
    db = {
        "langchain": "LangChain provides composable building blocks for LLM apps.",
        "langgraph": "LangGraph provides stateful orchestration for multi-step workflows.",
        "rag": "RAG combines retrieval with generation to improve grounding.",
    }
    q = query.lower()
    for k, v in db.items():
        if k in q:
            return v
    return "No exact match in KB."


@tool
def calc(expression: str) -> str:
    """Evaluate a simple math expression safely for +,-,*,/."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed):
        return "Invalid expression"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception:
        return "Calculation failed"


TOOLS = {"search_kb": search_kb, "calc": calc}


@dataclass
class AgentConfig:
    max_steps: int = 4


def run_agent(user_question: str, cfg: AgentConfig) -> str:
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([search_kb, calc])

    messages: list = [
        (
            "system",
            "You are a planner-executor assistant. Use tools when helpful, then provide final concise answer.",
        ),
        ("human", user_question),
    ]

    for _ in range(cfg.max_steps):
        ai_msg = model.invoke(messages)
        messages.append(ai_msg)

        if not ai_msg.tool_calls:
            return ai_msg.content or "No response generated."

        for call in ai_msg.tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]
            tool_out = TOOLS[tool_name].invoke(tool_args)
            messages.append(("tool", str(tool_out)))

    return "Stopped due to max_steps guard."


def main() -> None:
    load_dotenv()

    q = "What is LangGraph and also calculate 18*7?"
    answer = run_agent(q, AgentConfig(max_steps=4))
    print(answer)


if __name__ == "__main__":
    main()
