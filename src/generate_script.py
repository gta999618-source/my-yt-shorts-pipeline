"""
generate_script.py — real Gemini-powered script generation.

Phase 3: replaces the Phase 2 stub. Returns a Script object that
matches the Phase 2 shape so nothing downstream needs to change.
"""

from __future__ import annotations

import json

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from src.config import get_settings


class _StructuredScript(BaseModel):
    """Internal schema — the shape we force Gemini to return."""

    title: str = Field(
        description="Catchy YouTube Shorts title, max 90 characters, no clickbait lies.",
    )
    hook: str = Field(
        description="First 3-8 words. Must grab attention immediately.",
    )
    body: str = Field(
        description=(
            "The spoken script, 45-55 words. Fits 25-30 seconds aloud. "
            "No emojis, no stage directions, no markdown, no 'hey guys'."
        ),
    )
    cta: str = Field(
        description="Short closing line, 5-10 words. Question or call to action.",
    )
    description: str = Field(
        description="YouTube description with a hook, 2-3 sentences, plus 3 hashtags.",
    )
    tags: list[str] = Field(
        description="5-8 YouTube tags, lowercase, no # symbol.",
    )


class Script:
    """Public Script type — same interface as the Phase 2 stub."""

    def __init__(
        self,
        topic: str,
        hook: str,
        body: str,
        cta: str,
        title: str = "",
        description: str = "",
        tags: list[str] | None = None,
    ) -> None:
        self.topic = topic
        self.hook = hook
        self.body = body
        self.cta = cta
        self.title = title or hook[:90]
        self.description = description
        self.tags = tags or []

    def as_plain_text(self) -> str:
        return f"{self.hook}\n\n{self.body}\n\n{self.cta}"


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise SystemExit("GEMINI_API_KEY missing.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_script(topic: str) -> Script:
    """Call Gemini and return a validated Script."""
    settings = get_settings()
    model = settings.script_model
    print(f"[generate_script] topic={topic!r} model={model}")

    prompt = f"""You are writing a YouTube Shorts script about: {topic}.

Rules:
- The spoken body MUST be 45-55 words. Count carefully.
- Short sentences. Punchy. No filler.
- Hook the viewer in the first 3 words.
- End with a question or call to action.
- No emojis, no "hey guys", no channel plugs.
- Title must be under 90 characters."""

    response = _client().models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=_StructuredScript.model_json_schema(),
            temperature=0.9,
        ),
    )

    data = json.loads(response.text)
    structured = _StructuredScript.model_validate(data)

    # Enforce word count — Gemini sometimes overshoots.
    words = structured.body.split()
    if len(words) > 60:
        print(f"[generate_script] word count {len(words)} too high, truncating.")
        structured.body = " ".join(words[:55])

    script = Script(
        topic=topic,
        hook=structured.hook,
        body=structured.body,
        cta=structured.cta,
        title=structured.title,
        description=structured.description,
        tags=structured.tags,
    )
    print(f"[generate_script] OK title={script.title!r} words={len(script.body.split())}")
    return script
