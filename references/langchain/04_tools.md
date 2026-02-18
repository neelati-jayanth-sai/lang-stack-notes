# 04 - Tools and Tool Calling

## Why Tools

Tools let models invoke deterministic code for:
- calculations
- API/database reads
- external system actions

## Tool Pattern

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    return a * b
```

Bind tools to a chat model:

```python
model_with_tools = model.bind_tools([multiply])
```

## Operational Advice

- validate tool inputs
- keep tool behavior deterministic
- log tool calls and outputs
- treat tool errors as first-class outcomes
