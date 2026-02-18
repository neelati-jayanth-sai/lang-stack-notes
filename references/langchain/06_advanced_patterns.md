# 06 - Advanced Patterns

## Advanced Building Blocks

- structured outputs with Pydantic models
- fallback chains and retries
- guardrails for policy/safety
- streaming token responses
- async orchestration for throughput

## Structured Outputs

Use schema-bound outputs to reduce parser fragility.

## Reliability

- retries for transient failures
- timeout budgets per step
- idempotent tool design

## Evaluation

Create a regression set and run it in CI:
- correctness
- groundedness
- latency
- cost

## Migration to LangGraph

Use LangChain for components and LangGraph when you need explicit stateful control flow.
