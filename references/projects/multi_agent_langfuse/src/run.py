from __future__ import annotations

import argparse
import os
from contextlib import nullcontext
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from config import load_config
from graph import build_workflow
from prompting import build_prompt_resolver

_LANGFUSE_CLIENT = None


def parse_tags(tag_string: str) -> list[str]:
    return [tag.strip() for tag in tag_string.split(",") if tag.strip()]


def generate_session_id(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{ts}-{uuid4().hex[:8]}"


def build_langfuse_callbacks(cfg) -> list:
    # Optional dependency at runtime. Script still runs without Langfuse if keys/import are unavailable.
    if not cfg.langfuse_public_key or not cfg.langfuse_secret_key:
        return []

    is_v3 = False
    try:
        # Langfuse Python SDK v3
        from langfuse.langchain import CallbackHandler  # type: ignore
        from langfuse import Langfuse  # type: ignore

        is_v3 = True
    except Exception:
        try:
            # Langfuse Python SDK v2 fallback
            from langfuse.callback import CallbackHandler  # type: ignore
        except Exception as exc:
            print(f"[WARN] Langfuse callback handler import failed: {exc}")
            return []

    try:
        global _LANGFUSE_CLIENT
        if is_v3:
            _LANGFUSE_CLIENT = Langfuse(
                public_key=cfg.langfuse_public_key,
                secret_key=cfg.langfuse_secret_key,
                host=cfg.langfuse_host,
            )

        # Keep env in sync for SDK components that read env vars.
        os.environ["LANGFUSE_PUBLIC_KEY"] = cfg.langfuse_public_key
        os.environ["LANGFUSE_SECRET_KEY"] = cfg.langfuse_secret_key
        os.environ["LANGFUSE_HOST"] = cfg.langfuse_host

        handler = CallbackHandler(public_key=cfg.langfuse_public_key) if is_v3 else CallbackHandler()
        return [handler]
    except Exception as exc:
        print(f"[WARN] Langfuse callback handler initialization failed: {exc}")
        return []


def get_langfuse_client():
    return _LANGFUSE_CLIENT


def execute_workflow(
    *,
    cfg,
    graph,
    task: str,
    session_id: str,
    user_id: str,
    tags: list[str],
    trace_name: str,
    dataset_name: str | None,
    store_dataset_item: bool,
) -> dict[str, Any]:
    client = get_langfuse_client()

    initial_state = {
        "user_task": task,
        "langfuse_session_id": session_id,
        "langfuse_user_id": user_id,
        "langfuse_tags": tags,
        "research_notes": "",
        "analysis_notes": "",
        "draft": "",
        "review_feedback": "",
        "approved": False,
        "next_agent": "research",
        "step_count": 0,
        "final_answer": "",
    }

    invoke_config = {
        "metadata": {
            "langfuse_session_id": session_id,
            "langfuse_user_id": user_id,
            "langfuse_tags": tags,
            "workflow": "multi_agent_langfuse",
            "trace_name": trace_name,
        }
    }

    root_context = nullcontext()
    if client is not None:
        try:
            root_context = client.start_as_current_span(
                name=trace_name,
                input={"task": task},
                metadata={
                    "workflow": "multi_agent_langfuse",
                    "session_id": session_id,
                    "user_id": user_id,
                    "tags": tags,
                },
                trace_context={"session_id": session_id, "user_id": user_id},
            )
        except Exception:
            # Trace context formats may vary by SDK versions.
            root_context = client.start_as_current_span(
                name=trace_name,
                input={"task": task},
                metadata={
                    "workflow": "multi_agent_langfuse",
                    "session_id": session_id,
                    "user_id": user_id,
                    "tags": tags,
                },
            )

    with root_context as root_span:
        result = graph.invoke(initial_state, config=invoke_config)
        final_answer = result.get("final_answer") or result.get("draft") or "No final answer generated."

        if client is not None:
            # Add a dedicated generation observation for final response quality demos.
            with client.start_as_current_observation(
                name="workflow.final_answer",
                as_type="generation",
                input={"task": task},
                output=final_answer,
                model=cfg.groq_model,
                metadata={"session_id": session_id, "user_id": user_id, "tags": tags},
            ):
                pass

            if hasattr(root_span, "update"):
                root_span.update(
                    output={
                        "approved": result.get("approved", False),
                        "steps": result.get("step_count", 0),
                        "review_feedback": result.get("review_feedback", ""),
                        "final_answer_preview": final_answer[:300],
                    }
                )

            try:
                client.score_current_trace(
                    name="approved",
                    value=1.0 if result.get("approved", False) else 0.0,
                    data_type="BOOLEAN",
                    comment="Reviewer decision",
                    metadata={"session_id": session_id},
                )
                client.score_current_trace(
                    name="steps_used",
                    value=float(result.get("step_count", 0)),
                    data_type="NUMERIC",
                    comment="Total loop steps",
                    metadata={"session_id": session_id},
                )
            except Exception as exc:
                print(f"[WARN] score_current_trace failed: {exc}")

            try:
                client.create_score(
                    session_id=session_id,
                    name="run_quality_proxy",
                    value=1.0 if result.get("approved", False) else 0.0,
                    data_type="BOOLEAN",
                    comment="Session-level score",
                    metadata={"user_id": user_id, "tags": tags},
                )
            except Exception as exc:
                print(f"[WARN] create_score failed: {exc}")

            try:
                client.create_event(
                    name="workflow.completed",
                    input={"task": task},
                    output={
                        "approved": result.get("approved", False),
                        "steps": result.get("step_count", 0),
                    },
                    metadata={
                        "session_id": session_id,
                        "user_id": user_id,
                        "tags": tags,
                        "workflow": "multi_agent_langfuse",
                    },
                )
            except Exception as exc:
                print(f"[WARN] create_event failed: {exc}")

            if dataset_name and store_dataset_item:
                try:
                    client.create_dataset_item(
                        dataset_name=dataset_name,
                        input={"task": task},
                        expected_output={"approved": True},
                        metadata={
                            "session_id": session_id,
                            "user_id": user_id,
                            "tags": tags,
                            "source": "multi_agent_workflow",
                        },
                    )
                except Exception as exc:
                    print(f"[WARN] create_dataset_item failed: {exc}")

    if client is not None:
        try:
            client.flush()
        except Exception as exc:
            print(f"[WARN] Langfuse flush failed: {exc}")

    return {
        "result": result,
        "final_answer": final_answer,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str, help="User task for the multi-agent workflow")
    parser.add_argument(
        "--session-id",
        type=str,
        default=None,
        help="Langfuse session id. If omitted, auto-generated when LANGFUSE_AUTO_SESSION_ID=true.",
    )
    parser.add_argument("--user-id", type=str, default=None, help="Langfuse user id for this run.")
    parser.add_argument(
        "--tags",
        type=str,
        default=None,
        help="Comma-separated Langfuse tags.",
    )
    parser.add_argument(
        "--trace-name",
        type=str,
        default=None,
        help="Top-level trace/span name.",
    )
    parser.add_argument(
        "--dataset-name",
        type=str,
        default=None,
        help="Optional dataset name for logging dataset items. Falls back to LANGFUSE_DEFAULT_DATASET_NAME.",
    )
    parser.add_argument(
        "--store-dataset-item",
        action="store_true",
        help="When set with --dataset-name, stores the run input in a Langfuse dataset.",
    )
    args = parser.parse_args()

    cfg = load_config()
    callbacks = build_langfuse_callbacks(cfg)
    prompt_resolver = build_prompt_resolver(cfg, get_langfuse_client())
    graph = build_workflow(cfg, callbacks, prompt_resolver)
    session_id = args.session_id
    if not session_id and cfg.langfuse_auto_session_id:
        session_id = generate_session_id(cfg.langfuse_session_prefix)
    if not session_id:
        session_id = "single-run"

    user_id = args.user_id or cfg.langfuse_default_user_id
    tags = parse_tags(args.tags or cfg.langfuse_default_tags)
    trace_name = args.trace_name or cfg.langfuse_default_trace_name
    dataset_name = args.dataset_name if args.dataset_name is not None else cfg.langfuse_default_dataset_name or None

    out = execute_workflow(
        cfg=cfg,
        graph=graph,
        task=args.task,
        session_id=session_id,
        user_id=user_id,
        tags=tags,
        trace_name=trace_name,
        dataset_name=dataset_name,
        store_dataset_item=args.store_dataset_item,
    )

    result = out["result"]
    final_answer = out["final_answer"]

    print("\n=== FINAL ANSWER ===\n")
    print(final_answer)
    print("\n=== REVIEW FEEDBACK ===\n")
    print(result.get("review_feedback", ""))
    print(f"\nApproved: {result.get('approved', False)}")
    print(f"Steps executed: {result.get('step_count', 0)}")
    print(f"Session ID: {session_id}")
    print(f"User ID: {user_id}")


if __name__ == "__main__":
    main()
