# Langfuse Setup (Local Self-Hosted)

## Goal

Run Langfuse locally and send traces from this project to your local instance.

## Preferred Option (Included in this repo)

Use the deployment bundle included here:

```powershell
cd references\projects\multi_agent_langfuse\deploy\langfuse
Copy-Item .env.example .env
docker compose up -d
```

Open `http://localhost:3000`.

## Configure This Project

Set environment values in workspace `.env`:

```env
LANGFUSE_PUBLIC_KEY=your_local_public_key
LANGFUSE_SECRET_KEY=your_local_secret_key
LANGFUSE_HOST=http://localhost:3000
```

## Integration Pattern

This project passes Langfuse callback handlers via model config:

```python
callbacks = [langfuse_handler]
llm.invoke(messages, config={"callbacks": callbacks, "metadata": {...}})
```

## Validation

1. Run the app once.
2. Open `http://localhost:3000`.
3. Verify traces include agent metadata and inputs/outputs.
4. Verify sessions and scores appear after batch runs.

### Quick Validation Commands

```powershell
python references\projects\multi_agent_langfuse\src\run.py "Smoke test workflow" --session-id smoke-session-1 --user-id smoke-user-1 --tags "smoke,poc"
python references\projects\multi_agent_langfuse\src\multi_run.py --runs 5 --session-prefix val-session --user-prefix val-user --tags "batch,validation"
python references\projects\multi_agent_langfuse\src\langfuse_ops.py create-prompt --prompt-name poc-reviewer-prompt
python references\projects\multi_agent_langfuse\src\langfuse_ops.py seed-dataset --dataset-name poc-multi-agent-dataset
```

In Langfuse UI, check:
- Traces tab: multiple traces with tags/metadata
- Sessions tab: grouped runs via `session_id`
- Scores tab (or trace detail): `approved`, `steps_used`, `run_quality_proxy`
- Prompts tab: `poc-reviewer-prompt`
- Datasets tab: `poc-multi-agent-dataset`

## Troubleshooting

- No traces: verify containers are healthy and env vars are loaded.
- Auth errors: regenerate local API keys in Langfuse UI.
- Connection errors: confirm `LANGFUSE_HOST=http://localhost:3000`.
- `fillFromDate` dashboard errors: run `docker compose down -v && docker compose pull && docker compose up -d` in `deploy/langfuse`, then hard-refresh browser.

## Official Reference

- https://langfuse.com/self-hosting
- https://langfuse.com/self-hosting/deployment/docker-compose
