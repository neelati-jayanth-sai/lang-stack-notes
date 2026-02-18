# 15 - Runnables and LCEL Primitives

## Runnable Interface

Most modern LangChain components implement the Runnable contract.

Core methods:
- `invoke(input)` for single call
- `batch(inputs)` for multiple inputs
- `ainvoke(input)` for async
- `stream(input)` for streamed outputs/events

## LCEL Building Blocks

Common primitives from `langchain_core.runnables`:
- `RunnableLambda`: wrap Python functions
- `RunnablePassthrough`: keep original input while extending pipeline
- `RunnableParallel`: run branches concurrently and merge outputs
- `RunnableBranch`: route by condition

## Composition Patterns

### Sequential pipe

```python
chain = preprocess | prompt | model | parser
```

### Parallel fan-out

```python
branches = RunnableParallel(summary=summary_chain, bullets=bullet_chain)
```

### Conditional route

```python
router = RunnableBranch((is_math, math_chain), default_chain)
```

## When to Use Runnables

Use runnables when you need composable, testable units but do not yet require a full graph runtime.
If you need persistent state, loops, or complex control flow, move to LangGraph.
