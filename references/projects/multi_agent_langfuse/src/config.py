from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class AppConfig:
    llm_model: str
    llm_api_key: str
    llm_endpoint_url: str
    max_steps: int
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_host: str
    langfuse_auto_session_id: bool
    langfuse_session_prefix: str
    langfuse_default_user_id: str
    langfuse_user_prefix: str
    langfuse_default_tags: str
    langfuse_default_trace_name: str
    langfuse_default_dataset_name: str
    langfuse_use_managed_prompts: bool
    langfuse_prompt_label: str
    prompt_name_research: str
    prompt_name_analysis: str
    prompt_name_writer: str
    prompt_name_reviewer: str


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_config() -> AppConfig:
    load_dotenv()

    return AppConfig(
        llm_model=os.getenv("LLM_MODEL", os.getenv("OPENAI_MODEL", os.getenv("GROQ_MODEL", "gpt-4o-mini"))),
        llm_api_key=os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", os.getenv("GROQ_API_KEY", ""))),
        llm_endpoint_url=os.getenv("LLM_ENDPOINT_URL", os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")),
        max_steps=int(os.getenv("MAX_STEPS", "12")),
        langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
        langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
        langfuse_host=os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
        langfuse_auto_session_id=_as_bool(os.getenv("LANGFUSE_AUTO_SESSION_ID"), True),
        langfuse_session_prefix=os.getenv("LANGFUSE_SESSION_PREFIX", "poc-session"),
        langfuse_default_user_id=os.getenv("LANGFUSE_DEFAULT_USER_ID", "local-user"),
        langfuse_user_prefix=os.getenv("LANGFUSE_USER_PREFIX", "demo-user"),
        langfuse_default_tags=os.getenv("LANGFUSE_DEFAULT_TAGS", "poc,multi-agent,langgraph,langfuse"),
        langfuse_default_trace_name=os.getenv("LANGFUSE_DEFAULT_TRACE_NAME", "multi-agent-workflow"),
        langfuse_default_dataset_name=os.getenv("LANGFUSE_DEFAULT_DATASET_NAME", ""),
        langfuse_use_managed_prompts=_as_bool(os.getenv("LANGFUSE_USE_MANAGED_PROMPTS"), True),
        langfuse_prompt_label=os.getenv("LANGFUSE_PROMPT_LABEL", "latest"),
        prompt_name_research=os.getenv("PROMPT_NAME_RESEARCH", "poc-research-prompt"),
        prompt_name_analysis=os.getenv("PROMPT_NAME_ANALYSIS", "poc-analysis-prompt"),
        prompt_name_writer=os.getenv("PROMPT_NAME_WRITER", "poc-writer-prompt"),
        prompt_name_reviewer=os.getenv("PROMPT_NAME_REVIEWER", "poc-reviewer-prompt"),
    )
