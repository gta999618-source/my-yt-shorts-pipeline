"""Central configuration for the pipeline."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env in local dev; in CI, GitHub Actions injects env vars directly.
load_dotenv()

# --- Paths ---
ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "output"
STATE_DIR = ROOT / "state"

for d in (ASSETS_DIR, OUTPUT_DIR, STATE_DIR):
    d.mkdir(parents=True, exist_ok=True)

# --- Pipeline settings ---
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
VIDEO_FPS = int(os.getenv("VIDEO_FPS", "30"))
SHORT_DURATION_SEC = int(os.getenv("SHORT_DURATION_SEC", "45"))

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
