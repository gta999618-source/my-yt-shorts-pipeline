"""
upload_youtube.py — real YouTube Data API v3 upload.

Phase 5: replaces the Phase 2 stub. Uses OAuth refresh token
(no browser) and resumable upload for reliability.
"""

from __future__ import annotations

import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from src.config import get_settings

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# COPPA flag — must be declared. False for general content.
MADE_FOR_KIDS = False


def _credentials() -> Credentials:
    """Build Credentials from the refresh token — no browser needed."""
    settings = get_settings()

    if not (
        settings.yt_client_id
        and settings.yt_client_secret
        and settings.yt_refresh_token
    ):
        raise SystemExit(
            "Missing YouTube OAuth secrets. "
            "Set YT_CLIENT_ID, YT_CLIENT_SECRET, and YT_REFRESH_TOKEN."
        )

    return Credentials(
        token=None,  # library refreshes automatically
        refresh_token=settings.yt_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.yt_client_id,
        client_secret=settings.yt_client_secret,
        scopes=SCOPES,
    )


def upload_video(
    video_path: Path,
    title: str,
    description: str = "",
    tags: list[str] | None = None,
    privacy: str | None = None,
) -> str:
    """Upload via resumable protocol. Returns the YouTube video ID."""
    settings = get_settings()
    tags = tags or []
    privacy = privacy or settings.yt_privacy

    if not video_path.exists() or video_path.stat().st_size == 0:
        raise RuntimeError(f"Video file missing or empty: {video_path}")

    title = title[:100]  # YouTube hard limit
    size_mb = video_path.stat().st_size / (1024 * 1024)
    print(
        f"[upload_youtube] {video_path.name} ({size_mb:.1f} MB) "
        f"title={title!r} tags={len(tags)} privacy={privacy}"
    )

    youtube = build(
        "youtube", "v3",
        credentials=_credentials(),
        cache_discovery=False,
    )

    body = {
        "snippet": {
            "title": title,
            "description": description[:5000],
            "tags": tags[:500],
            "categoryId": settings.yt_category_id,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": MADE_FOR_KIDS,
        },
    }

    media = MediaFileUpload(
        str(video_path),
        mimetype="video/*",
        resumable=True,
        chunksize=256 * 1024,  # 256 KiB — required multiple
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    retries = 0
    max_retries = 5

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"[upload_youtube]   {pct}% uploaded")
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504):
                retries += 1
                if retries > max_retries:
                    raise
                wait = min(2 ** retries, 60)
                print(f"[upload_youtube]   transient {e.resp.status}, retry in {wait}s")
                time.sleep(wait)
            else:
                raise

    video_id = response["id"]
    print(f"[upload_youtube] OK https://youtu.be/{video_id}")
    print(f"[upload_youtube]   status={response['status']['uploadStatus']}")
    print(f"[upload_youtube]   privacy={response['status']['privacyStatus']}")
    return video_id
