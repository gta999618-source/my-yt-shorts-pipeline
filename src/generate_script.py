"""Phase 3: Generate the Short's script. STUB for now."""
from __future__ import annotations

from dataclasses import dataclass

from .config import settings


@dataclass
class Script:
    title: str
    body: str
    tags: list[str]


def generate_script(topic: str = "Why the sky is blue") -> Script:
    """Return a placeholder script. Real LLM call lands in Phase 3."""
    print(f"[generate_script] topic={topic!r} model={settings.script_model}")
    return Script(
        title=f"Placeholder: {topic}",
        body="This is a stub script. Real generation comes in Phase 3.",
        tags=["shorts", "placeholder"],
    )
