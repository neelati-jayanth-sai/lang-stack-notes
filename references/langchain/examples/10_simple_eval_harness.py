from dataclasses import dataclass


@dataclass
class EvalCase:
    question: str
    expected_keyword: str


def evaluate(response: str, expected_keyword: str) -> bool:
    return expected_keyword.lower() in response.lower()


def main() -> None:
    # Replace with chain/model calls in real projects.
    generated = {
        "What is RAG?": "RAG combines retrieval and generation to ground answers.",
        "What is LangGraph?": "LangGraph is stateful orchestration for LLM workflows.",
    }

    cases = [
        EvalCase(question="What is RAG?", expected_keyword="retrieval"),
        EvalCase(question="What is LangGraph?", expected_keyword="stateful"),
    ]

    passed = 0
    for case in cases:
        ok = evaluate(generated.get(case.question, ""), case.expected_keyword)
        print(f"{case.question} -> {'PASS' if ok else 'FAIL'}")
        passed += int(ok)

    print(f"Score: {passed}/{len(cases)}")


if __name__ == "__main__":
    main()
