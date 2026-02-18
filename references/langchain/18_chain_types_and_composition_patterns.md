# 18 - Chain Types and Composition Patterns

## Practical Chain Types

- prompt-model-parser chain (basic)
- retrieval chain (RAG)
- tool-augmented chain
- classification + route chain
- validation/repair chain

## Composition Patterns

### 1. Linear chain
Simple, low-latency path.

### 2. Router chain
Classify intent and route to specialized subchains.

### 3. Parallel enrichment chain
Run multiple analyses in parallel, then aggregate.

### 4. Guardrail sandwich
Input validation -> core chain -> output policy check.

## Error and Retry Design

- assign timeout per stage
- retry only retryable failures
- use fallback chain for graceful degradation
- include request IDs in logs/traces

## Chain vs Graph Decision

- choose chain for straightforward request-response logic
- choose graph when stateful multi-step control flow is needed
