"""
build_video.py — combine audio + visuals into a finished video file.
Phase 2: STUB. Phase 4 swaps in moviepy/ffmpeg.
"""

from __future__ import annotations

from pathlib import Path


def build_video(
    audio_path: Path,
    script_text: str,
    out_path: Path,
) -> Path:
    """Build the final video. STUB implementation."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "[STUB VIDEO PLACEHOLDER]\n\n"
        f"audio source: {audio_path}\n"
        f"script length: {len(script_text)} chars\n",
        encoding="utf-8",
    )
    return out_path
