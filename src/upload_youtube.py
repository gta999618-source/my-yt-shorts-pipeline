"""Phase 5: Upload to YouTube. STUB for now."""
from __future__ import annotations

from pathlib import Path

from .config import settings


def upload_video(video_path: Path, title: str, description: str, tags: list[str]) -> str:
    """Pretend to upload; return a fake video ID."""
    has_creds = bool(settings.yt_client_id and settings.yt_refresh_token)
    print(f"[upload_youtube] stub upload title={title!r} creds_present={has_creds}")
    return "STUB_VIDEO_ID"
