from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


@tool
def days_to_hours(days: int) -> int:
    """Convert days to hours."""
    return days * 24


def main() -> None:
    load_dotenv()

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    model_with_tools = model.bind_tools([multiply, days_to_hours])

    messages = [
        (
            "human",
            "If a task takes 6 days and repeats 3 times, how many total hours is that?",
        )
    ]

    ai_msg = model_with_tools.invoke(messages)
    print("Model response (may include tool calls):")
    print(ai_msg)


if __name__ == "__main__":
    main()
