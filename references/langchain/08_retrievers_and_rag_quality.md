# 08 - Retrievers and RAG Quality

## Retriever Types

- similarity search
- Max Marginal Relevance (MMR)
- metadata-filtered retrieval
- hybrid retrieval (keyword + vector)

## Query Transformation

Improve recall with:
- multi-query generation
- query rewriting
- hypothetical answer generation (HyDE)

## Context Construction

After retrieval:
- deduplicate overlapping chunks
- sort by relevance and recency
- enforce token budget
- include citation IDs in prompt context

## Grounded Prompt Pattern

Use a strict contract:
- answer from context only
- say "insufficient context" when needed
- cite chunk/source IDs

## Quality Evaluation

Track:
- retrieval recall@k
- answer groundedness
- citation correctness
- latency and token usage

## Frequent RAG Failures

- bad chunk boundaries
- stale index
- wrong metadata filters
- too much irrelevant context
- prompt not strict enough on grounding
