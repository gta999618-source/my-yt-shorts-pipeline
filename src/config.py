"""Environment configuration & validation."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

# Load .env in local dev; in CI, GitHub Actions injects env vars directly.
load_dotenv()

# Project root = parent of src/
ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
ASSETS_DIR = ROOT / "assets"
STATE_DIR = ROOT / "state"


class Settings(BaseModel):
    """All env vars the pipeline needs. Add per-phase as needed."""

    # Phase 3 — script generation
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    script_model: str = Field(default="gpt-4o-mini", alias="SCRIPT_MODEL")

    # Phase 4 — video build
    video_width: int = Field(default=1080, alias="VIDEO_WIDTH")
    video_height: int = Field(default=1920, alias="VIDEO_HEIGHT")
    video_fps: int = Field(default=30, alias="VIDEO_FPS")

    # Phase 5 — YouTube upload
    yt_client_id: str = Field(default="", alias="YT_CLIENT_ID")
    yt_client_secret: str = Field(default="", alias="YT_CLIENT_SECRET")
    yt_refresh_token: str = Field(default="", alias="YT_REFRESH_TOKEN")

    class Config:
        populate_by_name = True
        extra = "ignore"


def load_settings() -> Settings:
    """Load settings; raise a helpful error if validation fails."""
    try:
        return Settings(**os.environ)  # type: ignore[arg-type]
    except ValidationError as exc:
        raise SystemExit(f"❌ Config error:\n{exc}") from exc


def ensure_dirs() -> None:
    """Make sure output/assets/state exist (CI fresh checkouts may skip empty dirs)."""
    for d in (OUTPUT_DIR, ASSETS_DIR, STATE_DIR):
        d.mkdir(parents=True, exist_ok=True)


# Singleton-ish accessor
settings = load_settings()
