# LangChain + LangGraph References (Python 3.12)

This repository includes broad references for LangChain and LangGraph plus project-style implementations.

## Python Version

All content targets **Python 3.12**.

## Structure

- `langchain/`: components, chains, RAG, tools, agents, eval, security, optimization, deployment
- `langgraph/`: graph orchestration, routing, subgraphs, loops/retries, checkpoints, streaming, testing
- `projects/`: end-to-end reference projects
- `requirements-py312.txt`: dependency baseline for the core examples

## New Project: Multi-Agent + Langfuse

- `projects/multi_agent_langfuse/`: detailed supervisor-style multi-agent workflow with Langfuse tracing
- Start at `references/projects/multi_agent_langfuse/README.md`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r references\requirements-py312.txt
```

Create `.env` in workspace root:

```env
OPENAI_API_KEY=your_key_here
```

## Learning Flow

1. Start with `references/langchain/README.md`
2. Continue with `references/langgraph/README.md`
3. Use `references/projects/` for integrated, production-style examples
