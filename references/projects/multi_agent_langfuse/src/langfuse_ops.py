from __future__ import annotations

import argparse

from config import load_config
from prompting import FALLBACK_PROMPTS
from run import build_langfuse_callbacks


def get_client():
    cfg = load_config()
    build_langfuse_callbacks(cfg)
    from run import get_langfuse_client

    client = get_langfuse_client()
    if client is None:
        raise RuntimeError("Langfuse client unavailable. Check LANGFUSE_PUBLIC_KEY/SECRET_KEY/HOST.")
    return client


def seed_dataset(dataset_name: str) -> None:
    client = get_client()

    try:
        client.create_dataset(
            name=dataset_name,
            description="POC dataset for multi-agent Langfuse demos",
            metadata={"source": "multi_agent_langfuse", "purpose": "poc"},
        )
        print(f"Dataset created: {dataset_name}")
    except Exception:
        print(f"Dataset may already exist: {dataset_name}")

    sample_inputs = [
        "Create a short market brief for electric vehicles in India.",
        "Summarize opportunities and risks of open-source LLM adoption.",
        "Draft a GTM note for an AI coding assistant in SMB market.",
    ]
    for i, text in enumerate(sample_inputs, start=1):
        try:
            client.create_dataset_item(
                dataset_name=dataset_name,
                input={"task": text},
                expected_output={"approved": True},
                metadata={"seed_index": i, "source": "langfuse_ops"},
            )
            print(f"Added dataset item {i}")
        except Exception as exc:
            print(f"[WARN] Failed adding dataset item {i}: {exc}")

    client.flush()
    print("Dataset seed complete.")


def create_or_update_prompt(prompt_name: str) -> None:
    cfg = load_config()
    client = get_client()
    try:
        client.create_prompt(
            name=prompt_name,
            type="chat",
            labels=["production", "latest"],
            tags=["poc", "multi-agent"],
            commit_message="POC managed prompt creation",
            prompt=[
                {
                    "role": "system",
                    "content": "You are a concise reviewer. Return DECISION and FEEDBACK in two lines.",
                },
                {"role": "user", "content": "Task: {{task}}\\n\\nDraft: {{draft}}"},
            ],
            config={"model": cfg.llm_model, "temperature": 0},
        )
        print(f"Prompt created/updated: {prompt_name}")
    except Exception as exc:
        print(f"[WARN] create_prompt failed: {exc}")
    finally:
        client.flush()


def create_default_prompts() -> None:
    cfg = load_config()
    client = get_client()
    mapping = {
        cfg.prompt_name_research: "research",
        cfg.prompt_name_analysis: "analysis",
        cfg.prompt_name_writer: "writer",
        cfg.prompt_name_reviewer: "reviewer",
    }

    for prompt_name, agent_key in mapping.items():
        if not prompt_name.strip():
            continue
        fallback = FALLBACK_PROMPTS[agent_key]
        try:
            client.create_prompt(
                name=prompt_name,
                type="chat",
                labels=["production", cfg.langfuse_prompt_label],
                tags=["poc", "multi-agent", agent_key],
                commit_message=f"Create default prompt for {agent_key}",
                prompt=fallback,
                config={"model": cfg.llm_model, "temperature": 0},
            )
            print(f"Prompt created/updated: {prompt_name} ({agent_key})")
        except Exception as exc:
            print(f"[WARN] create_prompt failed for {prompt_name}: {exc}")

    client.flush()


def show_prompt(prompt_name: str) -> None:
    client = get_client()
    prompt = client.get_prompt(name=prompt_name, label="latest", type="chat")
    print(f"Prompt: {prompt_name}")
    print(prompt)
    client.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description="Langfuse operations utility for POC demos.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("seed-dataset", help="Create dataset and add sample items.")
    s1.add_argument("--dataset-name", required=True, type=str)

    s2 = sub.add_parser("create-prompt", help="Create/update a managed prompt in Langfuse.")
    s2.add_argument("--prompt-name", required=True, type=str)

    s3 = sub.add_parser("show-prompt", help="Fetch prompt by name and label=latest.")
    s3.add_argument("--prompt-name", required=True, type=str)

    sub.add_parser(
        "create-default-prompts",
        help="Create/update all default prompts configured via PROMPT_NAME_* env vars.",
    )

    args = parser.parse_args()

    if args.cmd == "seed-dataset":
        seed_dataset(args.dataset_name)
    elif args.cmd == "create-prompt":
        create_or_update_prompt(args.prompt_name)
    elif args.cmd == "show-prompt":
        show_prompt(args.prompt_name)
    elif args.cmd == "create-default-prompts":
        create_default_prompts()


if __name__ == "__main__":
    main()
