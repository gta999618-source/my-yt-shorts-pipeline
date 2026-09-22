"""
upload_youtube.py — push a finished video to YouTube.
Phase 2: STUB. Phase 5 swaps in the YouTube Data API v3.
"""

from __future__ import annotations

from pathlib import Path


def upload_video(video_path: Path, title: str) -> str:
    """Upload the video and return its YouTube ID. STUB implementation."""
    print(f"[STUB UPLOAD] Would upload '{video_path}' as '{title}'")
    return "stub-video-id-0000"
