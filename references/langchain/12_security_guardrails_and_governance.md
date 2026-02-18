# 12 - Security, Guardrails, and Governance

## Core Risks

- prompt injection
- data exfiltration
- unsafe tool execution
- PII leakage

## Guardrail Layers

- input validation and classification
- prompt hardening
- retrieval filtering by access policy
- tool permission boundaries
- output moderation and policy checks

## Prompt Injection Defenses

- separate instructions from data
- never treat retrieved text as trusted instructions
- enforce tool allowlists and argument schemas

## Data Governance

- redact PII before logs/traces
- define retention windows
- isolate tenant data in retrieval layer
- track model/provider and prompt versions
