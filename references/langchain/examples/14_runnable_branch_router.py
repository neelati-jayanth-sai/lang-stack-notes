from langchain_core.runnables import RunnableBranch, RunnableLambda


def is_math(text: str) -> bool:
    tokens = ["+", "-", "*", "/", "calculate"]
    return any(t in text.lower() for t in tokens)


def main() -> None:
    math_chain = RunnableLambda(lambda q: "Math route selected")
    general_chain = RunnableLambda(lambda q: "General route selected")

    router = RunnableBranch((is_math, math_chain), general_chain)

    print(router.invoke("calculate 8*9"))
    print(router.invoke("explain what langchain is"))


if __name__ == "__main__":
    main()
