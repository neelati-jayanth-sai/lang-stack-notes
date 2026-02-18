# 09 - Agents and Planning

## What an Agent Adds

An agent chooses actions dynamically instead of following a fixed chain.

Typical loop:
1. observe user goal
2. decide tool/action
3. execute tool
4. reflect on result
5. continue or finish

## When to Use Agents

Use agents for:
- open-ended tasks with unknown steps
- tool-rich environments
- dynamic branching workflows

Avoid agents for:
- deterministic ETL-like tasks
- strict low-latency paths

## Planning Patterns

- ReAct style (reason + act)
- planner/executor split
- supervisor/specialist model

## Safety Controls

Required in production:
- max iteration limits
- tool allowlists
- argument validation
- cost/time budgets

## LangChain + LangGraph

Use LangChain for components and LangGraph for robust agent runtime (state, branching, retries, persistence).
