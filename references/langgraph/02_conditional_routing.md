# 02 - Conditional Routing

## Why Routing Matters

Real systems choose different paths based on runtime state.

Examples:
- FAQ question -> retrieval path
- arithmetic question -> calculator tool
- high-risk request -> safety review node

## Pattern

1. classifier node writes `route`
2. conditional edge dispatches to target node
3. branch node writes result

## Design Tip

Keep routing logic deterministic and inspectable.
