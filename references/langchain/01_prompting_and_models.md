# 01 - Prompting and Models

## Prompt Templates

Use prompt templates to avoid hardcoded string concatenation and make prompts auditable.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise technical assistant."),
    ("human", "Explain {topic} in 3 bullet points.")
])
```

## Model Configuration

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    timeout=30,
    max_retries=2,
)
```

## LCEL Composition

LangChain Expression Language (LCEL) lets you compose runnables with `|`.

```python
chain = prompt | model
result = chain.invoke({"topic": "vector embeddings"})
```

## Best Practices

- keep system prompts short and specific
- pass user variables explicitly
- set deterministic temperature for tests (`0`)
- log prompts and model responses in development
