# 11 - Evaluation and Testing

## Test Pyramid for LLM Apps

1. unit tests: tools, parsers, prompt helpers
2. integration tests: chain + retriever + model mocks
3. regression tests: fixed evaluation dataset

## Evaluation Dimensions

- task correctness
- groundedness/hallucination rate
- formatting/schema compliance
- latency and cost

## Dataset Design

Include:
- easy, medium, hard prompts
- adversarial/ambiguous inputs
- out-of-distribution cases

## CI Strategy

- run deterministic checks each PR
- run model-in-loop nightly
- compare against baseline metrics

## Release Gate

Set objective thresholds (example):
- groundedness >= 95%
- schema failures <= 1%
- p95 latency <= target
