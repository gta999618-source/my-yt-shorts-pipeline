"""
generate_script.py — turn a topic into a short-form video script.
Phase 2: STUB. Phase 3 swaps in a real LLM call.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Script:
    topic: str
    hook: str
    body: str
    cta: str

    def as_plain_text(self) -> str:
        return f"{self.hook}\n\n{self.body}\n\n{self.cta}"


def generate_script(topic: str) -> Script:
    """Return a Script for the given topic. STUB implementation."""
    return Script(
        topic=topic,
        hook=f"[STUB HOOK] Did you know this about {topic}?",
        body=(
            f"[STUB BODY] Here are three quick facts about {topic}. "
            "One. Two. Three. That's it — short and punchy."
        ),
        cta="[STUB CTA] Follow for more.",
    )
