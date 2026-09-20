"""End-to-end pipeline: fetch -> clip -> caption -> upload."""
from .config import SHORT_DURATION_SEC
from .logger import get_logger

log = get_logger(__name__)

def fetch_sources() -> list[dict]:
    """Phase 3: pull candidate videos (RSS, API, etc.)."""
    log.info("Fetching source videos (stub)")
    return []

def make_clip(video: dict) -> str | None:
    """Phase 4: cut a short clip. Returns output path or None."""
    log.info("Making clip for %s (stub, %ss)", video.get("id"), SHORT_DURATION_SEC)
    return None

def add_captions(clip_path: str) -> str:
    """Phase 5: burn in captions."""
    log.info("Captioning %s (stub)", clip_path)
    return clip_path

def upload(clip_path: str) -> None:
    """Phase 6: upload to YouTube."""
    log.info("Uploading %s (stub)", clip_path)

def run() -> None:
    log.info("Pipeline start")
    for video in fetch_sources():
        clip = make_clip(video)
        if not clip:
            continue
        clip = add_captions(clip)
        upload(clip)
    log.info("Pipeline done")

if __name__ == "__main__":
    run()
