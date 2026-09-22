"""
config.py — centralized, validated configuration for my-yt-shorts-pipeline.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Only load .env locally. CI sets env vars directly.
if os.getenv("CI") != "true":
    load_dotenv(override=False)


class Settings(BaseSettings):
    """All runtime configuration for the pipeline."""

    model_config = SettingsConfigDict(
        env_file=None,
        case_sensitive=True,
        extra="ignore",
    )

    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")

    topic: str = Field("The history of the printing press", alias="TOPIC")
    output_dir: str = Field("output", alias="OUTPUT_DIR")
    log_level: str = Field("INFO", alias="LOG_LEVEL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
