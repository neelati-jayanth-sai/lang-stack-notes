# Architecture

## Goal

A supervisor controls four specialist agents and synthesizes a final response.

Agents:
- `research_agent`: gathers facts and context
- `analyst_agent`: identifies implications and tradeoffs
- `writer_agent`: drafts user-facing output
- `reviewer_agent`: checks quality/compliance and approves or requests revision

## Control Flow

1. User task enters graph state.
2. Supervisor chooses next specialist based on missing artifacts.
3. Specialist updates state (`research_notes`, `analysis_notes`, `draft`, etc.).
4. Reviewer decides `approved` vs `needs_revision`.
5. If revision requested and step budget remains, return to writer.
6. End when approved or max steps reached.

## State Contract

State keys:
- `user_task`: original request
- `langfuse_session_id`: groups traces under a business/user session
- `langfuse_user_id`: maps traces to a user identity
- `langfuse_tags`: custom tags for filtering in Langfuse UI
- `research_notes`: collected context
- `analysis_notes`: structured reasoning
- `draft`: current response draft
- `review_feedback`: reviewer output
- `approved`: final gate
- `next_agent`: routing signal from supervisor/reviewer
- `step_count`: loop guard
- `final_answer`: returned output

## Reliability Controls

- `MAX_STEPS` hard cap prevents loops
- reviewer can request rewrite only within budget
- deterministic temperature for repeatability

## Observability with Langfuse

This project uses both callback tracing and explicit Langfuse client instrumentation.

Implemented telemetry layers:
- callback traces on each LLM call (`research`, `analysis`, `writer`, `reviewer`)
- root workflow span (`multi-agent-workflow`)
- child generation span (`workflow.final_answer`)
- custom event (`workflow.completed`)
- scores:
  - trace-level: `approved`, `steps_used`
  - session-level: `run_quality_proxy`
- optional dataset item logging from each run

Recommended metadata carried across observations:
- workflow identifier/version
- session id
- user id
- tags
- step count and approval status
