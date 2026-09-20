"""End-to-end pipeline orchestrator. Runs inside GitHub Actions."""
from __future__ import annotations

import sys
import traceback

from src.build_video import build_video
from src.config import ensure_dirs, settings
from src.generate_audio import generate_audio
from src.generate_script import generate_script
from src.upload_youtube import upload_video


def run(topic: str = "Why the sky is blue") -> int:
    print("🚀 Pipeline start")
    ensure_dirs()
    print(f"   model={settings.script_model} size={settings.video_width}x{settings.video_height}")

    script = generate_script(topic)
    audio = generate_audio(script.body)
    video = build_video(script.body, audio)
    video_id = upload_video(video, script.title, script.body, script.tags)

    print(f"✅ Pipeline done. video_id={video_id}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
