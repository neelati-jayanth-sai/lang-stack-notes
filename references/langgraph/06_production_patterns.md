# 06 - Production Patterns

## Reliability

- retry transient failures per node
- timeouts and circuit breakers
- idempotent side-effect nodes

## Observability

Track:
- per-node latency
- token/cost usage
- branch frequency
- failure categories

## Testing Strategy

- unit test each node
- integration test graph paths
- regression test critical prompts and routes

## Deployment Checklist

- stable state schema
- checkpoint store configured
- PII redaction in logs
- fallback behavior documented
