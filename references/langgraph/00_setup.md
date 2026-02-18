# 00 - LangGraph Setup

## What LangGraph Adds

LangGraph is a stateful orchestration framework built for complex LLM workflows.
Use it when simple prompt chains are not enough.

Typical use cases:
- conditional routing
- loops and retries
- human-in-the-loop checkpoints
- multi-agent coordination
- long-running workflows with persisted state

## Install (Python 3.12)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r references\requirements-py312.txt
```

## Core Concept

A LangGraph app is:
- a typed state
- nodes that read/write state
- edges that define flow
- optional persistence/checkpointing
