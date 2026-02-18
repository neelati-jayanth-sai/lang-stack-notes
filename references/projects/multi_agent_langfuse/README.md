# Multi-Agent LangGraph + Langfuse Reference Project (Python 3.12)

This is a detailed reference project showing how to build and trace a **multi-agent workflow** with:
- LangChain components
- LangGraph orchestration
- Langfuse observability/tracing
- Groq-hosted chat models

## Langfuse Features Used In This POC

- trace/session/user grouping via `session_id` + `user_id`
- tags and structured metadata on every run
- LLM callback traces from LangChain
- custom root span (`workflow`) and child generation (`final_answer`)
- custom events (`workflow.completed`)
- scores:
  - trace-level scores (`approved`, `steps_used`)
  - session-level score (`run_quality_proxy`)
- dataset operations:
  - create dataset
  - create dataset items from runs
- prompt operations:
  - create/update managed prompts
  - fetch prompt by label

## What You Will Learn

- Designing a supervisor-driven multi-agent architecture
- Building specialist agents (research, analyst, writer, reviewer)
- Passing structured state across nodes
- Guarding workflow with retry/step limits
- Adding end-to-end traces with Langfuse callback handlers

## Project Layout

- `docs/ARCHITECTURE.md`: system design and flow
- `docs/LANGFUSE_SETUP.md`: local Langfuse setup and troubleshooting
- `deploy/langfuse/docker-compose.yml`: local self-hosted Langfuse stack
- `deploy/langfuse/.env.example`: stack env template
- `deploy/langfuse/README.md`: deployment commands
- `src/config.py`: environment/config handling
- `src/state.py`: shared graph state schema
- `src/agents/`: agent node implementations
- `src/graph.py`: compiled LangGraph workflow
- `src/run.py`: CLI entrypoint
- `src/multi_run.py`: batch simulation runner for generating multiple traces
- `src/langfuse_ops.py`: utility for prompt and dataset operations
- `examples/run_demo.ps1`: example execution script
- `examples/run_multiple.ps1`: batch run helper
- `examples/langfuse_feature_demo.ps1`: end-to-end Langfuse feature demo

## Python Version

Use **Python 3.12**.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r references\projects\multi_agent_langfuse\requirements.txt
Copy-Item references\projects\multi_agent_langfuse\.env.example .env
```

## Run Langfuse Locally

```powershell
cd references\projects\multi_agent_langfuse\deploy\langfuse
Copy-Item .env.example .env
docker compose up -d
```

Open `http://localhost:3000`, create a project, and generate API keys.

Then fill workspace `.env`:

```env
GROQ_API_KEY=...
GROQ_MODEL=llama-3.1-8b-instant
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_AUTO_SESSION_ID=true
LANGFUSE_SESSION_PREFIX=poc-session
LANGFUSE_DEFAULT_USER_ID=local-user
LANGFUSE_USER_PREFIX=demo-user
LANGFUSE_DEFAULT_TAGS=poc,multi-agent,langgraph,langfuse
LANGFUSE_DEFAULT_TRACE_NAME=multi-agent-workflow
LANGFUSE_DEFAULT_DATASET_NAME=
LANGFUSE_USE_MANAGED_PROMPTS=true
LANGFUSE_PROMPT_LABEL=latest
PROMPT_NAME_RESEARCH=poc-research-prompt
PROMPT_NAME_ANALYSIS=poc-analysis-prompt
PROMPT_NAME_WRITER=poc-writer-prompt
PROMPT_NAME_REVIEWER=poc-reviewer-prompt
```

### Detailed Env Explanation

