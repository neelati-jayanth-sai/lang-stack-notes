from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def build_vector_store() -> FAISS:
    docs = [
        "LangGraph is a framework for stateful, multi-step LLM workflows.",
        "LangChain provides model, prompt, tool, and retrieval building blocks.",
        "RAG improves factuality by retrieving relevant context before generation.",
    ]
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_texts(docs, embedding=embeddings)


def main() -> None:
    load_dotenv()

    vector_store = build_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    query = "How does RAG improve answer quality?"
    retrieved_docs = retriever.invoke(query)
    context = "\n".join(doc.page_content for doc in retrieved_docs)

    prompt = ChatPromptTemplate.from_template(
        "Use only the context below to answer.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = (prompt | model).invoke({"context": context, "question": query})

    print(response.content)


if __name__ == "__main__":
    main()
