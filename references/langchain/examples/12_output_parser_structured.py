from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI


class Incident(BaseModel):
    severity: Literal["low", "medium", "high"]
    team: str
    summary: str


def main() -> None:
    load_dotenv()

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    extractor = model.with_structured_output(Incident)

    result = extractor.invoke(
        "Database is down for checkout service in production. Customer orders failing."
    )
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
