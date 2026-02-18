# 13 - Performance and Cost Optimization

## Main Levers

- smaller model where acceptable
- tighter prompts
- retrieval pruning
- response length caps
- caching

## Caching Levels

- embedding cache
- retrieval result cache
- model response cache (careful with personalization)

## Throughput

- async model calls
- batch embedding/index operations
- separate online and offline workloads

## Observability Metrics

- tokens per request
- cost per request
- p50/p95 latency
- cache hit rate

Tune one lever at a time and measure impact.
