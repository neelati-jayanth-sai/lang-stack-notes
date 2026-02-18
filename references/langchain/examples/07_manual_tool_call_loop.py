from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


TOOLS = {"add": add}


def main() -> None:
    load_dotenv()

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([add])

    messages = [("human", "What is 19 + 23? Use tools if needed.")]
    ai_msg = model.invoke(messages)

    if ai_msg.tool_calls:
        for call in ai_msg.tool_calls:
            name = call["name"]
            args = call["args"]
            tool_output = TOOLS[name].invoke(args)
            messages.append(ai_msg)
            messages.append(("tool", str(tool_output)))

        final_msg = model.invoke(messages)
        print(final_msg.content)
    else:
        print(ai_msg.content)


if __name__ == "__main__":
    main()
