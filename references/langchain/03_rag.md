# 03 - RAG (Retrieval-Augmented Generation)

## RAG Flow

1. chunk source text
2. embed chunks
3. store in vector DB
4. retrieve top-k relevant chunks
5. answer with grounded context

## Minimal Components

- splitter: `RecursiveCharacterTextSplitter`
- embeddings: `OpenAIEmbeddings`
- vector store: `FAISS`
- retriever: `vectorstore.as_retriever()`

## Prompt Design for RAG

Use strict grounding:
- answer only from context
- say when context is insufficient
- return citations/chunk IDs when possible

## Failure Modes

- bad chunking strategy
- noisy top-k retrieval
- hallucination when prompt does not enforce grounding

## Improve Quality

- use overlap for chunking
- tune `k`
- add re-ranking
- evaluate with known Q/A sets
