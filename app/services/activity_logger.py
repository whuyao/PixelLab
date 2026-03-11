from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.models import WorldState


class ActivityLogger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event_type: str, state: WorldState, **payload: Any) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event_type": event_type,
            "day": state.day,
            "time_slot": state.time_slot,
            "positions": self._positions_snapshot(state),
            **payload,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _positions_snapshot(self, state: WorldState) -> dict[str, Any]:
        return {
            "player": {
                "id": state.player.id,
                "name": state.player.name,
                "x": state.player.position.x,
                "y": state.player.position.y,
            },
            "agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "x": agent.position.x,
                    "y": agent.position.y,
                    "location": agent.current_location,
                    "home": agent.home_label,
                    "is_resting": agent.is_resting,
                    "activity": agent.current_activity,
                    "bubble": agent.current_bubble,
                }
                for agent in state.agents
            ],
        }
