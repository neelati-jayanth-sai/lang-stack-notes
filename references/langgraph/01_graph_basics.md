# 01 - Graph Basics

## State

State is a typed dictionary (or `TypedDict`) shared across nodes.

```python
class MyState(TypedDict):
    query: str
    answer: str
```

## Nodes

Each node is a function that receives state and returns a partial state update.

```python
def answer_node(state: MyState) -> dict:
    return {"answer": f"Echo: {state['query']}"}
```

## Edges

Connect nodes using `START` and `END`.

## Mental Model

- LangChain: component composition
- LangGraph: workflow runtime and control flow
