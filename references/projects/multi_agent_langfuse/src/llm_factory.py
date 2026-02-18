from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq

from config import AppConfig



def build_llm(cfg: AppConfig) -> BaseChatModel:
    return ChatGroq(model=cfg.groq_model, temperature=0)
