"""
build_video.py — assemble the final vertical video.

Phase 4: real MP4 output with captions synced to audio.
"""

from __future__ import annotations

from pathlib import Path

from moviepy import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    TextClip,
)

from src.config import get_settings


def _srt_time_to_sec(t: str) -> float:
    """Convert '00:00:01,500' to 1.5 seconds."""
    t = t.strip().replace(",", ".")
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def _parse_srt(srt_path: Path) -> list[dict]:
    """Minimal SRT parser. Returns list of {start, end, text} dicts."""
    cues: list[dict] = []
    if not srt_path.exists():
        return cues

    content = srt_path.read_text(encoding="utf-8").strip()
    if not content:
        return cues

    blocks = content.split("\n\n")
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        try:
            times = lines[1].split(" --> ")
            start = _srt_time_to_sec(times[0])
            end = _srt_time_to_sec(times[1])
            text = " ".join(lines[2:]).strip()
            if text:
                cues.append({"start": start, "end": end, "text": text})
        except (ValueError, IndexError):
            continue
    return cues


def build_video(
    script_text: str,
    audio_path: Path,
    srt_path: Path,
    out_path: Path | None = None,
) -> Path:
    """Compose the final vertical MP4."""
    settings = get_settings()
    output = out_path or audio_path.with_suffix(".mp4")

    W = settings.video_width
    H = settings.video_height
    FPS = settings.video_fps

    print(f"[build_video] {W}x{H}@{FPS}fps -> {output}")

    # 1. Load audio to get duration
    audio = AudioFileClip(str(audio_path))
    duration = audio.duration

    # 2. Solid dark background
    background = ColorClip(size=(W, H), color=(15, 15, 25), duration=duration)

    # 3. Parse captions and create text clips
    caption_clips = []
    cues = _parse_srt(srt_path)
    print(f"[build_video] {len(cues)} caption cues")

    for cue in cues:
        try:
            txt = (
                TextClip(
                    text=cue["text"],
                    font_size=60,
                    color="white",
                    stroke_color="black",
                    stroke_width=3,
                    method="caption",
                    size=(W - 100, None),
                    text_align="center",
                )
                .with_start(cue["start"])
                .with_duration(cue["end"] - cue["start"])
                .with_position(("center", int(H * 0.75)))
            )
            caption_clips.append(txt)
        except Exception as e:
            print(f"[build_video] skipping cue (error: {e})")
            continue

    # 4. Composite
    final = CompositeVideoClip([background, *caption_clips])
    final = final.with_audio(audio)

    # 5. Export
    print(f"[build_video] rendering... (this takes 30-90s)")
    final.write_videofile(
        str(output),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="4000k",
        preset="medium",
        threads=4,
        logger=None,
    )

    # 6. Cleanup
    audio.close()
    final.close()
    background.close()
    for c in caption_clips:
        c.close()

    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError(f"Video render produced no output at {output}")

    mb = output.stat().st_size / (1024 * 1024)
    print(f"[build_video] OK {output.name} ({mb:.1f} MB)")
    return output
