"""
generate_audio.py — TTS with caption generation using edge-tts.

Phase 4: now produces BOTH an MP3 and an SRT subtitle file.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts
from edge_tts import SubMaker

from src.config import get_settings


async def _synth_with_subs(
    text: str,
    audio_path: Path,
    srt_path: Path,
    voice: str,
) -> None:
    """Synthesize audio AND capture word boundaries for subtitles."""
    communicate = edge_tts.Communicate(text, voice)
    submaker = SubMaker()

    with open(audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())


def synthesize(
    text: str,
    out_path: Path,
    srt_path: Path | None = None,
) -> Path:
    """Convert text to MP3 + SRT. Returns the audio path."""
    settings = get_settings()
    voice = settings.tts_voice

    out_path.parent.mkdir(parents=True, exist_ok=True)
    srt = srt_path or out_path.with_suffix(".srt")

    print(f"[generate_audio] voice={voice} chars={len(text)}")
    asyncio.run(_synth_with_subs(text, out_path, srt, voice))

    if not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(f"edge-tts produced no audio at {out_path}")

    kb = out_path.stat().st_size / 1024
    cues = srt.read_text(encoding="utf-8").count("-->") if srt.exists() else 0
    print(f"[generate_audio] OK audio={kb:.1f} KB, {cues} caption cues")
    return out_path
