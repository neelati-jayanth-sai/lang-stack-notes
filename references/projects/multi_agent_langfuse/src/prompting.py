from __future__ import annotations

from typing import Any, Callable, TypedDict

from config import AppConfig


class ResolvedPrompt(TypedDict):
    messages: list[tuple[str, str]]
    prompt_name: str
    prompt_label: str
    source: str


FALLBACK_PROMPTS: dict[str, list[dict[str, str]]] = {
    "research": [
        {
            "role": "system",
            "content": "You are a research specialist. Produce concise factual notes from provided material.",
        },
        {
            "role": "user",
            "content": "Task: {{task}}\n\nSource notes:\n{{source_notes}}",
        },
    ],
    "analysis": [
        {
            "role": "system",
            "content": "You are an analyst. Convert research into implications, risks, and opportunities.",
        },
        {
            "role": "user",
            "content": "Task: {{task}}\n\nResearch:\n{{research_notes}}\n\nRisk Scan:\n{{risk_notes}}",
        },
    ],
    "writer": [
        {
            "role": "system",
            "content": "You are a technical writer. Produce clear and structured output.",
        },
        {
            "role": "user",
            "content": "Write a concise final response for this task.\n\nTask: {{task}}\n\nResearch Notes:\n{{research_notes}}\n\nAnalysis Notes:\n{{analysis_notes}}",
        },
    ],
    "reviewer": [
        {
            "role": "system",
            "content": "You are a strict reviewer. Approve only if response is clear, grounded, and actionable. Return two lines: DECISION: <approve|revise> and FEEDBACK: <text>.",
        },
        {
            "role": "user",
            "content": "Task:\n{{task}}\n\nDraft:\n{{draft}}",
        },
    ],
}


def _resolve_prompt_name(cfg: AppConfig, agent_key: str) -> str:
    mapping = {
        "research": cfg.prompt_name_research,
        "analysis": cfg.prompt_name_analysis,
        "writer": cfg.prompt_name_writer,
        "reviewer": cfg.prompt_name_reviewer,
    }
    return mapping.get(agent_key, "").strip()


def _compile_fallback(fallback: list[dict[str, str]], variables: dict[str, Any]) -> list[tuple[str, str]]:
    messages: list[tuple[str, str]] = []
    for msg in fallback:
        content = msg["content"]
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
        messages.append((msg["role"], content))
    return messages


def build_prompt_resolver(cfg: AppConfig, client: Any) -> Callable[[str, dict[str, Any]], ResolvedPrompt]:
    def resolve(agent_key: str, variables: dict[str, Any]) -> ResolvedPrompt:
        fallback = FALLBACK_PROMPTS[agent_key]
        prompt_name = _resolve_prompt_name(cfg, agent_key) or f"fallback-{agent_key}"
        label = cfg.langfuse_prompt_label

        if cfg.langfuse_use_managed_prompts and client is not None and not prompt_name.startswith("fallback-"):
            try:
                prompt = client.get_prompt(
                    name=prompt_name,
                    label=label,
                    type="chat",
                    fallback=fallback,
                )
                messages = prompt.get_langchain_prompt(**variables)
                return {
                    "messages": messages,
                    "prompt_name": prompt_name,
                    "prompt_label": label,
                    "source": "langfuse",
                }
            except Exception:
                pass

        return {
            "messages": _compile_fallback(fallback, variables),
            "prompt_name": prompt_name,
            "prompt_label": label,
            "source": "fallback",
        }

    return resolve
