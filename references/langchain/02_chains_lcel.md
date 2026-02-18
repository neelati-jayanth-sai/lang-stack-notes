# 02 - Chains (LCEL)

## What a Chain Is

A chain is a reusable pipeline that transforms input to output.

Common chain steps:
- input preprocessing
- prompting
- model call
- output parsing

## Example: Prompt -> Model -> Parser

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()
text = chain.invoke({"topic": "RAG"})
```

## Batch and Async

```python
results = chain.batch([
    {"topic": "agents"},
    {"topic": "tools"}
])
```

## Why LCEL Matters

- easier testing for each stage
- better observability
- cleaner extension to advanced pipelines
