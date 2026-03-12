from __future__ import annotations

from typing import TYPE_CHECKING

from app.models import LabEvent, WorldState

if TYPE_CHECKING:
    from app.engine.game_engine import GameEngine


class MarketEngine:
    def __init__(self, host: "GameEngine") -> None:
        self.host = host

    def prepare_view(self) -> WorldState:
        self.host._sync_market_clock()
        self.host._refresh_market_microstructure()
        self.host._update_index_history(append=False)
        self.host._update_daily_index_history()
        return self.host.state

    def run_intraday_tick(self) -> WorldState:
        self.host._sync_market_clock()
        self.host._update_market_intraday()
        self.host._trigger_market_activity()
        return self.host.state

    def handle_event(self, event: LabEvent) -> WorldState:
        self.host._apply_event_to_market(event)
        return self.host.state

    def player_trade(self, symbol: str, side: str, shares: int) -> WorldState:
        self.host._sync_market_clock()
        if not self.host.state.market.is_open:
            raise ValueError("现在已经收盘了，等白天再交易。")
        self.host._execute_trade_for_player(symbol.upper(), side, shares, manual=True)
        self.host._refresh_tasks()
        return self.host.state

    def auto_trade_player(self) -> WorldState:
        self.host._sync_market_clock()
        if not self.host.state.market.is_open:
            return self.host.state
        symbol, side, shares, reason = self.host._decide_player_trade()
        self.host._execute_trade_for_player(symbol, side, shares, manual=False, reason=reason)
        self.host._refresh_tasks()
        return self.host.state
