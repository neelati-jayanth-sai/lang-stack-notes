# 03 - State, Reducers, and Persistence

## Persistent Threads

Use checkpointers to persist state across turns (thread-based memory).

## Reducers

Reducers merge values over time (useful for message lists or logs).

## Practical Guidance

- keep state schema explicit
- avoid putting large raw documents directly in state
- store IDs/keys and fetch heavy payloads from storage
- version state shape for migrations
