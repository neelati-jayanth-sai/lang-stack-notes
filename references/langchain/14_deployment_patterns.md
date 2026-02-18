# 14 - Deployment Patterns

## Architecture Patterns

- synchronous API for chat UX
- background workers for long jobs
- event-driven ingestion for index updates

## Config Management

Externalize:
- model IDs
- prompt templates
- retrieval settings
- feature flags

## Reliability Checklist

- retries with backoff
- timeout budgets
- dead-letter queues for failed jobs
- idempotency keys for side effects

## Versioning

Version these independently:
- prompts
- model config
- retrieval index
- tool contracts

## Rollout

- shadow traffic or canary release
- monitor quality + cost before full rollout
