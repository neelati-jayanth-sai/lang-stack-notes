from __future__ import annotations

import argparse
import time
from pathlib import Path

from config import load_config
from graph import build_workflow
from prompting import build_prompt_resolver
from run import build_langfuse_callbacks, execute_workflow, generate_session_id, get_langfuse_client, parse_tags


DEFAULT_TASKS = [
    "Create a short market brief for electric vehicles in India.",
    "Summarize risks and opportunities of open-source LLM adoption for startups.",
    "Write a one-page strategy note for AI copilots in enterprise support teams.",
    "Create a concise competitor analysis for code generation assistants.",
    "Draft a decision memo: build vs buy for an internal AI knowledge assistant.",
]


def load_tasks(tasks_file: str | None, inline_tasks: list[str]) -> list[str]:
    if inline_tasks:
        return [t.strip() for t in inline_tasks if t.strip()]

    if tasks_file:
        lines = Path(tasks_file).read_text(encoding="utf-8").splitlines()
        tasks = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        if tasks:
            return tasks

    return DEFAULT_TASKS


def main() -> None:
    parser = argparse.ArgumentParser(description="Run multiple workflow simulations for Langfuse tracing.")
    parser.add_argument("--runs", type=int, default=5, help="Number of total runs.")
    parser.add_argument(
        "--task",
        action="append",
        default=[],
        help="Task to run. Repeat flag to pass multiple tasks.",
    )
    parser.add_argument("--tasks-file", type=str, default=None, help="Path to newline-delimited tasks file.")
    parser.add_argument("--sleep-seconds", type=float, default=0.5, help="Delay between runs.")
    parser.add_argument("--user-prefix", type=str, default=None, help="Prefix for generated user ids.")
    parser.add_argument("--session-prefix", type=str, default=None, help="Prefix for session ids.")
    parser.add_argument(
        "--tags",
        type=str,
        default=None,
        help="Comma-separated tags to attach to each run.",
    )
    parser.add_argument(
        "--dataset-name",
        type=str,
        default=None,
        help="Optional dataset name for logging inputs during batch runs.",
    )
    parser.add_argument(
        "--store-dataset-item",
        action="store_true",
        help="When set with --dataset-name, stores each run input into Langfuse dataset.",
    )
    args = parser.parse_args()

    if args.runs < 1:
        raise ValueError("--runs must be >= 1")

    cfg = load_config()
    callbacks = build_langfuse_callbacks(cfg)
    prompt_resolver = build_prompt_resolver(cfg, get_langfuse_client())
    graph = build_workflow(cfg, callbacks, prompt_resolver)
    tasks = load_tasks(args.tasks_file, args.task)
    tags = parse_tags(args.tags or cfg.langfuse_default_tags)
    session_prefix = args.session_prefix or cfg.langfuse_session_prefix
    user_prefix = args.user_prefix or cfg.langfuse_user_prefix
    dataset_name = args.dataset_name if args.dataset_name is not None else cfg.langfuse_default_dataset_name or None

    print(f"Loaded {len(tasks)} task(s). Executing {args.runs} run(s).")
    print("Langfuse host:", cfg.langfuse_host)

    for i in range(args.runs):
        task = tasks[i % len(tasks)]
        run_label = f"run-{i + 1:03d}"
        session_id = generate_session_id(session_prefix)
        user_id = f"{user_prefix}-{(i % 5) + 1:02d}"
        task_for_run = f"{task} [run={run_label}]"

        print(f"\n=== {run_label} ===")
        print("Task:", task_for_run)
        print("Session:", session_id)
        print("User:", user_id)

        out = execute_workflow(
            cfg=cfg,
            graph=graph,
            task=task_for_run,
            session_id=session_id,
            user_id=user_id,
            tags=tags,
            trace_name="multi-agent-batch-run",
            dataset_name=dataset_name,
            store_dataset_item=args.store_dataset_item,
        )
        result = out["result"]
        final_answer = out["final_answer"]

        print("Approved:", result.get("approved", False))
        print("Steps:", result.get("step_count", 0))
        print("Final (first 200 chars):", final_answer[:200].replace("\n", " "))

        if args.sleep_seconds > 0 and i < args.runs - 1:
            time.sleep(args.sleep_seconds)

    print("\nBatch simulation complete. Check Langfuse UI for new traces.")


if __name__ == "__main__":
    main()
