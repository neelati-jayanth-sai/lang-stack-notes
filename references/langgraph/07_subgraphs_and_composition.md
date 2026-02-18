# 07 - Subgraphs and Composition

## Why Subgraphs

Subgraphs let you package reusable workflow units (e.g., retrieval, drafting, review).

Benefits:
- modular graph design
- clearer ownership boundaries
- easier testing per module

## Composition Pattern

1. build child graph for a specific concern
2. call child graph from a parent node
3. merge child output into parent state

## Practical Use Cases

- reusable RAG module
- shared safety/guardrail module
- standard approval module