- `LANGFUSE_HOST`: local Langfuse base URL.
- `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`: project API keys from local Langfuse UI.
- `LANGFUSE_AUTO_SESSION_ID`: when `true`, `run.py` auto-creates session IDs if you do not pass `--session-id`.
- `LANGFUSE_SESSION_PREFIX`: prefix for generated session IDs, example `poc-session-20260218093010-ab12cd34`.
- `LANGFUSE_DEFAULT_USER_ID`: default user id for single runs when `--user-id` is omitted.
- `LANGFUSE_USER_PREFIX`: prefix for generated users in batch runs (`multi_run.py`).
- `LANGFUSE_DEFAULT_TAGS`: default tags attached to traces, sessions, events, and scores.
- `LANGFUSE_DEFAULT_TRACE_NAME`: default top-level trace/span name.
- `LANGFUSE_DEFAULT_DATASET_NAME`: optional dataset name used when `--dataset-name` is omitted.
- `LANGFUSE_USE_MANAGED_PROMPTS`: when `true`, agent prompts are fetched from Langfuse by name.
- `LANGFUSE_PROMPT_LABEL`: prompt label to fetch (usually `latest` or `production`).
- `PROMPT_NAME_RESEARCH`, `PROMPT_NAME_ANALYSIS`, `PROMPT_NAME_WRITER`, `PROMPT_NAME_REVIEWER`:
  dynamic prompt names for each agent. Change these in `.env` without code changes.

### Dynamic Prompt Names (How It Works)

1. Each agent resolves its prompt name from `.env` (`PROMPT_NAME_*`).
2. The workflow fetches that prompt from Langfuse using `LANGFUSE_PROMPT_LABEL`.
3. If a prompt is missing/unavailable, the app falls back to built-in local prompt templates.
4. Trace metadata includes:
   - `prompt_name`
   - `prompt_label`
   - `prompt_source` (`langfuse` or `fallback`)

This gives a strong POC story: prompt changes can be done in Langfuse UI and activated by env/config without code edits.

## Run Workflow

```powershell
python references\projects\multi_agent_langfuse\src\run.py "Create a short market brief for electric vehicles"
```

With explicit session/user/tags:

```powershell
python references\projects\multi_agent_langfuse\src\run.py "Create a short market brief for electric vehicles" --session-id demo-session-1 --user-id demo-user-1 --tags "poc,langfuse,multi-agent"
```

Auto session id (recommended):

```powershell
python references\projects\multi_agent_langfuse\src\run.py "Create a short market brief for electric vehicles"
```

When `LANGFUSE_AUTO_SESSION_ID=true`, this creates a session id automatically and prints it in terminal output.

## Simulate Multiple Runs (for Langfuse UI)

```powershell
python references\projects\multi_agent_langfuse\src\multi_run.py --runs 10 --sleep-seconds 0.2
```

Optional custom tasks:

```powershell
python references\projects\multi_agent_langfuse\src\multi_run.py --runs 6 --task "Analyze AI copilots in fintech" --task "Draft GTM for coding assistant in SMB market" --session-prefix poc-session --user-prefix poc-user --tags "batch,poc,langfuse"
```

Log batch runs to a dataset:

```powershell
python references\projects\multi_agent_langfuse\src\multi_run.py --runs 6 --dataset-name poc-multi-agent-dataset --store-dataset-item
```

## Prompt + Dataset Operations

Create/update a managed prompt in Langfuse:

```powershell
python references\projects\multi_agent_langfuse\src\langfuse_ops.py create-prompt --prompt-name poc-reviewer-prompt
```

Create/update all default agent prompts from env (`PROMPT_NAME_*`):

```powershell
python references\projects\multi_agent_langfuse\src\langfuse_ops.py create-default-prompts
```

Create a dataset and seed items:

```powershell
python references\projects\multi_agent_langfuse\src\langfuse_ops.py seed-dataset --dataset-name poc-multi-agent-dataset
```

Fetch a prompt by `label=latest`:

```powershell
python references\projects\multi_agent_langfuse\src\langfuse_ops.py show-prompt --prompt-name poc-reviewer-prompt
```

Run a full feature demo:

```powershell
powershell -ExecutionPolicy Bypass -File references\projects\multi_agent_langfuse\examples\langfuse_feature_demo.ps1
```

## Notes

- This project is local-first for Langfuse and does not require Langfuse Cloud.
- LLM inference is through Groq via `langchain-groq`.
- For production, replace mock tools and add persistent workflow checkpointing.
