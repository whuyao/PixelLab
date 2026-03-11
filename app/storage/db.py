from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from app.models import WorldState


def init_db(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS snapshots (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              day INTEGER NOT NULL,
              time_slot TEXT NOT NULL,
              payload TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_snapshot(path: Path, state: WorldState) -> None:
    with sqlite3.connect(path) as conn:
        conn.execute(
            "INSERT INTO snapshots (day, time_slot, payload) VALUES (?, ?, ?)",
            (state.day, state.time_slot, json.dumps(state.model_dump(mode="json"))),
        )
        conn.commit()


def load_latest_snapshot(path: Path) -> dict | None:
    if not path.exists():
        return None
    with sqlite3.connect(path) as conn:
        row = conn.execute(
            "SELECT payload FROM snapshots ORDER BY id DESC LIMIT 1"
        ).fetchone()
    if not row:
        return None
    return json.loads(row[0])
