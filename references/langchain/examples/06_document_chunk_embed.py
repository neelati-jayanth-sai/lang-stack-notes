from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def main() -> None:
    load_dotenv()

    text = (
        "LangChain is a framework for building LLM applications. "
        "LangGraph adds stateful orchestration. "
        "RAG combines retrieval with generation to improve factual answers."
    )

    splitter = RecursiveCharacterTextSplitter(chunk_size=70, chunk_overlap=15)
    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vs = FAISS.from_texts(chunks, embedding=embeddings)

    docs = vs.similarity_search("What improves factual answers?", k=2)
    for i, doc in enumerate(docs, start=1):
        print(f"{i}. {doc.page_content}")


if __name__ == "__main__":
    main()
