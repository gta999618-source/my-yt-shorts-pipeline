"""
main.py — pipeline orchestrator for my-yt-shorts-pipeline.
"""

from __future__ import annotations

import sys

from src.build_video import build_video
from src.config import get_settings
from src.generate_audio import synthesize
from src.generate_script import generate_script
from src.logger import get_logger
from src.upload_youtube import upload_video


def main() -> int:
    settings = get_settings()
    log = get_logger("pipeline")

    out_dir = settings.output_path

    log.info("Pipeline starting. Topic=%r", settings.topic)

    # Stage 1 — real script
    script = generate_script(settings.topic)
    script_text = script.as_plain_text()
    script_path = out_dir / "script.txt"
    script_path.write_text(script_text, encoding="utf-8")
    log.info("Stage 1 OK — wrote %s (%d chars)", script_path, len(script_text))

    # Stage 2 — real audio + captions
    audio_path = synthesize(script_text, out_dir / "audio.mp3")
    log.info("Stage 2 OK — wrote %s", audio_path)

    # Stage 3 — real video
    video_path = build_video(
        script_text=script_text,
        audio_path=audio_path,
        srt_path=audio_path.with_suffix(".srt"),
        out_path=out_dir / "video.mp4",
    )
    log.info("Stage 3 OK — wrote %s", video_path)

    # Stage 4 — still stub
    video_id = upload_video(video_path, title=script.title)
    log.info("Stage 4 OK — video_id=%s", video_id)

    log.info("Pipeline complete. Artifacts in %s/", out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
