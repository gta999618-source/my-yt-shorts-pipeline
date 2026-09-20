"""Simple JSON-backed state store to avoid reprocessing."""
import json
from pathlib import Path
from .config import STATE_DIR
from .logger import get_logger

log = get_logger(__name__)
STATE_FILE = STATE_DIR / "processed.json"

def _load() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"processed": []}

def _save(data: dict) -> None:
    STATE_FILE.write_text(json.dumps(data, indent=2))

def is_processed(video_id: str) -> bool:
    return video_id in _load()["processed"]

def mark_processed(video_id: str) -> None:
    data = _load()
    if video_id not in data["processed"]:
        data["processed"].append(video_id)
        _save(data)
        log.info("Marked %s as processed", video_id)
