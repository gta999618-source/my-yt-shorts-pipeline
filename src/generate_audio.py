"""
generate_audio.py — real TTS using edge-tts (free, no API key).

Phase 3: replaces the Phase 2 stub. Same function name, same
signature — now it actually produces an MP3.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts

from src.config import get_settings


async def _synth_async(text: str, out_path: Path, voice: str) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out_path))


def synthesize(text: str, out_path: Path) -> Path:
    """Convert text to MP3. Returns the path to the audio file."""
    settings = get_settings()
    voice = settings.tts_voice

    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[generate_audio] voice={voice} chars={len(text)}")
    asyncio.run(_synth_async(text, out_path, voice))

    if not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(f"edge-tts produced no audio at {out_path}")

    kb = out_path.stat().st_size / 1024
    print(f"[generate_audio] OK wrote {out_path} ({kb:.1f} KB)")
    return out_path
