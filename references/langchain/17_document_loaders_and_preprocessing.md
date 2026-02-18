# 17 - Document Loaders and Preprocessing

## Role of Document Loaders

Loaders convert external sources into LangChain `Document` objects.
Each document typically includes:
- `page_content`
- `metadata`

## Typical Loaders

From `langchain_community.document_loaders`:
- `TextLoader`
- `DirectoryLoader`
- `CSVLoader`
- `PyPDFLoader` (PDF)
- `WebBaseLoader` (web pages)

## Preprocessing Checklist

Before indexing:
- normalize whitespace and encoding
- remove repeated headers/footers
- enrich metadata (source, section, timestamps)
- deduplicate near-identical chunks

## Loader Design Rules

- loaders should be idempotent
- keep source IDs stable across re-index runs
- isolate parsing failures per file and continue ingestion

## Example Pattern

1. load documents
2. clean and tag metadata
3. split into chunks
4. embed and store in vector index
