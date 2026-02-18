import asyncio
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


async def main() -> None:
    load_dotenv()

    prompt = ChatPromptTemplate.from_template("Give a one-line definition of {topic}.")
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | model | StrOutputParser()

    topics = ["LangChain", "LangGraph", "RAG", "tool calling"]
    tasks = [chain.ainvoke({"topic": topic}) for topic in topics]
    results = await asyncio.gather(*tasks)

    for topic, result in zip(topics, results, strict=True):
        print(f"{topic}: {result}")


if __name__ == "__main__":
    asyncio.run(main())
