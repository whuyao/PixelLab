from __future__ import annotations

from typing import TYPE_CHECKING

from app.models import WorldState

if TYPE_CHECKING:
    from app.engine.game_engine import GameEngine


class LifestyleEngine:
    def __init__(self, host: "GameEngine") -> None:
        self.host = host

    def prepare_view(self) -> WorldState:
        self.host._refresh_lifestyle_state()
        return self.host.state

    def run_tick(self) -> WorldState:
        self.host._trigger_lifestyle_activity()
        self.host._refresh_lifestyle_state()
        return self.host.state

    def run_new_day(self) -> WorldState:
        self.host._update_inflation_state()
        self.host._update_daily_cost_baselines()
        self.host._settle_property_income()
        self.host._settle_daily_living_costs()
        self.host._refresh_lifestyle_state()
        return self.host.state

    def player_consume(self, item_id: str, recipient_id: str = "player", financed: bool = False) -> WorldState:
        self.host._player_consume_item(item_id, recipient_id, financed=financed)
        self.host._refresh_lifestyle_state()
        return self.host.state

    def player_buy_property(self, property_id: str, financed: bool = False) -> WorldState:
        self.host._player_buy_property(property_id, financed=financed)
        self.host._refresh_lifestyle_state()
        return self.host.state

    def player_sell_property(self, property_id: str) -> WorldState:
        self.host._player_sell_property(property_id)
        self.host._refresh_lifestyle_state()
        return self.host.state
