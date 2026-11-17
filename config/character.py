"""The `Character` record every persona is built from."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Character:
    id: str                     # lowercase key, also the @mention handle
    name: str                   # display name
    accent: str                 # hex accent color used by the UI
    initials: str               # shown in the avatar circle
    tagline: str                # one-liner under the name in the roster
    persona: str                # who they are and how they text
    aliases: tuple[str, ...] = field(default_factory=tuple)  # extra @handles

    def public(self) -> dict:
        """The fields the frontend is allowed to see (no prompts)."""
        return {
            "id": self.id,
            "name": self.name,
            "accent": self.accent,
            "initials": self.initials,
            "tagline": self.tagline,
        }
