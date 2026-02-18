# 12 - Reference Architectures

## Architecture A: RAG Assistant

Flow:
- classify intent
- retrieval subgraph
- answer generation
- groundedness check
- optional human escalation

## Architecture B: Tool-Heavy Ops Agent

Flow:
- plan
- execute tool node(s)
- validate tool outputs
- retry or fallback
- finalize response

## Architecture C: Multi-Agent Supervisor

Flow:
- supervisor routes to specialist
- specialists write intermediate artifacts
- reviewer/arbiter resolves conflicts
- final synthesis

## Selection Rule

Choose the simplest architecture that meets reliability and latency requirements.
