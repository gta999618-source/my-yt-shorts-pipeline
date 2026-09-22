"""
generate_audio.py — convert script text into a voiceover audio file.
Phase 2: STUB. Phase 3 swaps in edge-tts.
"""

from __future__ import annotations

from pathlib import Path


def synthesize(text: str, out_path: Path) -> Path:
    """Write spoken text to out_path. STUB implementation."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        f"[STUB AUDIO PLACEHOLDER]\n\nWould speak:\n{text}\n",
        encoding="utf-8",
    )
    return out_path
