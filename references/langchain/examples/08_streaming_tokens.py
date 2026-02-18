from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main() -> None:
    load_dotenv()

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    for chunk in model.stream("Explain LangChain in one short paragraph."):
        if chunk.content:
            print(chunk.content, end="")

    print()


if __name__ == "__main__":
    main()
