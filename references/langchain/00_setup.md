# 00 - LangChain Setup

## What LangChain Is

LangChain is an application framework for building LLM-driven systems with composable building blocks:
- models
- prompts
- output parsers
- retrievers and vector stores
- tools and runtime orchestration

## Python 3.12 Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r references\requirements-py312.txt
```

## Core Packages

- `langchain`: high-level APIs
- `langchain-core`: runnable interfaces (LCEL)
- `langchain-openai`: OpenAI integrations
- `langchain-community`: community integrations

## Minimal Smoke Test

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
print(llm.invoke("Say hello in one short line.").content)
```

## API Key

Set `OPENAI_API_KEY` before running examples.

## Recommended Learning Order

1. prompts + models
2. LCEL chains
3. retrieval (RAG)
4. tools
5. memory and state
6. production patterns
