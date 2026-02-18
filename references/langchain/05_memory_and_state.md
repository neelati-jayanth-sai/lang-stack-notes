# 05 - Memory and State

## Important Distinction

- short-term chat history: in-session conversational context
- long-term memory: persisted user/project data

## Practical Rule

Store only what improves future behavior. Too much history hurts quality and cost.

## Patterns

- rolling window memory
- summary memory for long sessions
- retrieval-backed memory for user profiles and docs

## In Production

- persist memory in DB/vector store
- version prompts and memory schema
- redact sensitive data before persistence
