# 08 - Loops, Retries, and Error Paths

## Controlled Loops

Loops are useful for iterative refinement, but must be bounded.

Add controls:
- `attempt_count`
- `max_attempts`
- explicit stop criteria

## Retry Strategy

For transient failures:
- retry specific nodes only
- backoff between attempts
- route to fallback after max retries

## Error State Design

Track in state:
- `last_error`
- `error_type`
- `retryable`

This makes behavior testable and observable.
