# 07 - Documents, Chunking, and Embeddings

## Why This Layer Matters

RAG quality starts before retrieval. If documents are loaded and chunked poorly, no retriever can fully recover.

## Document Loading

Typical loaders:
- local text/markdown
- PDF and office docs
- web pages (with cleanup)
- database rows

Normalize text early:
- remove boilerplate/navigation fragments
- preserve source metadata (title, URL, timestamp)
- keep a stable document ID

## Chunking Strategies

Use `RecursiveCharacterTextSplitter` first, then tune:
- chunk size: 300 to 1200 tokens (task-dependent)
- overlap: 10% to 25%
- separators: headings, paragraphs, sentences

Chunking guidelines:
- factual QA: smaller chunks
- reasoning/synthesis: medium chunks
- policy/legal docs: preserve section boundaries

## Embeddings

Embedding model choice impacts recall, latency, and cost.

Operational guidance:
- standardize one embedding model per index
- reindex if embedding model changes
- store embedding model/version in metadata

## Metadata Design

Useful metadata fields:
- `source_id`
- `title`
- `created_at`
- `section`
- `security_label`

Good metadata enables filtering and better retrieval controls.
