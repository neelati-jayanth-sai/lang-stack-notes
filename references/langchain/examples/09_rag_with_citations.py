from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def build_store() -> FAISS:
    texts = [
        "[doc-1] LangChain provides reusable components for LLM apps.",
        "[doc-2] LangGraph provides stateful orchestration and control flow.",
        "[doc-3] RAG grounds model answers with retrieved context.",
    ]
    return FAISS.from_texts(texts, embedding=OpenAIEmbeddings(model="text-embedding-3-small"))


def main() -> None:
    load_dotenv()

    store = build_store()
    retrieved = store.similarity_search("Why does RAG reduce hallucinations?", k=2)
    context = "\n".join(d.page_content for d in retrieved)

    prompt = ChatPromptTemplate.from_template(
        "Answer only from context. Cite doc ids like [doc-1].\n\nContext:\n{context}\n\nQ: {q}"
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    out = (prompt | model).invoke({"context": context, "q": "How does RAG help answer quality?"})
    print(out.content)


if __name__ == "__main__":
    main()
