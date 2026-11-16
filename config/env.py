"""Small helpers for reading configuration from the environment.

Importing this module loads `.env` once, so everything that reads settings
afterwards sees the same values. Each helper falls back to a default instead
of crashing when a value is missing or not a valid number.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from config.paths import BASE_DIR, ENV_FILE

load_dotenv(ENV_FILE)


def env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    return value.strip() if value is not None else default


def env_int(name: str, default: int) -> int:
    try:
        return int(env_str(name, str(default)))
    except ValueError:
        return default


def env_float(name: str, default: float) -> float:
    try:
        return float(env_str(name, str(default)))
    except ValueError:
        return default


def resolve_path(raw: str) -> Path:
    """Relative paths are anchored to the project folder, not the cwd."""
    path = Path(raw)
    return path if path.is_absolute() else BASE_DIR / path
