"""The squad roster.

To add a new character: create `config/personas/<name>.py` that defines a
`Character(...)`, import it here and append it to `CHARACTERS`. Nothing else
needs to change: the prompts, @mentions, mute toggles and accent colors in the
UI are all driven from this list.
"""

from __future__ import annotations

from config.character import Character
from config.personas.armin import ARMIN
from config.personas.eren import EREN
from config.personas.levi import LEVI

CHARACTERS: list[Character] = [EREN, LEVI, ARMIN]

CHARACTER_MAP: dict[str, Character] = {c.id: c for c in CHARACTERS}


def get_character(character_id: str) -> Character | None:
    return CHARACTER_MAP.get(character_id.lower())


def public_roster() -> list[dict]:
    return [c.public() for c in CHARACTERS]
