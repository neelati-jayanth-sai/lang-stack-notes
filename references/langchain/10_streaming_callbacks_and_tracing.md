# 10 - Streaming, Callbacks, and Tracing

## Streaming

Streaming improves UX by returning tokens/events incrementally.

Common stream types:
- model tokens
- tool call events
- chain/graph step events

## Callback Handlers

Callbacks let you collect runtime telemetry:
- start/end of model call
- token usage
- errors and retries
- per-step latency

## Tracing

Trace each request with:
- request ID
- prompt version
- model name/version
- tool calls
- final output and citations

## Practical Advice

- log structured JSON, not plain text
- redact sensitive fields before logging
- keep a replay path for failed runs
