from __future__ import annotations

from langchain_core.tools import tool


@tool
def quick_web_research(topic: str) -> str:
    """Mock research tool. Replace with real search API in production."""
    return (
        f"Research summary for '{topic}': market direction is mixed, "
        "adoption is rising in multiple regions, and regulation is evolving."
    )


@tool
def risk_scan(topic: str) -> str:
    """Mock risk scan tool. Replace with domain-specific risk service."""
    return (
        f"Risk scan for '{topic}': policy volatility, supply-chain pressure, "
        "and margin compression are common watch points."
    )
