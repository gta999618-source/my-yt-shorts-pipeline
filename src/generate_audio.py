"""
generate_audio.py — TTS with caption generation using edge-tts.

Phase 4: produces BOTH an MP3 and an SRT subtitle file.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts

from src.config import get_settings


async def _synth_with_subs(
    text: str,
    audio_path: Path,
    srt_path: Path,
    voice: str,
) -> None:
    """Synthesize audio AND capture word boundaries for subtitles."""
    communicate = edge_tts.Communicate(text, voice)
    submaker = edge_tts.SubMaker()

    with open(audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # edge-tts 7.x requires all four positional arguments
                submaker.feed(
                    chunk["offset"],
                    chunk["duration"],
                    chunk["text"],
                )

    # Write SRT file
    srt_content = submaker.get_srt()
    if not srt_content.strip():
        # Fallback: build one big SRT from the full text
        print("[generate_audio] WARNING: no word boundaries, using fallback SRT")
        srt_content = _fallback_srt(text)

    srt_path.write_text(srt_content, encoding="utf-8")


def _fallback_srt(text: str) -> str:
    """If SubMaker is empty, split text into chunks with rough timing."""
    words = text.split()
    # Roughly 3 words per second
    chunk_size = 8
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    lines = []
    t = 0.0
    for i, chunk in enumerate(chunks, start=1):
        end = t + (len(chunk.split()) / 3.0)
        lines.append(f"{i}\n{_fmt(t)} --> {_fmt(end)}\n{chunk}\n")
        t = end
    return "\n".join(lines)


def _fmt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


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
