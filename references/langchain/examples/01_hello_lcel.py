from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def main() -> None:
    load_dotenv()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a concise teacher."),
            ("human", "Explain {topic} in 4 short lines."),
        ]
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | model | StrOutputParser()

    response = chain.invoke({"topic": "LangChain LCEL"})
    print(response)


if __name__ == "__main__":
    main()
