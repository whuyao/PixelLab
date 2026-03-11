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
                "cash": state.player.cash,
                "portfolio": state.player.portfolio,
            },
            "agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "x": agent.position.x,
                    "y": agent.position.y,
                    "cash": agent.cash,
                    "money_desire": agent.money_desire,
                    "money_urgency": agent.money_urgency,
                    "credit_score": agent.credit_score,
                    "portfolio": agent.portfolio,
                    "location": agent.current_location,
                    "home": agent.home_label,
                    "is_resting": agent.is_resting,
                    "activity": agent.current_activity,
                    "bubble": agent.current_bubble,
                }
                for agent in state.agents
            ],
            "market": {
                "is_open": state.market.is_open,
                "sentiment": state.market.sentiment,
                "index_value": state.market.index_value,
                "stocks": [
                    {
                        "symbol": quote.symbol,
                        "price": quote.price,
                        "change_pct": quote.change_pct,
                        "day_change_pct": quote.day_change_pct,
                    }
                    for quote in state.market.stocks
                ],
                "index_history": [
                    {
                        "day": candle.day,
                        "open": candle.open,
                        "high": candle.high,
                        "low": candle.low,
                        "close": candle.close,
                        "limit_state": candle.limit_state,
                    }
                    for candle in state.market.index_history
                ],
            },
            "loans": [
                {
                    "id": loan.id,
                    "lender_id": loan.lender_id,
                    "borrower_id": loan.borrower_id,
                    "principal": loan.principal,
                    "amount_due": loan.amount_due,
                    "interest_rate": loan.interest_rate,
                    "due_day": loan.due_day,
                    "status": loan.status,
                }
                for loan in state.loans
            ],
        }
