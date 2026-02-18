# 19 - Agents Deep Dive

## What an Agent Really Is

An agent is a control loop that decides the next action at runtime.

Core loop:
1. read objective + current state
2. decide next action (tool call or final answer)
3. execute tool if needed
4. update working context
5. stop when completion criteria are met

## Agent Runtime Model

### Inputs
- user goal
- available tools
- policies/constraints
- current conversation context

### Internal State
- scratchpad (reasoning artifacts)
- tool results
- attempt counter
- budget counters (time/cost/tokens)

### Outputs
- final user-facing answer
- optional structured trace (actions + tool results)

## Planning Styles

### 1) ReAct-style
Interleaves thinking and acting step-by-step.

Use when:
- tools are heterogeneous
- path is uncertain

Tradeoff:
- can be verbose and expensive without strict limits

### 2) Planner + Executor
Planner creates a coarse plan; executor runs each step.

Use when:
- tasks are multi-stage
- auditing and predictability are important

Tradeoff:
- planner errors can propagate unless validation exists

### 3) Supervisor + Specialists
Supervisor routes subtasks to specialized workers.

Use when:
- domain-specific experts exist
- task decomposition quality matters

Tradeoff:
- coordination overhead, conflict resolution complexity

## Tool Strategy

Tool quality determines agent reliability.

Design rules:
- tools must be deterministic when possible
- define strict schemas for args
- return machine-friendly outputs (JSON-like)
- enforce per-tool timeouts
- isolate tool failures (no global crash)

## Stopping Criteria (Mandatory)

Never run open-ended loops in production.

Use hard guards:
- `max_steps`
- `max_wall_time`
- `max_tool_calls`
- `max_token_budget`

And semantic guards:
- answer confidence threshold
- no-progress detection across N steps

## Failure Modes and Fixes

### Infinite or long loops
Fix:
- step limits
- progress checks
- fallback completion path

### Wrong tool selection
Fix:
- better tool descriptions
- router/classifier pre-step
- tool allowlist by intent

### Tool argument hallucination
Fix:
- strict schema validation
- retry with argument-repair prompt

### Expensive behavior
Fix:
- planner-first approach
- smaller model for routing/planning
- cache deterministic tool outputs

## Safety and Governance for Agents

Apply guardrails at three layers:

### Input layer
- prompt injection detection
- intent/risk classification

### Action layer
- tool permission checks
- high-risk action approval gates

### Output layer
- policy moderation
- redaction of sensitive info

## Observability Blueprint

Log each agent step with:
- request ID / thread ID
- chosen action
- tool name + args hash
- tool latency + result status
- token usage per step
- termination reason

This enables postmortems and optimization.

## Testing Agents

Test suites should include:
- happy path tasks
- ambiguous tasks
- adversarial tool-injection attempts
- timeout/failure simulation
- regression set with expected action traces

## Practical Build Sequence

1. start with single-tool loop + strict max steps
2. add schema validation + retries
3. add router/planner
4. add observability and eval harness
5. add policy gates and HITL for risky actions
6. migrate orchestration to LangGraph when branching/state complexity grows

## LangChain vs LangGraph for Agents

- LangChain: quick agent prototypes and tool integration
- LangGraph: production-grade agent runtime with explicit stateful control flow, persistence, and robust branching

## Related Examples in This Folder

- `examples/07_manual_tool_call_loop.py`
- `examples/15_agent_planner_executor_pattern.py`
