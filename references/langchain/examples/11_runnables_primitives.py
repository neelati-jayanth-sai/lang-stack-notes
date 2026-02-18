from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough


def main() -> None:
    lower = RunnableLambda(lambda x: x.lower())
    word_count = RunnableLambda(lambda x: len(x.split()))

    pipeline = RunnablePassthrough() | RunnableParallel(
        normalized=lower,
        words=word_count,
    )

    out = pipeline.invoke("LangChain Runnables Are Composable")
    print(out)


if __name__ == "__main__":
    main()
