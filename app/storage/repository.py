from __future__ import annotations

from pathlib import Path

from app.models import WorldState
from app.storage.db import init_db, load_latest_snapshot, save_snapshot


class SnapshotRepository:
    def __init__(self, path: Path) -> None:
        self.path = path
        init_db(path)

    def load(self) -> WorldState | None:
        payload = load_latest_snapshot(self.path)
        if payload is None:
            return None
        if payload.get("version", 1) < 15:
            return None
        return WorldState.model_validate(payload)

    def save(self, state: WorldState) -> None:
        save_snapshot(self.path, state)
