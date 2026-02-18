from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class ConceptSummary(BaseModel):
    topic: str = Field(description="The requested topic")
    key_points: list[str] = Field(description="Exactly 3 concise points")


def main() -> None:
    load_dotenv()

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_model = model.with_structured_output(ConceptSummary)

    prompt = ChatPromptTemplate.from_template(
        "Summarize {topic} for a beginner in exactly 3 key points."
    )

    chain = prompt | structured_model
    result = chain.invoke({"topic": "retrieval augmented generation"})

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
