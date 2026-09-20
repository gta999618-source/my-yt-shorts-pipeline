"""Phase 3: Text-to-speech. STUB for now."""
from __future__ import annotations

from pathlib import Path

from .config import OUTPUT_DIR


def generate_audio(text: str, out_path: Path | None = None) -> Path:
    """Write a placeholder .txt marker instead of real audio."""
    out = out_path or (OUTPUT_DIR / "voiceover.placeholder.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"[STUB AUDIO]\n{text}\n", encoding="utf-8")
    print(f"[generate_audio] wrote placeholder -> {out}")
    return out
