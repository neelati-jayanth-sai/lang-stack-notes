# 10 - Streaming and Runtime Events

## Event Types

- node started/completed
- model token stream
- tool invocation events
- failures/retries

## Why Event Streams Matter

- real-time UX feedback
- debugging of stuck workflows
- operational telemetry for SLOs

## Implementation Tips

- attach request/thread IDs to every event
- publish structured JSON events
- include redaction layer before export
