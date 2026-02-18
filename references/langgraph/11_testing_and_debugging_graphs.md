# 11 - Testing and Debugging Graphs

## Test Strategy

1. node-level unit tests
2. branch-path integration tests
3. end-to-end scenario tests with representative data

## Assertions to Add

- expected node transitions
- max step counts not exceeded
- state invariants preserved
- fallback path correctness

## Debugging Workflow

- replay from checkpoint
- inspect state diffs per node
- verify routing decisions are deterministic
