from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from config import AppConfig



def build_llm(cfg: AppConfig) -> BaseChatModel:
    return ChatOpenAI(
        model=cfg.llm_model,
        api_key=cfg.llm_api_key or None,
        base_url=cfg.llm_endpoint_url,
        temperature=0,
    )
