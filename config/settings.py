"""Central configuration for The Squad Room.

Everything is read once from the environment (via `.env`) and exposed as the
immutable `settings` object. Which AI provider is used (Gemini or Claude) is
decided here, so the rest of the app never has to care.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config.env import env_float, env_int, env_str, resolve_path
from config.paths import BASE_DIR, STATIC_DIR  # noqa: F401  (re-exported)

PROVIDERS = ("gemini", "anthropic")
_PLACEHOLDER_KEYS = {"", "your-api-key-here"}


@dataclass(frozen=True)
class Settings:
    llm_provider: str            # "gemini" or "anthropic"

    gemini_api_key: str
    gemini_chat_model: str
    gemini_lore_model: str
    gemini_thinking_level: str

    anthropic_api_key: str
    anthropic_chat_model: str
    anthropic_lore_model: str
    anthropic_effort: str

    user_name: str
    history_limit: int
    lore_inject_count: int
    typing_delay_min: float
    typing_delay_max: float
    db_path: Path

    # ---- values for whichever provider is active ----

    @property
    def provider_label(self) -> str:
        return "Gemini" if self.llm_provider == "gemini" else "Claude"

    @property
    def api_key_name(self) -> str:
        return "GEMINI_API_KEY" if self.llm_provider == "gemini" else "ANTHROPIC_API_KEY"

    @property
    def api_key(self) -> str:
        return self.gemini_api_key if self.llm_provider == "gemini" else self.anthropic_api_key

    @property
    def has_api_key(self) -> bool:
        return self.api_key not in _PLACEHOLDER_KEYS

    @property
    def chat_model(self) -> str:
        return self.gemini_chat_model if self.llm_provider == "gemini" else self.anthropic_chat_model

    @property
    def lore_model(self) -> str:
        return self.gemini_lore_model if self.llm_provider == "gemini" else self.anthropic_lore_model

    @property
    def missing_key_message(self) -> str:
        return (
            f"No API key found. Copy .env.example to .env, add {self.api_key_name}, "
            "and restart the server."
        )


def _load() -> Settings:
    provider = env_str("LLM_PROVIDER", "gemini").lower()
    if provider not in PROVIDERS:
        provider = "gemini"

    delay_min = max(0.0, env_float("TYPING_DELAY_MIN", 1.0))
    delay_max = max(delay_min, env_float("TYPING_DELAY_MAX", 2.0))

    return Settings(
        llm_provider=provider,
        gemini_api_key=env_str("GEMINI_API_KEY", ""),
        gemini_chat_model=env_str("GEMINI_CHAT_MODEL", "") or "gemini-4-hydrogen",
        gemini_lore_model=env_str("GEMINI_LORE_MODEL", "") or "gemini-3.5-flash-lite",
        gemini_thinking_level=env_str("GEMINI_THINKING_LEVEL", "low").lower(),
        anthropic_api_key=env_str("ANTHROPIC_API_KEY", ""),
        anthropic_chat_model=env_str("ANTHROPIC_CHAT_MODEL", "") or "claude-haiku-5-5",
        anthropic_lore_model=env_str("ANTHROPIC_LORE_MODEL", "") or "claude-haiku-5-5",
        anthropic_effort=env_str("ANTHROPIC_EFFORT", "low").lower(),
        user_name=env_str("USER_NAME", "You") or "You",
        history_limit=max(4, env_int("HISTORY_LIMIT", 40)),
        lore_inject_count=max(0, env_int("LORE_INJECT_COUNT", 3)),
        typing_delay_min=delay_min,
        typing_delay_max=delay_max,
        db_path=resolve_path(env_str("DATABASE_PATH", "data/squad_room.db")),
    )


settings = _load()
