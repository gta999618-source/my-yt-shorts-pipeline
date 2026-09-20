"""Phase 4: Assemble video. STUB for now."""
from __future__ import annotations

from pathlib import Path

from .config import OUTPUT_DIR, settings


def build_video(script_text: str, audio_path: Path) -> Path:
    """Write a placeholder marker instead of a real MP4."""
    out = OUTPUT_DIR / "short.placeholder.txt"
    out.write_text(
        f"[STUB VIDEO]\n{settings.video_width}x{settings.video_height}@{settings.video_fps}fps\n"
        f"script_len={len(script_text)} audio={audio_path.name}\n",
        encoding="utf-8",
    )
    print(f"[build_video] wrote placeholder -> {out}")
    return out
