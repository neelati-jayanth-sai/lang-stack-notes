from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader


def main() -> None:
    demo_dir = Path("references/langchain/examples/_demo_docs")
    demo_dir.mkdir(parents=True, exist_ok=True)

    (demo_dir / "a.txt").write_text("LangChain is for LLM components.", encoding="utf-8")
    (demo_dir / "b.txt").write_text("LangGraph is for stateful orchestration.", encoding="utf-8")

    loader = DirectoryLoader(
        str(demo_dir),
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()

    for i, doc in enumerate(docs, start=1):
        print(f"{i}. {doc.metadata.get('source')} -> {doc.page_content}")


if __name__ == "__main__":
    main()
