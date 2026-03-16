from __future__ import annotations

import hashlib
import json
import random
import re
from dataclasses import dataclass
from uuid import uuid4

from app.engine.dialogue_system import (
    DESIRE_LABELS,
    ambient_line_for,
    desire_label_for_agent,
    dominant_desire_for_agent,
    self_reflection_for,
    weather_label,
)
from app.engine.event_system import build_internal_event
from app.engine.lifestyle_engine import LifestyleEngine
from app.engine.market_engine import MarketEngine
from app.engine.social_engine import SocialEngine
from app.engine.task_system import apply_task_progress
from app.engine.time_system import advance_time
from app.engine.world_state import build_initial_world
from app.models import AnalysisPoint, Agent, BankLoanRecord, BusinessEntity, CasinoState, ConsumableItem, DailyBankPoint, DailyBriefItem, DailyBriefing, DailyBusinessPoint, DailyCasinoPoint, DailyEconomyPoint, DialogueOutcome, DialogueRecord, FeedPost, FinanceRecord, GrayCase, IndexCandle, LabEvent, LoanRecord, MemoryEntry, NewsTimelineItem, Point, PropertyAsset, SocialThread, StateDiffResponse, StoryBeat, Task, TimeSlot, TouristAgent, TourismState, WorldState
from app.services.activity_logger import ActivityLogger


WORLD_WIDTH = 44
WORLD_HEIGHT = 26
SLOT_SEQUENCE: list[TimeSlot] = ["morning", "noon", "afternoon", "evening", "night"]


@dataclass(slots=True)
class Room:
    name: str
    x1: int
    y1: int
    x2: int
    y2: int

    def contains(self, x: int, y: int) -> bool:
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def clamp(self, x: int, y: int) -> Point:
        return Point(x=max(self.x1, min(self.x2, x)), y=max(self.y1, min(self.y2, y)))


ROOMS = [
    Room("foyer", 1, 2, 8, 24),
    Room("office", 9, 2, 18, 10),
    Room("compute", 19, 2, 28, 10),
    Room("data_wall", 29, 2, 43, 10),
    Room("meeting", 10, 12, 25, 24),
    Room("lounge", 26, 12, 43, 24),
]

OBSTACLES = [
    Room("grove_north", 2, 3, 4, 6),
    Room("grove_south", 2, 17, 4, 21),
    Room("herb_bed_west", 11, 4, 12, 6),
    Room("herb_bed_mid", 14, 5, 15, 7),
    Room("herb_bed_east", 16, 3, 17, 5),
    Room("rock_patch_north", 22, 4, 23, 5),
    Room("rock_patch_south", 25, 7, 26, 8),
    Room("orchard_west", 32, 3, 33, 4),
    Room("orchard_mid", 36, 4, 37, 5),
    Room("orchard_east", 40, 6, 41, 7),
    Room("lake_water", 28, 15, 42, 24),
    Room("hay_stack", 16, 18, 17, 19),
    Room("shrub_patch", 22, 14, 23, 15),
    Room("log_stack", 38, 16, 39, 17),
    Room("pine_cluster", 40, 20, 42, 22),
    Room("sunflower_patch", 12, 20, 13, 22),
]

HUBS = {
    "lin": {"morning": (34, 5), "noon": (18, 17), "afternoon": (33, 7), "evening": (29, 18), "night": (20, 18)},
    "mika": {"morning": (13, 17), "noon": (19, 18), "afternoon": (31, 6), "evening": (28, 20), "night": (27, 19)},
    "jo": {"morning": (24, 6), "noon": (13, 9), "afternoon": (23, 7), "evening": (17, 17), "night": (11, 8)},
    "rae": {"morning": (33, 20), "noon": (15, 18), "afternoon": (29, 19), "evening": (36, 20), "night": (31, 20)},
    "kai": {"morning": (40, 5), "noon": (33, 18), "afternoon": (39, 7), "evening": (35, 19), "night": (37, 21)},
}

ROOM_LABELS = {
    "foyer": "林间入口",
    "office": "香草苗圃",
    "compute": "石径工坊",
    "data_wall": "果园坡地",
    "meeting": "麦田广场",
    "lounge": "湖畔营地",
}

RESOURCE_LABELS = {
    "compute": "算力窗口",
    "evidence": "证据链",
    "attention": "团队注意力",
    "signal": "外部信号窗口",
    "calm": "团队缓冲空间",
}

HOME_SPOTS = {
    "lin": (9, 3, "林澈的小屋"),
    "mika": (14, 23, "米遥的小屋"),
    "jo": (21, 3, "周铖的小屋"),
    "rae": (24, 23, "芮宁的小屋"),
    "kai": (38, 3, "凯川的小屋"),
}

PROPERTY_LAYOUT_ANCHORS: dict[str, list[tuple[int, int]]] = {
    "property-player-cottage": [(6, 22)],
    "property-lin-cottage": [(9, 2)],
    "property-mika-cottage": [(14, 22)],
    "property-jo-cottage": [(21, 2)],
    "property-rae-cottage": [(24, 22)],
    "property-kai-cottage": [(38, 2)],
    "property-farm-north": [(14, 14)],
    "property-greenhouse-lot": [(23, 18), (22, 18)],
    "property-shop-orchard": [(35, 8)],
    "property-rental-lakeside": [(39, 12)],
    "property-tourist-inn": [(34, 12)],
    "property-tourist-market": [(6, 14)],
    "property-underground-casino": [(30, 8)],
    "property-qingsong-coop": [(11, 12)],
    "property-backstreet-store": [(28, 11)],
}

ACTIVITY_ANCHORS: dict[str, list[tuple[int, int]]] = {
    "market_chat": [(7, 16), (9, 15), (11, 15)],
    "market_watch": [(8, 14), (10, 14), (12, 14)],
    "inn_forecourt": [(35, 14), (37, 14), (34, 16)],
    "workshop_huddle": [(24, 7), (26, 6), (34, 6)],
    "foyer_gossip": [(13, 8), (18, 6), (21, 6)],
    "lakeside_pause": [(29, 20), (33, 20), (37, 20)],
    "buyer_tour": [(34, 19), (23, 18), (35, 8), (24, 7)],
    "vip_stroll": [(29, 20), (34, 6), (24, 7), (37, 20)],
    "noon_social": [(17, 18), (24, 18), (33, 18)],
    "coop_stop": [(12, 14), (13, 12)],
    "backstreet_stop": [(29, 13), (30, 11)],
}

SLOT_ACTIVITY_ANCHORS: dict[str, list[str]] = {
    "morning": ["workshop_huddle", "foyer_gossip"],
    "noon": ["noon_social", "market_chat", "lakeside_pause"],
    "afternoon": ["workshop_huddle", "market_watch", "buyer_tour"],
    "evening": ["market_chat", "lakeside_pause", "inn_forecourt"],
    "night": ["inn_forecourt", "lakeside_pause"],
}

DISPLAY_NAME_BY_ID = {
    "lin": "林澈",
    "mika": "米遥",
    "jo": "周铖",
    "rae": "芮宁",
    "kai": "凯川",
}

LEGACY_NAME_REPLACEMENTS = {
    "Lin": "林澈",
    "Mika": "米遥",
    "Jo": "周铖",
    "Rae": "芮宁",
    "Kai": "凯川",
    "general": "社会热点",
    "market": "市场",
    "geoai": "GeoAI",
    "policy": "政策",
    "gaming": "游戏行业",
    "tech": "科技动向",
    "foyer": "林间入口",
    "office": "香草苗圃",
    "compute": "石径工坊",
    "data_wall": "果园坡地",
    "meeting": "麦田广场",
    "lounge": "湖畔营地",
}

FORCED_REST_THRESHOLD = 8
MARKET_SYMBOL_PREFERENCE = {
    "rational": "GEO",
    "creative": "AGR",
    "engineering": "SIG",
    "empathetic": "AGR",
    "opportunist": "SIG",
}
LIMIT_MOVE_PCT = 10.0
GEOAI_BASE_MILESTONES = [50, 100, 180, 260, 360, 500, 700, 950]
GEOAI_MILESTONE_STEP = 350


def geoai_milestones_up_to(current: int) -> list[int]:
    milestones = list(GEOAI_BASE_MILESTONES)
    next_threshold = GEOAI_BASE_MILESTONES[-1] + GEOAI_MILESTONE_STEP
    while next_threshold <= current:
        milestones.append(next_threshold)
        next_threshold += GEOAI_MILESTONE_STEP
    return milestones
BASE_PRICES = {"GEO": 24.0, "AGR": 18.0, "SIG": 31.0}
INDEX_WEIGHTS = {"GEO": 0.42, "AGR": 0.33, "SIG": 0.25}
SECTOR_BETA = {"GEO": 1.14, "AGR": 0.82, "SIG": 1.28}
IDIOSYNCRATIC_VOL = {"GEO": 0.72, "AGR": 0.58, "SIG": 0.94}
BASE_SHARES_OUTSTANDING = {"GEO": 180000, "AGR": 240000, "SIG": 150000}
BASE_AVG_VOLUME = {"GEO": 5600, "AGR": 4800, "SIG": 5200}
TOURIST_NAME_POOL = ["许栀", "沈禾", "顾岚", "孟遥", "程汐", "唐屿", "苏楠", "袁栩", "陆晴", "乔朔"]
TOURIST_ARCHETYPES = [
    {
        "archetype": "周末散客",
        "topic_pool": ["天气、住宿和集市小吃", "湖边散步和值不值得多待", "住一晚划不划算", "这里晚上安不安静"],
        "spending_desire": 54,
        "budget": 18,
    },
    {
        "archetype": "摄影游客",
        "topic_pool": ["果园、湖边和好看的角落", "哪块光线最好", "夜里哪里最有气氛", "哪处最适合慢慢走"],
        "spending_desire": 48,
        "budget": 16,
    },
    {
        "archetype": "短住买手",
        "topic_pool": ["集市、价格和什么值得带回去", "房租、短住和生活成本", "哪块更适合长住", "手里的钱花在哪更值"],
        "spending_desire": 68,
        "budget": 26,
    },
    {
        "archetype": "考察访客",
        "topic_pool": ["GeoAI、小镇故事和谁最懂这里", "这地方怎么一步步变成这样", "谁在推动这里变化", "科技和日常到底怎么缠在一起"],
        "spending_desire": 42,
        "budget": 14,
    },
]
TOURISM_EVENT_TITLES = [
    "湖畔夜市",
    "周末采风日",
    "田园慢生活节",
    "果园开放日",
]
TOURIST_SIGNAL_BANK = [
    {"title": "游客带来外地买手消息", "summary": "几位游客提到外地渠道正在回补农食和文旅周边订单。", "category": "market", "tone": 1, "target": "AGR", "strength": 2},
    {"title": "游客聊起一波空间智能参访热", "summary": "来访者频繁讨论小镇里的 GeoAI 展示和空间智能体验，市场开始把相关能力当成新的卖点。", "category": "geoai", "tone": 1, "target": "GEO", "strength": 2},
    {"title": "游客带来一条监管收紧风声", "summary": "短住买手在集市里谈到外地监管可能收紧交易和数据流通，大家情绪明显谨慎。", "category": "market", "tone": -1, "target": "SIG", "strength": 3},
    {"title": "游客口中的消费回暖传闻", "summary": "回头客在旅馆里说，周边几个片区的消费人流比上月明显回暖。", "category": "general", "tone": 1, "target": "AGR", "strength": 2},
    {"title": "游客散播一条地产观望消息", "summary": "看房游客普遍觉得短期房价偏高，购买动作可能会先放慢。", "category": "market", "tone": -1, "target": "AGR", "strength": 2},
]


class GameEngine:
    def __init__(self, state: WorldState | None = None, activity_logger: ActivityLogger | None = None) -> None:
        self.random = random.Random(7)
        self.activity_logger = activity_logger
        is_new_world = state is None
        self.state = state or build_initial_world()
        self.market_engine = MarketEngine(self)
        self.social_engine = SocialEngine(self)
        self.lifestyle_engine = LifestyleEngine(self)
        self.state.world_width = WORLD_WIDTH
        self.state.world_height = WORLD_HEIGHT
        if is_new_world:
            self.state.player.position = Point(x=7, y=20)
            for agent in self.state.agents:
                x, y = HUBS[agent.id][self.state.time_slot]
                agent.position = Point(x=x, y=y)
                agent.current_location = self._room_for(x, y)
        self._ensure_agent_runtime_fields()
        self._update_inflation_state()
        self._refresh_presence()

    def get_state(self) -> WorldState:
        self._ensure_agent_runtime_fields()
        self._refresh_bank_state()
        self._refresh_government_agent_state()
        self.market_engine.prepare_view()
        self._refresh_tasks()
        self.social_engine.prepare_view()
        self.lifestyle_engine.prepare_view()
        self._normalize_recent_dialogue_history()
        self._sync_event_history()
        self._refresh_state_signatures()
        return self.state

    def get_state_diff(self, signatures: dict[str, str] | None = None) -> StateDiffResponse:
        self.get_state()
        sections = self._build_state_sections()
        current_signatures = self._sign_sections(sections)
        changed = [
            name
            for name, signature in current_signatures.items()
            if (signatures or {}).get(name) != signature
        ]
        return StateDiffResponse(
            version=self.state.version,
            signatures=current_signatures,
            changed=changed,
            sections={name: sections[name] for name in changed},
        )

    def _refresh_state_signatures(self) -> None:
        self.state.version = max(self.state.version, 60)
        self.state.section_signatures = self._sign_sections(self._build_state_sections())

    def _sign_sections(self, sections: dict[str, object]) -> dict[str, str]:
        return {
            name: hashlib.sha1(
                json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()[:12]
            for name, payload in sections.items()
        }

    def _build_state_sections(self) -> dict[str, object]:
        state = self.state
        def dump(value: object) -> object:
            if hasattr(value, "model_dump"):
                return value.model_dump(mode="json")
            if isinstance(value, list):
                return [dump(item) for item in value]
            if isinstance(value, dict):
                return {key: dump(item) for key, item in value.items()}
            return value

        return {
            "metrics": {
                "day": state.day,
                "time_slot": state.time_slot,
                "weather": state.weather,
                "lab": dump(state.lab),
                "geoai_milestones": list(state.geoai_milestones),
                "market": dump(state.market),
                "company": dump(state.company),
                "tourism": dump(state.tourism),
                "casino": dump(state.casino),
            },
            "analysis": {
                "analysis_history": dump(state.analysis_history[-40:]),
                "daily_economy_history": dump(state.daily_economy_history[-40:]),
                "daily_bank_history": dump(state.daily_bank_history[-40:]),
                "daily_casino_history": dump(state.daily_casino_history[-40:]),
                "agents": dump(state.agents),
                "player": dump(state.player),
                "tourists": dump(state.tourists),
                "tourism": dump(state.tourism),
                "events": dump(state.events),
                "gray_cases": dump(state.gray_cases),
                "market": dump(state.market),
                "casino": dump(state.casino),
            },
            "fiscal": {
                "day": state.day,
                "government": dump(state.government),
                "finance_history": dump(state.finance_history[:240]),
                "casino": dump(state.casino),
            },
            "tasks": {
                "tasks": dump(state.tasks),
                "archived_tasks": dump(state.archived_tasks[:20]),
            },
            "events": {
                "gray_cases": dump(state.gray_cases),
                "story_beats": dump(state.story_beats[:18]),
                "events": dump(state.events),
                "event_history": dump(state.event_history[:220]),
            },
            "finance": {
                "finance_history": dump(state.finance_history[:240]),
            },
            "dialogue": {
                "latest_dialogue": dump(state.latest_dialogue),
                "dialogue_history": dump(state.dialogue_history[:1000]),
                "loans": dump(state.loans),
            },
            "feed": {
                "feed_timeline": dump(state.feed_timeline[:1000]),
            },
            "daily": {
                "daily_briefings": dump(state.daily_briefings[:3]),
            },
            "signals": {
                "news_timeline": dump(state.news_timeline[:40]),
                "latest_signal": state.events[0].title if state.events else "",
                "tourism_latest_signal": state.tourism.latest_signal if state.tourism else "",
            },
            "gray_cases": {
                "gray_cases": dump(state.gray_cases),
            },
            "memory": {
                "player": dump(state.player),
                "agents": dump(state.agents),
                "tourists": dump(state.tourists),
                "tourism": dump(state.tourism),
                "properties": dump(state.properties),
                "loans": dump(state.loans),
                "bank_loans": dump(state.bank_loans),
                "dialogue_history": dump(state.dialogue_history[:80]),
                "company": dump(state.company),
                "day": state.day,
                "time_slot": state.time_slot,
            },
            "market": {
                "market": dump(state.market),
                "player": dump(state.player),
                "agents": dump(state.agents),
                "tourists": dump(state.tourists),
                "tourism": dump(state.tourism),
                "casino": dump(state.casino),
                "bank": dump(state.bank),
                "bank_loans": dump(state.bank_loans),
            },
            "bank": {
                "bank": dump(state.bank),
                "bank_loans": dump(state.bank_loans),
                "player": dump(state.player),
                "agents": dump(state.agents),
                "casino": dump(state.casino),
            },
            "lifestyle": {
                "player": dump(state.player),
                "agents": dump(state.agents),
                "tourists": dump(state.tourists),
                "tourism": dump(state.tourism),
                "casino": dump(state.casino),
                "properties": dump(state.properties),
                "lifestyle_catalog": dump(state.lifestyle_catalog),
                "company": dump(state.company),
                "bank_loans": dump(state.bank_loans),
                "bank": dump(state.bank),
            },
        }

    def _sync_event_history(self) -> None:
        if getattr(self.state, "event_history", None) is None:
            self.state.event_history = []
        known_ids = {event.id for event in self.state.event_history}
        for event in self.state.events:
            if event.id in known_ids:
                continue
            self.state.event_history.insert(0, event.model_copy(deep=True))
            known_ids.add(event.id)
        self.state.event_history = self.state.event_history[:200]

    def log_world_snapshot(self, event_type: str, details: dict[str, object] | None = None) -> None:
        self._log(event_type, **(details or {}))

    def move_player(self, dx: int, dy: int) -> WorldState:
        if abs(dx) > 1 or abs(dy) > 1:
            raise ValueError("每次移动不能超过一格。")
        previous = self.state.player.position.model_copy()
        next_point = self._move_with_collision(self.state.player.position, dx, dy)
        if next_point == self.state.player.position and (dx != 0 or dy != 0):
            raise ValueError("那边有树丛、石头或围栏挡着，换条路走。")
        self.state.player.position = next_point
        self.state.player.daily_actions.append(f"move:{next_point.x},{next_point.y}")
        self._log(
            "player_move",
            actor={"id": self.state.player.id, "name": self.state.player.name},
            movement={"from": previous.model_dump(), "to": next_point.model_dump(), "delta": {"dx": dx, "dy": dy}},
        )
        return self.state

    def interact_with_agent(self, agent_id: str) -> DialogueOutcome:
        if self.has_tourist(agent_id):
            tourist = self.get_tourist(agent_id)
            outcome = DialogueOutcome(
                agent_id=tourist.id,
                agent_name=tourist.name,
                line=tourist.current_bubble or f"{tourist.name} 正在四处张望，像是想和人聊两句。",
                topic=tourist.favorite_topic or "临时闲聊",
                bubble_text=tourist.current_bubble or "这里还挺热闹。",
                effects=["游客正在观察周围。"],
            )
            self.state.latest_dialogue = outcome
            return outcome
        return self.social_engine.interact_with_agent(agent_id)

    def player_trade(self, symbol: str, side: str, shares: int) -> WorldState:
        return self.market_engine.player_trade(symbol, side, shares)

    def auto_trade_player(self) -> WorldState:
        return self.market_engine.auto_trade_player()

    def player_consume_item(self, item_id: str, recipient_id: str = "player", financed: bool = False) -> WorldState:
        return self.lifestyle_engine.player_consume(item_id, recipient_id=recipient_id, financed=financed)

    def player_buy_property(self, property_id: str, financed: bool = False) -> WorldState:
        return self.lifestyle_engine.player_buy_property(property_id, financed=financed)

    def player_sell_property(self, property_id: str) -> WorldState:
        return self.lifestyle_engine.player_sell_property(property_id)

    def player_gamble(self, amount: int = 20) -> WorldState:
        asset = self._casino_asset()
        if asset is None:
            raise ValueError("地下赌场今晚没有开门。")
        if not self._is_player_near_property(asset, radius=2):
            raise ValueError("你还没走到地下赌场门口，先靠近后再试手气。")
        stake = max(5, min(int(amount or 20), 2000))
        if self.state.player.cash < stake:
            raise ValueError(f"你手头现金只有 ${self.state.player.cash}，不够下注 ${stake}。")
        result = self._resolve_casino_round(
            payer_type="player",
            payer_id=self.state.player.id,
            payer_name=self.state.player.name,
            available_cash=self.state.player.cash,
            stake=stake,
            trigger="manual",
        )
        gambling_tax = result["tax"]
        gross_payout = result["payout"]
        net_delta = result["net"]
        outcome_text = result["outcome"]
        if gross_payout > 0:
            self.state.player.cash += gross_payout
        self._adjust_player_satisfaction(int(result["satisfaction"]))
        self.state.player.daily_actions.append(f"casino:{outcome_text}:${stake}")
        self.state.player.last_trade_summary = f"你在后巷地下赌场下注 ${stake}，{outcome_text}，净变化 ${net_delta}。"
        self.state.player.current_activity = "刚在后巷地下赌场的牌桌边收手，脑子还在回味上一把。"
        self.state.player.current_bubble = "再来一把，还是先收手？"
        event_summary = (
            f"你在后巷地下赌场下注 ${stake}，{outcome_text}。"
            f"{' 台面返还了 $' + str(gross_payout) + '。' if gross_payout else ' 这把直接打了水漂。'}"
            f" 政府顺手抽走了 ${gambling_tax} 的赌税。"
        )
        self.state.events.insert(
            0,
            build_internal_event(
                title="后巷地下赌场又亮起了灯",
                summary=event_summary,
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="ambient_dialogue",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=["player"],
                participant_names=[self.state.player.name],
                topic="地下赌场",
                summary=event_summary,
                key_point=f"下注 ${stake}，赌税 ${gambling_tax}，牌桌返还 ${gross_payout}，净变化 ${net_delta}。",
                transcript=[
                    f"你：今晚试一把，先压 ${stake}。",
                    f"庄家：{outcome_text}{'，拿走 $' + str(gross_payout) if gross_payout else '。'}",
                ],
                desire_labels={self.state.player.name: "试试运气，赌一口气"},
                mood="warm" if net_delta > 0 else "tense" if net_delta < -stake // 2 else "neutral",
                financial_note=f"下注 ${stake}，赌税 ${gambling_tax}，牌桌返还 ${gross_payout}。",
                gray_trade=True,
                gray_trade_type="地下赌博",
                gray_trade_severity=2 if gross_payout else 3,
            )
        )
        self._append_finance_record(
            actor_id=self.state.player.id,
            actor_name=self.state.player.name,
            category="casino",
            action="gamble",
            summary=f"你在 {asset.name} 下注 ${stake}，{outcome_text}，净变化 ${net_delta}，赌税 ${gambling_tax}。",
            amount=net_delta,
            asset_name=asset.name,
            counterparty="灰市牌桌",
        )
        self._record_casino_stats(stake=stake, payout=gross_payout, tax=gambling_tax, actor_name=self.state.player.name, actor_type="player")
        self._maybe_register_casino_case(
            actor_id=self.state.player.id,
            actor_name=self.state.player.name,
            actor_type="player",
            stake=stake,
            net_delta=net_delta,
            trigger="manual",
        )
        self._maybe_publish_casino_buzz(
            actor_name=self.state.player.name,
            actor_type="player",
            stake=stake,
            outcome_text=outcome_text,
            net_delta=net_delta,
            tourist=False,
        )
        if net_delta >= max(140, stake):
            self.state.player.current_bubble = "今晚手气真在我这边。"
        self._log(
            "player_gamble",
            casino={"id": asset.id, "name": asset.name},
            wager={"stake": stake, "tax": gambling_tax, "payout": gross_payout, "net": net_delta, "outcome": outcome_text},
        )
        self._refresh_presence()
        self._refresh_tasks()
        self._refresh_memory_streams()
        return self.state

    def _resolve_casino_round(
        self,
        *,
        payer_type: str,
        payer_id: str,
        payer_name: str,
        available_cash: int,
        stake: int,
        trigger: str,
    ) -> dict[str, int | str]:
        stake = max(5, min(int(stake), min(1200, max(5, available_cash))))
        gambling_tax = self._collect_tax(
            payer_type=payer_type,
            payer_id=payer_id,
            payer_name=payer_name,
            revenue_key="gambling",
            label="地下赌场下注",
            base_amount=stake,
            rate_pct=max(4.0, self.state.government.consumption_tax_rate_pct * 0.9),
            minimum=1,
        )
        roll = self.random.random()
        if roll < 0.035:
            gross_payout = int(round(stake * 4.2))
            outcome_text = "一下吃到大彩头"
            satisfaction_delta = 12
            stress_delta = -8
        elif roll < 0.18:
            gross_payout = int(round(stake * 2.15))
            outcome_text = "赢得挺痛快"
            satisfaction_delta = 7
            stress_delta = -5
        elif roll < 0.37:
            gross_payout = int(round(stake * 1.28))
            outcome_text = "小赢了一点"
            satisfaction_delta = 3
            stress_delta = -2
        elif roll < 0.49:
            gross_payout = int(round(stake * 0.92))
            outcome_text = "差一点就回本了"
            satisfaction_delta = -1
            stress_delta = 1
        else:
            gross_payout = 0
            outcome_text = "这一把基本输干净了"
            satisfaction_delta = -6 if stake >= 80 else -4
            stress_delta = 5 if trigger != "desperation" else 7
        net_delta = gross_payout - stake - gambling_tax
        return {
            "stake": stake,
            "tax": gambling_tax,
            "payout": gross_payout,
            "net": net_delta,
            "outcome": outcome_text,
            "satisfaction": satisfaction_delta,
            "stress": stress_delta,
        }

    def _record_casino_stats(self, *, stake: int, payout: int, tax: int, actor_name: str, actor_type: str) -> None:
        casino = self.state.casino
        casino.daily_visits += 1
        casino.total_visits += 1
        casino.daily_wagers += stake
        casino.total_wagers += stake
        casino.daily_payouts += payout
        casino.total_payouts += payout
        casino.daily_tax += tax
        casino.total_tax += tax
        if payout >= stake * 2:
            casino.daily_big_wins += 1
            casino.total_big_wins += 1
        casino.house_bankroll = max(0, casino.house_bankroll + stake - payout)
        casino.current_heat = self._bounded(casino.current_heat + (4 if stake >= 80 else 2) + (3 if payout > 0 else 0))
        actor_label = "游客" if actor_type == "tourist" else "镇上人" if actor_type == "agent" else "你"
        casino.last_note = f"{actor_name} 这轮在牌桌押了 ${stake}，{actor_label}们又开始谈论今晚赌场手气。"

    def _maybe_register_casino_case(
        self,
        *,
        actor_id: str,
        actor_name: str,
        actor_type: str,
        stake: int,
        net_delta: int,
        trigger: str,
    ) -> None:
        severity = 3 if stake >= 140 or trigger == "desperation" else 2 if stake >= 60 else 1
        chance = 0.18 + severity * 0.09 + (0.1 if actor_type == "tourist" else 0.05)
        if self.random.random() > min(0.62, chance):
            return
        case = GrayCase(
            id=f"gray-{uuid4().hex[:8]}",
            case_type="underground_gambling",
            participants=[actor_id, "gray-market"],
            participant_names=[actor_name, "灰市牌桌"],
            topic="后巷地下赌场",
            summary=f"{actor_name} 刚在后巷地下赌场押了 ${stake}，牌桌输赢和税费都开始引来风声。",
            amount=abs(net_delta) if net_delta != 0 else stake,
            severity=severity,
            start_day=self.state.day,
            due_day=self.state.day + (1 if severity >= 3 else 2),
            exposure_risk=min(94, 18 + severity * 18 + (12 if stake >= 180 else 0)),
            status="active",
        )
        self.state.gray_cases.insert(0, case)
        self.state.gray_cases = self.state.gray_cases[:16]

    def _maybe_publish_casino_buzz(
        self,
        *,
        actor_name: str,
        actor_type: str,
        stake: int,
        outcome_text: str,
        net_delta: int,
        tourist: bool,
    ) -> None:
        if self.random.random() > (0.62 if stake >= 120 or abs(net_delta) >= 120 else 0.44 if stake >= 80 else 0.22):
            return
        category = "gossip" if tourist or stake < 100 else "market"
        hot_line = (
            f"{actor_name} 今晚在后巷地下赌场{outcome_text}，旁边已经有人在议论谁又想靠赌桌翻身。"
            if net_delta >= 0
            else f"{actor_name} 刚在后巷地下赌场栽了一手，旁边已经有人把这事当八卦在传。"
        )
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="tourist" if tourist else "system",
            author_id="casino-buzz" if tourist else "system",
            author_name=actor_name if tourist else "系统新闻台",
            day=self.state.day,
            time_slot=self.state.time_slot,
            category=category,
            content=hot_line[:160],
            topic_tags=["赌场", "灰市", "牌桌风声"],
            desire_tags=["赌一口气", "翻本", "看热闹"],
            likes=4 + min(20, stake // 20),
            views=40 + min(240, stake),
            summary="后巷地下赌场又成了大家嘴里的热议点。",
            impacts=["影响团队氛围", "影响监管注意力", "影响游客讨论"],
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        self._append_feed_post(post, remember=True, apply_impacts=True)

    def _append_casino_event(self, actor_name: str, stake: int, outcome_text: str, net_delta: int, *, tourist: bool) -> None:
        tone = "market" if abs(net_delta) >= 80 or stake >= 100 else "general"
        label = "游客" if tourist else "镇上人"
        summary = (
            f"{actor_name} 刚在后巷地下赌场押了 ${stake}，{outcome_text}，净变化 ${net_delta}。"
            f" 这一下又把{label}们的注意力拽回了后巷牌桌。"
        )
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"{actor_name} 在后巷地下赌场试了手气",
                summary=summary,
                slot=self.state.time_slot,
                category=tone,
            ),
        )
        self.state.events = self.state.events[:8]

    def _append_casino_dialogue_record(
        self,
        *,
        actor_id: str,
        actor_name: str,
        actor_role: str,
        stake: int,
        outcome_text: str,
        net_delta: int,
        payout: int,
        tax: int,
    ) -> None:
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="gray_trade",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=[actor_id],
                participant_names=[actor_name],
                topic="地下赌场",
                summary=f"{actor_name} 在后巷地下赌场压了 ${stake}，{outcome_text}，净变化 ${net_delta}。",
                key_point=f"{actor_name} 压了 ${stake}，返还 ${payout}，赌税 ${tax}，净变化 ${net_delta}。",
                transcript=[
                    f"{actor_name}：我先压 ${stake}，看看今晚手气站不站我这边。",
                    f"庄家：{outcome_text}{'，桌上回了 $' + str(payout) if payout else '。'}",
                ],
                desire_labels={actor_name: "想搏一把运气和现金缓冲"},
                mood="warm" if net_delta > 0 else "tense" if net_delta < -(stake // 2) else "neutral",
                financial_note=f"{actor_role}下注 ${stake}，返还 ${payout}，赌税 ${tax}，净变化 ${net_delta}。",
                gray_trade=True,
                gray_trade_type="地下赌博",
                gray_trade_severity=2 if payout else 3,
            )
        )

    def _pick_casino_relation_target(self, actor: Agent) -> Agent | None:
        same_area = [
            other
            for other in self.state.agents
            if other.id != actor.id and not other.is_resting and other.current_location == actor.current_location
        ]
        if same_area:
            return self.random.choice(same_area)
        others = [other for other in self.state.agents if other.id != actor.id and not other.is_resting]
        if not others:
            return None
        return self.random.choice(others)

    def _apply_casino_social_effects(self, actor: Agent, *, stake: int, net_delta: int) -> None:
        target = self._pick_casino_relation_target(actor)
        if net_delta >= 0:
            actor.consumption_desire = self._bounded(actor.consumption_desire + min(8, max(2, net_delta // 60)))
            actor.life_satisfaction = self._bounded(actor.life_satisfaction + min(6, 1 + net_delta // 120))
            actor.state.mood = self._bounded(actor.state.mood + min(5, 1 + net_delta // 140))
        else:
            actor.state.stress = self._bounded(actor.state.stress + min(6, max(1, abs(net_delta) // 120)))
            actor.consumption_desire = self._bounded(actor.consumption_desire - min(4, max(1, abs(net_delta) // 180)))
        if target is None:
            return
        if net_delta <= -max(90, stake // 2):
            actor.current_bubble = self.random.choice(["别碰我。", "今晚真晦气。", "谁都别来烦我。"])
            target.current_bubble = self.random.choice(["你先冷静。", "别把火撒我这。"])
            self._adjust_relation(actor, target, -3, "在后巷地下赌场输钱后把火气带到了人身上")
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{actor.name} 在赌场输钱后和 {target.name} 呛起来",
                    summary=f"{actor.name} 刚在后巷地下赌场输了 ${abs(net_delta)} 左右，火气没压住，和 {target.name} 顶了几句。",
                    slot=self.state.time_slot,
                    category="general",
                ),
            )
            self.state.events = self.state.events[:8]
            return
        if net_delta >= max(140, stake):
            actor.current_bubble = self.random.choice(["今晚手气在我这。", "这把真让我吃到了。", "后巷今晚认我。"])
            target.current_bubble = self.random.choice(["你别太飘。", "见好就收。"])
            self._adjust_relation(actor, target, -1, "在后巷地下赌场赢大钱后忍不住当面炫耀")
            post = FeedPost(
                id=f"feed-{uuid4().hex[:8]}",
                author_type="agent",
                author_id=actor.id,
                author_name=actor.name,
                day=self.state.day,
                time_slot=self.state.time_slot,
                category="gossip",
                content=self._clean_feed_text(self._casino_brag_post(actor, stake=stake, net_delta=net_delta)),
                topic_tags=["后巷赌局", "炫耀", "牌桌"],
                desire_tags=["赢了想让人看见", "赌桌翻身"],
                likes=8 + min(18, net_delta // 35),
                views=80 + min(240, net_delta),
                summary="有人在微博上炫耀后巷赌局的赢面。",
                impacts=["影响团队氛围", "影响监管注意力"],
            )
            post.credibility = self._feed_credibility_for_post(post)
            post.heat = self._compute_feed_heat(post)
            self._append_feed_post(post, remember=True, apply_impacts=True)

    def _casino_brag_post(self, actor: Agent, *, stake: int, net_delta: int) -> str:
        lines = {
            "lin": f"后巷这把我拿了 ${net_delta}。别神化手气，我只是在别人上头的时候收手更快。",
            "mika": f"刚从后巷出来，居然真让我带走了 ${net_delta}。现在心脏还在跳，先别劝我冷静。",
            "jo": f"后巷这把净进 ${net_delta}。别讲运气，谁先乱，钱就往谁口袋里流。",
            "rae": f"今晚后巷意外赢了 ${net_delta}。开心归开心，但旁边真有人输得脸都白了。",
            "kai": f"后巷这把拿到 ${net_delta}。这阵风先吹到我这边了，就这么简单。",
        }
        return lines.get(actor.id, f"刚从后巷地下赌场拿到 ${net_delta}，今晚牌桌真偏我。")

    def _publish_tourist_casino_post(self, tourist: TouristAgent, *, stake: int, net_delta: int, outcome_text: str) -> None:
        tier_style = {
            "regular": f"后巷那个赌桌居然真有人敢压，我刚试了 ${stake}，{outcome_text}。这地方比白天看起来野多了。",
            "repeat": f"上次来还没这么吵，这次后巷赌局已经传开了。我刚压了 ${stake}，{outcome_text}，难怪大家都爱围着看。",
            "vip": f"后巷赌局真不是摆设。我刚下了 ${stake}，{outcome_text}。花钱这事，至少今晚算有点刺激。",
            "buyer": f"本来在看房，结果被后巷赌局拽过去了。我压了 ${stake}，{outcome_text}，现在更想知道这里到底是什么地方。",
        }
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="tourist",
            author_id=tourist.id,
            author_name=tourist.name,
            day=self.state.day,
            time_slot=self.state.time_slot,
            category="gossip" if abs(net_delta) >= 30 else "tourism",
            content=self._clean_feed_text(tier_style.get(tourist.visitor_tier, tier_style["regular"])),
            topic_tags=["后巷赌局", "地下赌场", "游客见闻"],
            desire_tags=["看热闹", "试试手气", "逛到真事"],
            likes=6 + min(12, abs(net_delta) // 18),
            views=60 + min(180, stake * 2),
            summary="游客把后巷赌局发到了小镇微博上。",
            impacts=["影响游客讨论", "影响监管注意力", "影响团队氛围"],
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        self._append_feed_post(post, remember=True, apply_impacts=True)

    def create_player_feed_post(
        self,
        content: str,
        category: str = "daily",
        reply_to_post_id: str | None = None,
        quote_post_id: str | None = None,
        mood: str = "neutral",
    ) -> WorldState:
        cleaned = (content or "").strip()
        if not cleaned:
            raise ValueError("先写一句你想发的内容。")
        reply_to = self._find_feed_post(reply_to_post_id) if reply_to_post_id else None
        quote_to = self._find_feed_post(quote_post_id) if quote_post_id else None
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="player",
            author_id=self.state.player.id,
            author_name=self.state.player.name,
            day=self.state.day,
            time_slot=self.state.time_slot,
            category=category if category in {"daily", "mood", "research", "market", "property", "tourism", "policy", "gossip"} else "daily",
            mood=self._normalize_feed_mood(mood),
            content=cleaned[:160],
            topic_tags=self._feed_topic_tags(cleaned, category),
            desire_tags=[self._player_desire_label(cleaned)],
            reply_to_post_id=reply_to.id if reply_to else None,
            quote_post_id=quote_to.id if quote_to else None,
            likes=max(0, min(18, 2 + self.state.player.reputation_score // 16)),
            views=max(12, 30 + self.state.day % 17 + self.state.player.reputation_score),
            summary=f"你发了一条关于“{self._feed_title_topic(cleaned, category)}”的微博。",
            impacts=self._feed_impacts_for_category(category),
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        self._append_feed_post(post, remember=True, apply_impacts=True)
        self.state.player.daily_actions.append(f"feed:{category}")
        if reply_to and reply_to.author_type == "agent" and reply_to.author_id != self.state.player.id:
            agent = self.get_agent(reply_to.author_id)
            self._adjust_player_relation(agent, 1, "你在小镇微博上公开接了对方的话。", observer=True)
        self._log("feed_post", author_type="player", author_name=self.state.player.name, category=post.category, content=post.content, heat=post.heat)
        return self.state

    def react_to_feed_post(self, post_id: str, action: str) -> WorldState:
        post = self._find_feed_post(post_id)
        if post is None:
            raise KeyError(f"未找到微博帖子：{post_id}")
        if action not in {"like", "repost", "watch"}:
            raise ValueError("不支持的微博互动动作。")
        if action == "watch":
            post.views = min(9999, post.views + 4)
        elif action == "like":
            post.views = min(9999, post.views + 2)
            post.likes = min(999, post.likes + 1)
            if post.author_type == "agent":
                agent = self.get_agent(post.author_id)
                self._adjust_player_relation(agent, 1, "你在小镇微博上给对方点了赞。", observer=True)
        elif action == "repost":
            post.views = min(9999, post.views + 9)
            post.likes = min(999, post.likes + 2)
            post.reposts = min(999, post.reposts + 1)
            self._apply_player_intervention_cost("feed_repost", amount=1)
            tone = self._feed_tone(post.content)
            if post.category == "market":
                self.state.market.sentiment = self._bounded(self.state.market.sentiment + tone * 2)
            elif post.category == "tourism":
                self.state.tourism.latest_signal = f"小镇微博转发：{post.content[:24]}"
                self.state.tourism.daily_messages_count += 1
            elif post.category in {"mood", "gossip"}:
                self.state.lab.team_atmosphere = self._bounded(self.state.lab.team_atmosphere + tone)
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        self._log("feed_reaction", action=action, post_id=post.id, author_name=post.author_name, category=post.category, heat=post.heat)
        return self.state

    def speak_to_agent(self, agent_id: str, player_text: str) -> DialogueOutcome:
        if self.has_tourist(agent_id):
            return self.speak_to_tourist(agent_id, player_text, observer=False)
        return self.social_engine.speak_to_agent(agent_id, player_text)

    def commit_external_dialogue(self, agent_id: str, dialogue: DialogueOutcome, player_text: str) -> DialogueOutcome:
        return self.social_engine.commit_external_dialogue(agent_id, dialogue, player_text)

    def speak_to_tourist(self, tourist_id: str, player_text: str, observer: bool = False) -> DialogueOutcome:
        tourist = self._find_tourist(tourist_id)
        cleaned = player_text.strip()
        if not cleaned:
            raise ValueError("先输入一句你想说的话。")
        dialogue_topic = self._dialogue_topic_from_player_text(cleaned, tourist.favorite_topic or "旅途见闻")
        line = self._tourist_reply_line(tourist, cleaned)
        mood_delta = 2 if any(token in cleaned for token in ["欢迎", "慢慢逛", "需要帮忙", "休息", "坐坐"]) else 1
        tourist.mood = self._bounded(tourist.mood + mood_delta)
        tourist.current_bubble = line
        tourist.current_activity = f"刚和你聊了“{dialogue_topic or '这地方'}”，看起来还想再逛逛。"
        tourist.brief_note = f"对你刚才提到的“{dialogue_topic[:16]}”有印象，今天会更愿意在这里花钱和停留。"
        self._remember_tourist(tourist, f"你刚和玩家聊了“{cleaned[:16]}”，觉得这里还值得继续逛。", 2)
        self._remember_tourist(tourist, f"你刚回了一句“{line[:20]}”，心情比刚才更松一点。", 1)
        if observer:
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + 1)
        else:
            self.state.player.reputation_score = self._bounded(self.state.player.reputation_score + 1)
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + 1)
        outcome = DialogueOutcome(
            agent_id=tourist.id,
            agent_name=tourist.name,
            player_text=cleaned,
            line=line,
            topic=dialogue_topic,
            bubble_text=line,
            effects=["游客心情 +1", "小镇人气 +1"],
        )
        self.state.latest_dialogue = outcome
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="player_dialogue",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=["player", tourist.id],
                participant_names=[self.state.player.name, tourist.name],
                topic=dialogue_topic,
                summary=self._natural_player_tourist_summary(tourist.name, dialogue_topic),
                key_point=self._natural_player_tourist_key_point(tourist.name, dialogue_topic),
                transcript=[f"你：{cleaned}", f"{tourist.name}：{line}"],
                desire_labels={self.state.player.name: self._player_desire_label(cleaned), tourist.name: "想把这趟行程过得舒服一点"},
                mood="warm",
            )
        )
        self._append_finance_record(
            actor_id=tourist.id,
            actor_name=tourist.name,
            category="tourism",
            action="chat",
            summary=f"{tourist.name} 刚和你聊了一会儿，接下来更可能去旅馆或集市消费。",
            amount=0,
            asset_name=self.state.tourism.market_name,
            counterparty=self.state.player.name,
        )
        self._log(
            "tourist_player_dialogue",
            tourist={"id": tourist.id, "name": tourist.name, "archetype": tourist.archetype},
            dialogue={"player_text": cleaned, "reply": line},
        )
        return outcome

    def get_agent(self, agent_id: str) -> Agent:
        return self._find_agent(agent_id)

    def has_tourist(self, tourist_id: str) -> bool:
        return any(tourist.id == tourist_id for tourist in self.state.tourists)

    def get_tourist(self, tourist_id: str) -> TouristAgent:
        return self._find_tourist(tourist_id)

    def inject_event(self, event: LabEvent) -> WorldState:
        return self._ingest_event(event, player_injected=True)

    def schedule_news_timeline_item(self, event: LabEvent, query: str, theme: str, scheduled_day: int, scheduled_time_slot: TimeSlot) -> None:
        self.state.news_timeline.insert(
            0,
            NewsTimelineItem(
                id=f"timeline-{uuid4().hex[:8]}",
                title=event.title,
                summary=event.summary,
                source=event.source or "Brave Search",
                query=query,
                theme=theme,
                category=event.category,
                scheduled_day=scheduled_day,
                scheduled_time_slot=scheduled_time_slot,
                mood=self._timeline_mood_for_event(event),
                tone_hint=event.tone_hint,
                market_target=event.market_target,
                market_strength=event.market_strength,
                impacts=dict(event.impacts),
            ),
        )
        self.state.news_timeline = sorted(
            self.state.news_timeline,
            key=lambda item: (item.status != "scheduled", item.scheduled_day, SLOT_SEQUENCE.index(item.scheduled_time_slot)),
        )[:24]

    def build_timeline_event(self, item: NewsTimelineItem) -> LabEvent:
        return LabEvent(
            id=f"event-{uuid4().hex[:8]}",
            category=item.category,
            title=item.title,
            summary=item.summary,
            source=item.source,
            time_slot=self.state.time_slot,
            impacts=dict(item.impacts),
            participants=[],
            tone_hint=item.tone_hint if item.tone_hint else (1 if self.random.random() < 0.5 else -1),
            market_target=item.market_target,
            market_strength=max(4, item.market_strength),
        )

    def slot_after(self, offset: int = 1) -> tuple[int, TimeSlot]:
        base_index = SLOT_SEQUENCE.index(self.state.time_slot)
        total = base_index + max(1, offset)
        day_delta, slot_index = divmod(total, len(SLOT_SEQUENCE))
        return self.state.day + day_delta, SLOT_SEQUENCE[slot_index]

    def _slot_sort_key(self, day: int, slot: TimeSlot) -> tuple[int, int]:
        return day, SLOT_SEQUENCE.index(slot)

    def _ingest_event(self, event: LabEvent, player_injected: bool) -> WorldState:
        self.state.events.insert(0, event)
        self.state.events = self.state.events[:8]
        if player_injected:
            self.state.player.injected_topics.insert(0, event.title)
            self.state.player.injected_topics = self.state.player.injected_topics[:8]
            self._apply_player_intervention_cost("macro_signal", amount=1)
        self.state.lab.external_sensitivity = min(100, self.state.lab.external_sensitivity + 8)
        self.state.lab.collective_reasoning = min(100, self.state.lab.collective_reasoning + event.impacts.get("collective_reasoning", 0))
        self.state.lab.research_progress = min(100, self.state.lab.research_progress + event.impacts.get("research_progress", 0))
        if event.tone_hint >= 2:
            self.state.lab.reputation = self._bounded(self.state.lab.reputation + 2)
        elif event.tone_hint <= -2:
            self.state.lab.reputation = self._bounded(self.state.lab.reputation - 1)
        self._advance_geoai_progress(event.impacts.get("geoai_progress", 0), reason=event.title)
        self.social_engine.handle_event(event)
        self.market_engine.handle_event(event)
        apply_task_progress(self.state.tasks, "news")
        self._refresh_presence()
        self._log(
            "external_event",
            event={
                "id": event.id,
                "title": event.title,
                "category": event.category,
                "summary": event.summary,
                "source": event.source,
            },
        )
        return self.state

    def trigger_scheduled_news(self) -> None:
        for item in self.state.news_timeline:
            if item.status != "scheduled":
                continue
            if self._slot_sort_key(item.scheduled_day, item.scheduled_time_slot) < self._slot_sort_key(self.state.day, self.state.time_slot):
                item.status = "expired"
                continue
            if item.scheduled_day != self.state.day or item.scheduled_time_slot != self.state.time_slot:
                continue
            event = self.build_timeline_event(item)
            self._ingest_event(event, player_injected=False)
            self._seed_feed_from_external_event(event, item.theme)
            item.status = "triggered"
            item.triggered_day = self.state.day
            item.triggered_time_slot = self.state.time_slot

    def advance_for_reflection(self, reason: str) -> WorldState:
        self.state.events.insert(
            0,
            build_internal_event(
                title="实验室短暂停顿",
                summary=f"团队为了“{reason}”暂停了一会儿，准备进入下一个时段。",
                slot=self.state.time_slot,
            ),
        )
        self.state.events = self.state.events[:8]
        self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + 1)
        for agent in self.state.agents:
            agent.state.stress = max(0, agent.state.stress - 2)
            agent.state.energy = min(100, agent.state.energy + 1)
        apply_task_progress(self.state.tasks, "rest")
        self._advance_world()
        self._log("advance_reflection", reason=reason)
        return self.state

    def simulate_world(self) -> WorldState:
        self.market_engine.prepare_view()
        self.social_engine.prepare_view()
        self.lifestyle_engine.prepare_view()
        self.market_engine.run_intraday_tick()
        self._maybe_generate_system_news()
        self._maybe_trigger_random_lab_event()
        self._maybe_trigger_regulatory_audit()
        self._move_agents_autonomously()
        self._trigger_work_activity()
        self._trigger_bank_activity()
        self._run_tourism_activity()
        self._tick_business_competition()
        self._trigger_casino_activity()
        self._trigger_gray_market_activity()
        self.lifestyle_engine.run_tick()
        self._trigger_property_market_activity()
        self.social_engine.run_tick()
        self._maybe_generate_feed_posts()
        self._spread_feed_posts()
        self._advance_gray_cases(daily_roll=False)
        self._settle_due_loans()
        self._settle_due_bank_loans()
        self._soft_shift_player_pressure()
        self._refresh_tasks()
        self._refresh_memory_streams()
        self._refresh_government_agent_state()
        self._log("world_simulation_tick")
        return self.state

    def _maybe_generate_feed_posts(self) -> None:
        if getattr(self.state, "feed_timeline", None) is None:
            self.state.feed_timeline = []
        current_slot_posts = [post for post in self.state.feed_timeline if post.day == self.state.day and post.time_slot == self.state.time_slot]
        latest_event = self.state.events[0] if self.state.events else None
        scheduled_social = next(
            (
                item
                for item in self.state.news_timeline
                if item.status == "scheduled" and str(item.theme).startswith("社会热点")
            ),
            None,
        )
        recent_hot_gossip = any(post.category == "gossip" and post.heat >= 16 for post in self.state.feed_timeline[:10])
        topic_buzz = bool(
            latest_event
            and latest_event.category in {"general", "market"}
            and (latest_event.source in {"Brave Search", "系统新闻台"} or "热点" in latest_event.title)
        )
        social_buzz = (
            topic_buzz
            or recent_hot_gossip
            or bool(self.state.tourism.latest_signal and "微博热议" in self.state.tourism.latest_signal)
            or scheduled_social is not None
        )
        slot_cap = 5 if social_buzz else 3
        if len(current_slot_posts) >= slot_cap:
            return
        hot_post = self._pick_hot_feed_post()
        candidates: list[FeedPost] = []
        recent_feed = self.state.feed_timeline[:8]
        recent_agent_posts = sum(1 for post in recent_feed if post.author_type == "agent")
        recent_government_posts = sum(1 for post in recent_feed if post.author_type == "government")
        if scheduled_social is not None and not any(
            post.author_type == "system" and "社会热点" in (post.topic_tags or []) for post in recent_feed
        ):
            candidates.append(self._build_scheduled_social_preview_post(scheduled_social))
        if hot_post is not None and self.random.random() < 0.28 and self._feed_thread_depth(hot_post.id) < 3:
            agent_pool = [agent for agent in self.state.agents if agent.id != hot_post.author_id] or self.state.agents
            agent = self.random.choice(agent_pool)
            if not self._has_recent_author_reply_to_target(agent.id, hot_post.id):
                candidates.append(self._build_agent_feed_reply(agent, hot_post))
        elif self.random.random() < 0.76 or recent_agent_posts == 0:
            agent = self.random.choice(self.state.agents)
            candidates.append(self._build_agent_feed_post(agent, latest_event))
        if self.state.tourists and self.random.random() < 0.32:
            tourist_pool = [tourist for tourist in self.state.tourists if tourist.id != (hot_post.author_id if hot_post else "")] or self.state.tourists
            tourist = self.random.choice(tourist_pool)
            if hot_post is not None and self.random.random() < 0.22 and self._feed_thread_depth(hot_post.id) < 3:
                candidates.append(self._build_tourist_feed_reply(tourist, hot_post))
            else:
                candidates.append(self._build_tourist_feed_post(tourist, latest_event))
        if social_buzz and self.random.random() < 0.78:
            buzz_pool = [agent for agent in self.state.agents if hot_post is None or agent.id != hot_post.author_id] or self.state.agents
            candidates.append(self._build_agent_feed_post(self.random.choice(buzz_pool), latest_event))
            if self.state.tourists and self.random.random() < 0.55:
                candidates.append(self._build_tourist_feed_post(self.random.choice(self.state.tourists), latest_event))
            if hot_post is not None and self.random.random() < 0.24 and self._feed_thread_depth(hot_post.id) < 3:
                reactive_pool = [agent for agent in self.state.agents if agent.id != hot_post.author_id] or self.state.agents
                reactive_agent = self.random.choice(reactive_pool)
                if not self._has_recent_author_reply_to_target(reactive_agent.id, hot_post.id):
                    candidates.append(self._build_agent_feed_reply(reactive_agent, hot_post))
            if hot_post is not None and self.random.random() < 0.14 and self._feed_thread_depth(hot_post.id) < 2:
                second_wave_pool = [agent for agent in self.state.agents if agent.id not in {hot_post.author_id}] or self.state.agents
                second_agent = self.random.choice(second_wave_pool)
                if not self._has_recent_author_reply_to_target(second_agent.id, hot_post.id):
                    candidates.append(self._build_agent_feed_reply(second_agent, hot_post))
        if self.random.random() < 0.2 or (self.state.time_slot in {"morning", "evening"} and recent_government_posts == 0):
            if hot_post is not None and hot_post.author_type != "government" and self.random.random() < 0.48:
                candidates.append(self._build_government_feed_reply(hot_post))
            else:
                candidates.append(self._build_government_feed_post(latest_event))
        for post in candidates[: max(0, slot_cap - len(current_slot_posts))]:
            inserted = self._append_feed_post(post, remember=True, apply_impacts=True)
            if inserted:
                self._log("feed_post", author_type=post.author_type, author_name=post.author_name, category=post.category, content=post.content, heat=post.heat)

    def _build_agent_feed_post(self, agent: Agent, latest_event: LabEvent | None) -> FeedPost:
        category = self._agent_feed_category(agent, latest_event)
        content, tags = self._agent_feed_content(agent, category, latest_event)
        desire_code, _ = dominant_desire_for_agent(self.state, agent)
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="agent",
            author_id=agent.id,
            author_name=agent.name,
            day=self.state.day,
            time_slot=self.state.time_slot,
            category=category,
            content=self._clean_feed_text(content),
            topic_tags=tags,
            desire_tags=[DESIRE_LABELS.get(desire_code, desire_code)],
            likes=max(0, min(24, 3 + max(0, agent.relations.get("player", 0)) // 12 + self.random.randint(0, 4))),
            views=max(18, 24 + agent.cash // 120 + self.random.randint(0, 25)),
            summary=f"{agent.name} 把这轮最在意的事发成了一条公开帖子。",
            impacts=self._feed_impacts_for_category(category),
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _build_agent_feed_reply(self, agent: Agent, target_post: FeedPost) -> FeedPost:
        if target_post.author_id == agent.id:
            return self._build_agent_feed_post(agent, self.state.events[0] if self.state.events else None)
        desire_code, _ = dominant_desire_for_agent(self.state, agent)
        topic = self._feed_discussion_topic(target_post)
        style_seed = int(hashlib.sha1(f"{agent.id}-{target_post.id}-{self.state.day}".encode("utf-8")).hexdigest()[:6], 16)
        softener = (agent.speech_habits or [""])[0] if agent.speech_habits else ""
        content = self._agent_feed_reply_content(agent, target_post.author_name, topic, desire_code, style_seed, softener)
        location_label = ROOM_LABELS.get(agent.current_location, agent.current_location)
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="agent",
            author_id=agent.id,
            author_name=agent.name,
            day=self.state.day,
            time_slot=self.state.time_slot,
            category=target_post.category if target_post.category in {"research", "market", "property", "tourism", "policy", "gossip", "mood"} else "daily",
            content=self._clean_feed_text(content),
            topic_tags=list(dict.fromkeys((target_post.topic_tags or [])[:3] + [location_label])),
            desire_tags=[DESIRE_LABELS.get(desire_code, desire_code)],
            reply_to_post_id=target_post.id,
            likes=max(0, min(20, 2 + agent.state.focus // 22 + self.random.randint(0, 4))),
            views=max(18, 22 + self.random.randint(0, 22)),
            summary=f"{agent.name} 在公开场里接了 {target_post.author_name} 的话。",
            impacts=self._feed_impacts_for_category(target_post.category),
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _build_tourist_feed_post(self, tourist: TouristAgent, latest_event: LabEvent | None) -> FeedPost:
        is_social_buzz = bool(
            latest_event
            and latest_event.category == "general"
            and (latest_event.source in {"Brave Search", "系统新闻台"} or "热点" in latest_event.title or "传闻" in latest_event.title)
        )
        category = "gossip" if is_social_buzz else ("tourism" if tourist.visitor_tier != "buyer" else "property")
        base_text = tourist.brief_note or tourist.current_activity or "这里比我预想得更有意思。"
        style_seed = int(hashlib.sha1(f"{tourist.id}-{self.state.day}-{self.state.time_slot}-{tourist.visitor_tier}".encode("utf-8")).hexdigest()[:6], 16)
        angle = style_seed % 3
        location_label = ROOM_LABELS.get(tourist.current_location, tourist.current_location)
        if category == "gossip":
            topic = (latest_event.title if latest_event is not None else tourist.favorite_topic or "这条小镇传闻")[:24]
            options = [
                f"今天到处都在聊“{topic}”。我本来只想看看热闹，结果听着听着，发现大家真正怕的还是日子会越来越贵、越来越挤。",
                f"游客视角说一句：“{topic}”这种传闻一热，气氛马上就会变。有人觉得更有戏，有人已经开始担心这里会不会被搞得太满。",
                f"我今天在旅馆和集市听了好几轮“{topic}”，最明显的感觉是：同一件事，对想赚钱的人和想过安稳日子的人完全不是一个意思。",
            ]
            content = options[angle]
        elif tourist.visitor_tier == "vip":
            options = [
                f"今天在{location_label}转了一圈，我本来挺挑的，结果还真被这里留住了。不是因为它多贵，而是它居然有点真生活。",
                "我花钱向来认感觉。这里最难得的是，不会让人觉得自己只是被当成一笔消费。",
                "说实话，很多地方只会端着热闹给你看，这里倒是有点松弛，像能真的住人。",
            ]
            content = options[angle]
        elif tourist.visitor_tier == "buyer":
            options = [
                "今天看房时心里有点打鼓。价格当然重要，但我现在更在意的是，住进来以后会不会天天都觉得累。",
                "我对这里开始认真了，所以反而更谨慎。一个地方如果只适合投资，不适合生活，最后会把自己掏空。",
                "现在最想比较的不是挂牌数字，而是这里能不能让我把日子过顺。房子要是只会涨，不会让人想留下，其实也没劲。",
            ]
            content = options[angle]
        elif tourist.visitor_tier == "repeat":
            options = [
                "第二次来还是觉得这里有劲儿，这就不容易了。回头客最怕第一次像惊喜，第二次只剩套路。",
                "能让我再回来一次，通常不是因为更热闹，而是因为第一次没看清的层次第二次开始冒出来了。",
                "回访最大的好处，就是能分清这地方是真的有生活，还是只会第一次哄你开心。",
            ]
            content = options[angle]
        else:
            options = [
                f"随手记一下：这里比我想的更像有人在过日子，不只是摆给游客看。今天最有意思的是{(tourist.favorite_topic or '集市和旅馆周边')[:14]}。",
                "第一次来，本来只想看热闹，结果反而记住了人怎么停下来聊天、干活、互相看一眼。",
                "游客其实很容易被漂亮景观哄住，但这里偶尔会冒出一点真的生活感，这点挺戳人的。",
            ]
            content = options[angle]
        tags = [location_label, self._tourist_tier_label(tourist.visitor_tier)]
        if category == "gossip":
            tags.append("社会热点")
        if latest_event is not None and latest_event.category in {"market", "general"}:
            tags.append(self._localized_text(latest_event.category))
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="tourist",
            author_id=tourist.id,
            author_name=tourist.name,
            day=self.state.day,
            time_slot=self.state.time_slot,
            category=category,
            content=self._clean_feed_text(content),
            topic_tags=tags,
            desire_tags=[tourist.favorite_topic or "到处看看"],
            likes=max(0, min(18, 1 + tourist.message_influence * 3 + self.random.randint(0, 4))),
            views=max(16, 18 + tourist.message_influence * 12 + self.random.randint(0, 18)),
            summary=f"{tourist.name} 发了一条游客动态。",
            impacts=self._feed_impacts_for_category(category),
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _build_tourist_feed_reply(self, tourist: TouristAgent, target_post: FeedPost) -> FeedPost:
        if target_post.author_id == tourist.id:
            return self._build_tourist_feed_post(tourist, self.state.events[0] if self.state.events else None)
        style_seed = int(hashlib.sha1(f"{tourist.id}-{target_post.id}-{self.state.day}".encode("utf-8")).hexdigest()[:6], 16)
        location_label = ROOM_LABELS.get(tourist.current_location, tourist.current_location)
        if target_post.category == "gossip":
            options = [
                f"{tourist.name} 回复 {target_post.author_name}：我先不管真假，反正这种传闻一多，游客会先犹豫，还会不会来、还愿不愿意花钱。",
                f"{tourist.name} 回复 {target_post.author_name}：这类话一热起来，外面的人第一反应不是分析，是先觉得这里到底还舒不舒服。",
                f"{tourist.name} 回复 {target_post.author_name}：我只说游客视角，这种风声会直接改大家的脚步，很多人会先观望。",
            ]
        else:
            options = [
                f"{tourist.name} 回复 {target_post.author_name}：你这话我能懂。游客最后不是记逻辑，是记这里值不值得多待半天、多花一点钱。",
                f"{tourist.name} 回复 {target_post.author_name}：外面的人看这里，先看气氛顺不顺。感觉一拧巴，消费和停留都会往下掉。",
                f"{tourist.name} 回复 {target_post.author_name}：我同意一部分。游客很现实，舒服就留下，不舒服就走。",
            ]
        content = options[style_seed % len(options)]
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="tourist",
            author_id=tourist.id,
            author_name=tourist.name,
            day=self.state.day,
            time_slot=self.state.time_slot,
            category="gossip" if target_post.category == "gossip" else ("tourism" if target_post.category != "property" else "property"),
            content=self._clean_feed_text(content),
            topic_tags=list(dict.fromkeys((target_post.topic_tags or [])[:3] + [location_label])),
            desire_tags=[tourist.favorite_topic or "体验感"],
            reply_to_post_id=target_post.id,
            likes=max(0, min(14, 1 + tourist.message_influence * 2 + self.random.randint(0, 3))),
            views=max(12, 16 + tourist.message_influence * 10 + self.random.randint(0, 16)),
            summary=f"{tourist.name} 接了一条公开帖子。",
            impacts=self._feed_impacts_for_category("tourism"),
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _build_government_feed_post(self, latest_event: LabEvent | None) -> FeedPost:
        agenda = self.state.government.current_agenda or "维持财政与设施平衡"
        action = self.state.government.last_agent_action or "继续观察游客、税收和市场反馈"
        note = self.state.government.last_policy_note or "暂无新的额外说明"
        options = [
            f"【小镇运营通告】当前工作重心为“{agenda}”。最近已执行：{action}。后续安排将结合财政承受、维护成本与居民反馈继续推进。",
            f"【小镇运营通告】现阶段优先处理“{agenda}”。最近完成事项：{action}。有关新增动作，将在评估预算与公共服务需求后发布。",
            f"【小镇运营通告】当前仍围绕“{agenda}”展开。最新进展：{action}。补充说明：{note[:28]}。",
        ]
        style_seed = int(hashlib.sha1(f"{self.state.day}-{self.state.time_slot}-government".encode('utf-8')).hexdigest()[:6], 16)
        content = options[style_seed % len(options)]
        tags = ["财政", "监管", "公共服务"]
        if latest_event is not None:
            tags.append(latest_event.category)
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="government",
            author_id="government",
            author_name="小镇财政与监管局",
            day=self.state.day,
            time_slot=self.state.time_slot,
            category="policy",
            content=self._clean_feed_text(content),
            topic_tags=tags,
            desire_tags=["稳定运行"],
            likes=2 + max(0, self.state.government.enforcement_level // 18),
            views=32 + self.state.day % 21,
            summary="政府发布了一条公开运营说明。",
            impacts=["影响政府页", "进入政策观察"],
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _build_government_feed_reply(self, target_post: FeedPost) -> FeedPost:
        if target_post.author_type == "government":
            return self._build_government_feed_post(self.state.events[0] if self.state.events else None)
        style_seed = int(hashlib.sha1(f"gov-reply-{target_post.id}-{self.state.day}".encode("utf-8")).hexdigest()[:6], 16)
        options = [
            f"【政府回应】已收到 {target_post.author_name} 关于此事的公开意见。相关问题将结合预算、维护成本与实际影响一并评估，不会仅依据热度即时调整。",
            f"【政府回应】关于这类讨论，小镇不会回避。后续处理将以账目、维护责任和公共承受度为依据，并在必要时补充说明。",
            f"【政府回应】有关反映已记录。是否调整，将综合谁承担成本、谁受到影响以及整体公共收益后再作决定。",
        ]
        content = options[style_seed % len(options)]
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="government",
            author_id="government",
            author_name="小镇财政与监管局",
            day=self.state.day,
            time_slot=self.state.time_slot,
            category="policy",
            content=self._clean_feed_text(content),
            topic_tags=list(dict.fromkeys((target_post.topic_tags or [])[:3] + ["财政", "监管"])),
            desire_tags=["稳定运行"],
            reply_to_post_id=target_post.id,
            likes=3 + self.random.randint(0, 4),
            views=28 + self.state.day % 23,
            summary=f"政府回应了 {target_post.author_name} 的公开帖子。",
            impacts=["影响政府页", "进入政策观察", "进入晨报"],
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _agent_feed_category(self, agent: Agent, latest_event: LabEvent | None) -> str:
        if latest_event and latest_event.category == "market":
            return "market"
        if latest_event and latest_event.category == "general" and (latest_event.source in {"Brave Search", "系统新闻台"} or "热点" in latest_event.title):
            return "gossip"
        if any(post.category == "gossip" and post.heat >= 16 for post in self.state.feed_timeline[:8]) and self.random.random() < 0.36:
            return "gossip"
        if self.state.tourism.latest_signal and any(token in self.state.tourism.latest_signal for token in ["微博热议", "传闻", "热点"]) and self.random.random() < 0.28:
            return "gossip"
        if "GeoAI" in (agent.current_plan or "") or "GeoAI" in (agent.current_activity or ""):
            return "research"
        if "房" in (agent.current_activity or "") or agent.current_location == self.state.tourism.inn_location:
            return "property"
        if agent.state.stress >= 72 or agent.state.mood <= 35:
            return "mood"
        if agent.current_location in {self.state.tourism.market_location, self.state.tourism.inn_location}:
            return "tourism"
        return "daily"

    def _agent_feed_content(self, agent: Agent, category: str, latest_event: LabEvent | None) -> tuple[str, list[str]]:
        event_hint = latest_event.title if latest_event is not None else "今天还没出更大的外部波动"
        plan_hint = (agent.current_plan or agent.current_activity or event_hint).replace("“", "").replace("”", "")
        style_seed = int(hashlib.sha1(f"{agent.id}-{self.state.day}-{self.state.time_slot}-{category}".encode("utf-8")).hexdigest()[:6], 16)
        angle = style_seed % 3
        speech = (agent.speech_habits or [""])[0] if agent.speech_habits else ""
        desire_code, _ = dominant_desire_for_agent(self.state, agent)
        location_label = ROOM_LABELS.get(agent.current_location, agent.current_location)
        if category == "research":
            if agent.id == "lin":
                options = [
                    f"{speech}我今天一直卡在“{plan_hint[:26]}”上。最怕的不是没突破，是它看起来像突破，实际上只是把漏洞换了个地方藏。",
                    f"GeoAI 这轮最磨人的，是每个人都想快一点，但证据没到让我放心的那一步。我宁可慢，也不想以后回头补锅。",
                    f"我现在不敢被漂亮结果哄住。先把“{plan_hint[:24]}”一层层拆开，能证实多少算多少。",
                ]
            elif agent.id == "mika":
                options = [
                    f"{speech}我今天脑子里一直在打架：一边觉得“{plan_hint[:24]}”可能真能冒新路，一边又怕自己只是被兴奋感带跑了。",
                    f"研究这事最怪的地方，就是灵光一来，人会忍不住先爱上那个答案。我现在在努力把自己拽回来。",
                    f"如果这轮 GeoAI 真有点东西，那应该是那种越想越亮的感觉，不是第一眼特别炸、第二眼就空掉。",
                ]
            elif agent.id == "jo":
                options = [
                    f"{speech}别先庆祝。我今天盯着“{plan_hint[:24]}”看了半天，能不能落地还早，先把最硬那一步做完再说。",
                    f"研究不是拼谁先喊突破，是拼谁最后真把东西做出来。现在这轮还差得远，别被漂亮话抬走。",
                    f"我不怕难题，我怕半成品硬往前推。GeoAI 这块今天最该做的，是把假动作剔掉。",
                ]
            elif agent.id == "rae":
                options = [
                    f"{speech}今天研究组的情绪其实很满，大家都在“{plan_hint[:24]}”这里绷着。我更想先把那口气理顺，不然好结果也会被焦虑吃掉。",
                    f"研究推进当然重要，但如果每个人都被自己吓得发紧，再好的思路也会被磨掉。我今天最在意的是节奏。",
                    f"我其实能感觉到这轮是有东西的，只是越到这种时候越要照顾人，不然最后先散掉的是人心。",
                ]
            else:
                options = [
                    f"{speech}我今天闻到一点风向变了的味道，“{plan_hint[:24]}”这条线如果成，后面不只是研究，外面的资金和注意力都会跟着动。",
                    f"研究有时候像盘前信号，看着还不成形，但真转起来会很快。我现在反而不想说得太满，先盯第二步。",
                    f"我不觉得这轮只是技术问题。GeoAI 如果往前拱出来，后面整套话语权都会变，所以现在每一步都有人在看。",
                ]
            content = options[angle]
            tags = ["GeoAI", "研究讨论", location_label]
        elif category == "market":
            if agent.id == "lin":
                options = [
                    f"{speech}这轮盘面最危险的不是涨跌本身，而是太多人已经把“想象中的结果”当成事实先算进去了。",
                    f"表面像轮动，底下其实是预期在自我抬价。只要证据一松，情绪会掉得比价格更快。",
                    f"今天让我不舒服的，是“{plan_hint[:22]}”这种还没坐实的东西，已经被当成下注理由了。",
                ]
            elif agent.id == "mika":
                options = [
                    f"{speech}今天看盘像看一群人集体做梦，梦做得太齐的时候我反而会紧张，因为醒得也会很整齐。",
                    f"市场最会骗你的时候，就是它看起来特别有故事感的时候。我现在对这种顺滑上涨会本能地多看一眼。",
                    f"这轮钱在往哪里跑其实已经很有戏了，大家嘴上说理性，脚已经先冲过去了。",
                ]
            elif agent.id == "jo":
                options = [
                    f"{speech}别跟我讲情怀，盘面今天就是有人在抢先手。涨归涨，谁最后接盘、谁先变现，才是硬问题。",
                    f"市场里最不缺的就是说法。我只看一件事：钱是不是在真流动，还是只是在互相壮胆。",
                    f"今天这盘子不复杂，就是有人想快进。快进可以，别装成价值发现就行。",
                ]
            elif agent.id == "rae":
                options = [
                    f"{speech}这轮市场让我最在意的，其实是大家会不会被它带得越来越急。钱一快，人就容易把边界弄丢。",
                    f"盘面一热，很多人会把焦虑伪装成判断。我更担心这种气氛会顺着市场一路传到生活里。",
                    f"市场本身不是坏事，但如果每个人都开始被涨跌牵着走，后面最先伤到的还是日常。",
                ]
            else:
                options = [
                    f"{speech}这轮盘感挺强，风已经吹起来了。问题不是涨不涨，是谁闻到得早、谁跑得慢。",
                    f"市场现在像在找下一个能讲大故事的口子。你要说纯基本面，我不信；你要说没机会，我也不信。",
                    f"钱在找叙事，叙事也在找钱。今天这种味道一出来，后面就不会只是一根线的问题了。",
                ]
            content = options[angle]
            tags = ["市场", self.state.market.regime, self.state.market.rotation_leader]
        elif category == "property":
            if agent.id == "lin":
                options = [
                    f"{speech}住房这件事最难的不是价格，而是它会决定谁能把生活安下来，谁只能一直临时应付。",
                    f"地产在这里已经不是孤零零的资产了，它在改人的判断、消费和留下来的勇气。",
                    f"如果“{plan_hint[:22]}”继续往前顶，接下来变化的不只挂牌价，还有谁愿意把以后押在这里。",
                ]
            elif agent.id == "mika":
                options = [
                    f"{speech}看房这事最近特别像照镜子。大家挑的不是墙和窗，是自己想过成什么样。",
                    f"我越来越觉得住房会暴露一个地方的真性格：它到底是在欢迎人留下，还是只欢迎价格往上走。",
                    f"房子如果只剩涨幅，最后会把生活感磨掉。可没有生活感，这地方就又不值那个价了。",
                ]
            elif agent.id == "jo":
                options = [
                    f"{speech}地产别说虚的。房子够不够住、维护费扛不扛得住、谁最后买单，这几件事先算清楚。",
                    f"看房热起来以后，最容易被忽略的是后面的维护和周转。买得到不算本事，养得住才算。",
                    f"住房一旦被拿来只当筹码，后面最先掉队的是普通日子，不是报表。",
                ]
            elif agent.id == "rae":
                options = [
                    f"{speech}最近很多人的情绪都挂在住房上。住得稳不稳，会直接改掉一个人说话的方式和脸上的松弛。",
                    f"住房焦虑很少是单独来的，它后面总拖着消费、关系和安全感一起动。",
                    f"我现在更在意的是谁还能安心住下来，而不是谁又多赚了一点账面数字。",
                ]
            else:
                options = [
                    f"{speech}房这条线最近太敏感了。游客在看，资金在看，想留下来的人也在看，风往哪儿偏一下都很明显。",
                    f"地产一热，后面连游客停留和消费都会跟着重排。说白了，这已经不是单独的房价问题。",
                    f"我现在盯住房，不是因为它最浪漫，而是因为它最容易把别的信号都放大出来。",
                ]
            content = options[angle]
            tags = ["地产", "住房", location_label]
        elif category == "tourism":
            if agent.id == "lin":
                options = [
                    f"{speech}游客今天怎么走、在哪儿停、愿不愿意回头，比单纯的消费额更像真实信号。",
                    f"游客不会替我们写报告，但他们会用脚投票。停留时间和回访意愿，往往比热闹数字更诚实。",
                    f"如果只盯收入，很容易看漏真正的风向。游客最后是松下来还是赶着走，其实已经说明很多了。",
                ]
            elif agent.id == "mika":
                options = [
                    f"{speech}我今天最喜欢看游客发呆和突然停住的那几秒，那些不是流程，是一个地方真的把人留住了。",
                    f"游客最诚实的时刻不是掏钱，是他们忽然愿意把速度慢下来。我会一直记这种小反应。",
                    f"热闹不是难点，难的是让人觉得想多待一会儿。今天这点我反而觉得挺有戏。",
                ]
            elif agent.id == "jo":
                options = [
                    f"{speech}游客别只看人头，关键看停留、看复购、看最后有没有继续掏钱。数字得拆开看。",
                    f"今天游客流量还行，但我更关心他们花钱以后有没有觉得值。只来一趟的热闹没多大用。",
                    f"游客最怕被当成提款机。体验接不住，后面所有回头率都会掉。",
                ]
            elif agent.id == "rae":
                options = [
                    f"{speech}游客其实很敏感，他们会先感到这里的氛围稳不稳、累不累，然后才决定要不要多留一会儿。",
                    f"我今天反而更在意游客是不是舒服。体验感一差，人会很快收回来，连消费都带着防备。",
                    f"游客愿意留下，不只是因为热闹，也因为这里有没有让人放松一点点。",
                ]
            else:
                options = [
                    f"{speech}游客这条线像外面吹进来的风，今天往哪边偏一点，明天消费和看房都会跟着转。",
                    f"我越来越觉得游客不是客流，是风向标。谁先闻到那股变化，后面谁就先占位置。",
                    f"别小看游客停留，他们一犹豫、一回头，后面整个市场的节奏都可能跟着动。",
                ]
            content = options[angle]
            tags = ["游客", "消费", location_label]
        elif category == "mood":
            if agent.id == "lin":
                options = [
                    f"{speech}这轮状态是有点绷，但我更怕自己在发紧的时候做出过于自信的判断，所以先把节奏放稳。",
                    f"有时候最累的不是事情本身，而是你明知道证据还不够，周围却已经在等你开口。",
                    f"今天真正压着我的，是“{plan_hint[:24]}”到底还值不值得继续顶，不是表面那点热闹。",
                ]
            elif agent.id == "mika":
                options = [
                    f"{speech}我今天情绪有点飘，一会儿觉得什么都能做，一会儿又觉得自己是不是想太多了。",
                    f"最烦的不是忙，是脑子里同时冒出十条路，然后每一条都像在喊我立刻决定。",
                    f"我现在最想先让自己别乱冲。兴奋感很好，但要是被它牵着跑，后面会很空。",
                ]
            elif agent.id == "jo":
                options = [
                    f"{speech}状态紧是正常的，别演。事一堆、人一堆、钱一堆，谁都不可能一直松着。",
                    f"我今天烦的不是结果差，是有些问题明明该现在处理，却总有人想往后拖。",
                    f"这轮最耗人的，是每件事都像在催你马上定方向，连喘口气都像浪费时间。",
                ]
            elif agent.id == "rae":
                options = [
                    f"{speech}今天大家都绷得挺紧，我自己也没多轻松，只能提醒自己先别把呼吸弄丢。",
                    f"很多时候情绪不是突然爆的，是一整天都在忍。今天我能感觉到那个边缘已经很近了。",
                    f"我现在最想做的不是逞强，而是把自己和身边的人都先稳住一点。",
                ]
            else:
                options = [
                    f"{speech}我今天心里一直有点毛，像风要变但还没完全吹过来，这种时候人最容易做错动作。",
                    f"状态紧的时候，外面每个小信号都会被放大。我现在在强迫自己别被那些噪音拖走。",
                    f"今天压着我的不是单独一件事，是“接下来可能一起变”的那种感觉。",
                ]
            content = options[angle]
            tags = ["情绪", "节奏", location_label]
        elif category == "gossip":
            latest_title = (latest_event.title if latest_event is not None else plan_hint)[:24]
            if agent.id == "lin":
                options = [
                    f"{speech}外面的热点最容易把复杂问题压成一句口号。今天这条“{latest_title}”，我更想先看它到底戳中了什么真实处境。",
                    f"我对社会热点一直有点警惕，因为它们最会制造一种“大家都懂了”的错觉。真正难的是把情绪后面的结构讲清楚。",
                    f"这轮热点表面热，底下还是住房、收入和生活成本这些老问题。换个标题，并不代表矛盾就换了。",
                ]
            elif agent.id == "mika":
                options = [
                    f"{speech}我今天刷到“{latest_title}”时心里咯噔了一下。那种感觉像很多人突然同时把自己憋着的话说出来了。",
                    f"社会热点最有意思的地方，是它会把平时没人敢直说的情绪一下子拽到台面上。我会被这种时刻击中。",
                    f"有些热帖一看就知道会过去，但也有些会留在心里。“{latest_title}”就有点这种味道。",
                ]
            elif agent.id == "jo":
                options = [
                    f"{speech}外面那条“{latest_title}”我看了，情绪是情绪，现实还是现金、房租、工时和谁来买单。",
                    f"社会热点最容易把人带去站队，我更想先问一句：这事落到日常里，到底是谁更难了。",
                    f"热帖当然能吵，但吵完以后生活成本还在、账还得付。所以我对这种热度一向先打个折。",
                ]
            elif agent.id == "rae":
                options = [
                    f"{speech}我今天看到“{latest_title}”的时候，第一反应不是对错，而是很多人应该真的被这些日子压得很难开口。",
                    f"社会热点有时像一个公共出口，让平时说不出来的人终于能把累和委屈往外放一点。",
                    f"这类讨论最不该被轻轻带过，因为它后面常常站着一整片还没被照顾到的人。",
                ]
            else:
                options = [
                    f"{speech}这条“{latest_title}”能冲上来，说明外面的风已经在变了。谁先接住这股讨论，后面谁就更容易带节奏。",
                    f"社会热点我一般不会只当围观。它一热，游客、消费、住房、舆情都会跟着偏一点，这才是我盯它的原因。",
                    f"很多人把热帖当情绪，我更把它当信号。像“{latest_title}”这种，后面通常不只是一阵风。",
                ]
            content = options[angle]
            tags = ["社会热点", latest_title, location_label]
        else:
            if agent.id == "lin":
                options = [
                    f"{speech}今天最该记住的不是热闹，是“{plan_hint[:30]}”这种小地方。很多转向都是先从没人注意的角落开始。",
                    f"表面看今天没什么爆点，但我脑子里一直没放下“{plan_hint[:28]}”，它比大声说出来的东西更像真问题。",
                    f"如果今天只能留一句话，我会提醒自己先把“{plan_hint[:26]}”看透，再决定要不要表态。",
                ]
            elif agent.id == "mika":
                options = [
                    f"{speech}今天最戳我的不是结果，是“{plan_hint[:28]}”那一下让我突然意识到，很多事其实已经在悄悄偏了。",
                    f"我老觉得今天表面很平，底下却一直有小东西在冒泡。“{plan_hint[:26]}”就是那种泡。",
                    f"要给今天留一句话的话，大概是：别急着翻篇，有些细节还在等你回头看第二次。",
                ]
            elif agent.id == "jo":
                options = [
                    f"{speech}今天最值得记的不是谁说得响，是“{plan_hint[:28]}”这种会真落地的东西。别被表面节奏带走。",
                    f"看着没大事，不代表真没事。有些小动作要是现在不盯住，后面会很烦。",
                    f"今天给自己的话就一句：先把最实的那块做完，别被虚的东西拖着跑。",
                ]
            elif agent.id == "rae":
                options = [
                    f"{speech}今天我最想记住的是“{plan_hint[:28]}”，因为它不一定最显眼，但它最能说明大家现在是松还是紧。",
                    f"有些一天的气氛，会藏在很细的地方。我今天一直忘不掉“{plan_hint[:26]}”那一下。",
                    f"如果今天留一句话，我会写：先顾住人，再顾住后面的事。",
                ]
            else:
                options = [
                    f"{speech}今天最有味道的，不是明面上的热闹，而是“{plan_hint[:28]}”这种像信号一样冒出来的小动作。",
                    f"我脑子里一直挂着“{plan_hint[:26]}”，因为这种不起眼的东西，往往才是下一轮真正会动的地方。",
                    f"要说今天给自己的提醒，就是先盯信号、别急着下注，风还没吹透。",
                ]
            content = options[angle]
            tags = ["日常", location_label]
        if desire_code in DESIRE_LABELS:
            tags.append(DESIRE_LABELS[desire_code])
        return content[:160], [tag for tag in tags if tag]

    def _agent_feed_reply_content(
        self,
        agent: Agent,
        target_author: str,
        topic: str,
        desire_code: str,
        style_seed: int,
        softener: str,
    ) -> str:
        angle = style_seed % 3
        lead = f"{softener}，" if softener else ""
        if agent.id == "lin":
            options = [
                f"{lead}{target_author}，这话我听进去了，但我还是要追一句：证据在哪儿？别最后又靠猜。",
                f"{lead}我不急着站队。先把“{topic}”里最虚的那层剥掉，再看值不值得往前顶。",
                f"{lead}你这句不算错，但我最怕的是大家先被说服，后面才发现代价比想的重。",
            ]
        elif agent.id == "mika":
            options = [
                f"{lead}你这句一下戳到我了。我也觉得“{topic}”有点不对劲，就是说不上来哪儿别扭。",
                f"{lead}我不是抬杠，我只是老觉得这里面还藏了一层。现在就往前冲，我心里发毛。",
                f"{lead}你这么一说我更纠结了。它听起来是顺的，可我总觉得后面会有人被扯痛。",
            ]
        elif agent.id == "jo":
            options = [
                f"{lead}{target_author}，少绕。真上“{topic}”，钱谁掏，活谁干，锅谁背？先说清。",
                f"{lead}我不吃热度这一套。说得再漂亮，落地还是看谁先累死、谁先赔钱。",
                f"{lead}方向可以聊，但别空聊。你先把账摆出来，我再决定接不接这事。",
            ]
        elif agent.id == "rae":
            options = [
                f"{lead}我知道你在急，但“{topic}”真往下走，最先被压住的人是谁，我还是得问一句。",
                f"{lead}这话我不是不同意，我只是怕节奏一快，又有人没来得及开口就被推着走了。",
                f"{lead}你这句后劲挺大。我现在更想看的是，事情过去之后，大家会不会更累。",
            ]
        else:
            options = [
                f"{lead}你这句一出来，风向已经变了。后面谁会跟、谁会躲，我现在就想看这个。",
                f"{lead}这事不只是在吵，它已经像信号一样散开了。再热一点，游客和钱都会跟着动。",
                f"{lead}我先不说对错，我只说感觉：这话继续发酵，后面肯定有人要顺着它带节奏。",
            ]
        return options[angle][:160]

    def _feed_topic_tags(self, content: str, category: str) -> list[str]:
        tags = [category]
        if any(token in content for token in ["GeoAI", "空间智能", "研究"]):
            tags.append("GeoAI")
        if any(token in content for token in ["股票", "盘面", "市场", "现金流"]):
            tags.append("市场")
        if any(token in content for token in ["游客", "旅馆", "集市"]):
            tags.append("游客")
        if any(token in content for token in ["房", "住房", "看房", "地产"]):
            tags.append("地产")
        if any(token in content for token in ["税", "监管", "财政"]):
            tags.append("政策")
        return tags[:4]

    def _feed_impacts_for_category(self, category: str) -> list[str]:
        mapping = {
            "daily": ["影响关系"],
            "mood": ["影响关系", "进入记忆"],
            "research": ["影响研究", "进入记忆"],
            "market": ["影响市场", "进入记忆"],
            "property": ["影响地产", "影响游客"],
            "tourism": ["影响游客", "进入晨报"],
            "policy": ["影响政府页", "进入晨报"],
            "gossip": ["影响关系", "影响游客"],
        }
        return mapping.get(category, ["进入记忆"])

    def _feed_title_topic(self, content: str, category: str) -> str:
        if category == "research":
            return "研究进展"
        if category == "market":
            return "市场看法"
        if category == "tourism":
            return "游客动态"
        if category == "property":
            return "房产与生活"
        if category == "policy":
            return "政策变化"
        if category == "mood":
            return "心情和状态"
        if category == "gossip":
            return "社会热点"
        return content[:10] or "日常动态"

    def _feed_discussion_topic(self, post: FeedPost) -> str:
        raw_tags = [tag for tag in (post.topic_tags or []) if tag and tag not in {"daily", "mood", "research", "market", "property", "tourism", "policy", "gossip"}]
        for tag in raw_tags:
            if len(tag) <= 18 and not any(token in tag for token in ["foyer", "office", "compute", "data_wall", "meeting", "lounge"]):
                return tag
        if post.category == "gossip":
            return "这波社会热点"
        if post.category == "policy":
            return "政策变化"
        if post.category == "market":
            return "市场风向"
        if post.category == "tourism":
            return "游客体验"
        if post.category == "property":
            return "住房和房产"
        if post.category == "research":
            return "研究推进"
        if post.category == "mood":
            return "现在这股情绪"
        return "眼下这件事"

    def _feed_thread_depth(self, post_id: str) -> int:
        return sum(1 for post in self.state.feed_timeline[:40] if post.reply_to_post_id == post_id or post.quote_post_id == post_id)

    def _has_recent_author_reply_to_target(self, author_id: str, post_id: str) -> bool:
        return any(
            post.author_id == author_id and (post.reply_to_post_id == post_id or post.quote_post_id == post_id)
            for post in self.state.feed_timeline[:40]
        )

    def _clean_feed_text(self, content: str, limit: int = 160) -> str:
        text = " ".join((content or "").split()).strip()
        if len(text) <= limit:
            return text
        clipped = text[: limit - 1].rstrip(" ，,、：:")
        sentence_cut = max(clipped.rfind(mark) for mark in ["。", "！", "？", "；"])
        if sentence_cut >= 24:
            clipped = clipped[: sentence_cut + 1]
        else:
            space_cut = clipped.rfind(" ")
            if space_cut >= 24:
                clipped = clipped[:space_cut]
        return clipped.rstrip("，,、：:") + "。"

    def _compute_feed_heat(self, post: FeedPost) -> int:
        return max(1, int(post.likes * 1.5 + post.reposts * 3.2 + post.views / 11 + len(post.topic_tags) * 2 + post.credibility / 12))

    def _recompute_feed_timeline_heat(self) -> None:
        if not self.state.feed_timeline:
            return
        for post in self.state.feed_timeline:
            post.heat = self._compute_feed_heat(post)
        self.state.feed_timeline.sort(
            key=lambda item: (
                self._slot_sort_key(item.day, item.time_slot),
                item.heat,
                item.credibility,
            ),
            reverse=True,
        )
        self.state.feed_timeline = self.state.feed_timeline[:1000]

    def _feed_credibility_for_post(self, post: FeedPost) -> int:
        if post.author_type == "player":
            return max(12, min(96, 18 + int((self.state.player.reputation_score or 0) * 0.72) + int(self.state.lab.reputation * 0.08)))
        if post.author_type == "agent":
            agent = self.get_agent(post.author_id)
            return max(12, min(95, int((agent.credit_score + agent.state.focus + max(0, 100 - agent.state.stress)) / 3)))
        if post.author_type == "government":
            return max(40, min(98, 52 + self.state.government.public_service_level // 2))
        if post.author_type == "business":
            business = next((item for item in self.state.businesses or [] if item.id == post.author_id), None)
            if business is None:
                return 46
            base = 32 + business.reputation // 2 + business.quality_level // 5
            if business.strategy == "gray":
                base -= 6
            return max(24, min(90, base))
        if post.author_type == "tourist":
            tourist = next((item for item in self.state.tourists if item.id == post.author_id), None)
            if tourist is None:
                return 42
            base = 34 + tourist.message_influence * 8
            if tourist.visitor_tier == "vip":
                base += 12
            elif tourist.visitor_tier == "buyer":
                base += 8
            return max(18, min(86, base))
        return 50

    def _find_feed_post(self, post_id: str | None) -> FeedPost | None:
        if not post_id:
            return None
        return next((post for post in self.state.feed_timeline if post.id == post_id), None)

    def _pick_hot_feed_post(self) -> FeedPost | None:
        candidates = [post for post in self.state.feed_timeline[:12] if post.heat >= 14]
        if not candidates:
            return None
        return max(candidates, key=lambda item: item.heat + item.credibility // 6)

    def _feed_tone(self, content: str) -> int:
        positive = ["回暖", "利好", "稳定", "热闹", "顺", "改善", "值得", "支撑", "增长", "热"]
        negative = ["拖慢", "风险", "紧", "压", "问题", "放缓", "谨慎", "绷", "差", "跌"]
        score = sum(1 for token in positive if token in content) - sum(1 for token in negative if token in content)
        return max(-2, min(2, score))

    def _normalize_feed_mood(self, mood: str | None) -> str:
        candidate = (mood or "neutral").strip().lower()
        return candidate if candidate in {"neutral", "warm", "spark", "tense", "cool"} else "neutral"

    def _infer_feed_mood(self, category: str, content: str, tone_hint: int = 0) -> str:
        tone = tone_hint if tone_hint else self._feed_tone(content)
        if category in {"policy", "research"}:
            if tone < 0:
                return "tense"
            if tone > 0:
                return "spark" if category == "research" else "cool"
            return "cool"
        if category in {"market", "property"}:
            if tone > 0:
                return "spark"
            if tone < 0:
                return "tense"
            return "neutral"
        if category in {"tourism", "daily"}:
            if tone > 0:
                return "warm"
            if tone < 0:
                return "tense"
            return "neutral"
        if category == "mood":
            if tone > 0:
                return "warm"
            if tone < 0:
                return "tense"
            return "cool"
        if category == "gossip":
            if tone < 0:
                return "tense"
            if tone > 0:
                return "spark"
            return "warm"
        return "neutral"

    def _timeline_mood_for_event(self, event: LabEvent) -> str:
        tone = int(getattr(event, "tone_hint", 0) or 0)
        if event.category == "geoai":
            return "spark" if tone > 0 else "cool"
        if event.category == "market":
            if tone < 0:
                return "tense"
            if tone > 0:
                return "spark"
            return "cool" if (event.market_strength or 0) >= 4 else "neutral"
        if event.category == "general":
            if tone > 0:
                return "warm"
            if tone < 0:
                return "tense"
        return "neutral"

    def _spread_feed_posts(self) -> None:
        if not self.state.feed_timeline:
            return
        current_day, current_slot_index = self._slot_sort_key(self.state.day, self.state.time_slot)
        current_serial = current_day * len(SLOT_SEQUENCE) + current_slot_index
        for post in self.state.feed_timeline[:18]:
            post_day, post_slot_index = self._slot_sort_key(post.day, post.time_slot)
            post_serial = post_day * len(SLOT_SEQUENCE) + post_slot_index
            freshness = max(0, 6 - max(0, current_serial - post_serial))
            category_bias = {
                "market": 4,
                "policy": 3,
                "research": 3,
                "tourism": 2,
                "property": 2,
                "mood": 1,
                "daily": 1,
                "gossip": 2,
            }.get(post.category, 1)
            visibility_gain = max(1, freshness + category_bias + post.credibility // 25)
            reaction_gain = max(0, freshness // 2 + category_bias // 2)
            if post.author_type == "government":
                visibility_gain += 3
            if post.author_type == "tourist" and post.category == "tourism":
                visibility_gain += 2
            post.views = min(9999, post.views + visibility_gain + self.random.randint(0, 4))
            post.likes = min(999, post.likes + reaction_gain + self.random.randint(0, 2))
            if freshness >= 4 and self.random.random() < min(0.38, post.credibility / 240):
                post.reposts = min(999, post.reposts + 1)
        self._recompute_feed_timeline_heat()

    def _apply_feed_impacts(self, post: FeedPost) -> None:
        tone = self._feed_tone(post.content)
        credibility_weight = max(1, post.credibility // 25)
        heat_weight = max(1, post.heat // 20)
        if post.category == "market":
            market_shift = tone * credibility_weight * heat_weight
            if tone > 0:
                market_shift += 1
                self.state.player.consumption_desire = self._bounded(self.state.player.consumption_desire + 1)
                for agent in self.state.agents:
                    agent.consumption_desire = self._bounded(agent.consumption_desire + 1)
            self.state.market.sentiment = self._bounded(self.state.market.sentiment + market_shift)
        elif post.category == "tourism":
            self.state.tourism.latest_signal = f"微博舆情：{post.content[:24]}"
            self.state.tourism.daily_messages_count += 1
            if tone > 0:
                self.state.tourism.repeat_customers_total += 1
                self.state.market.sentiment = self._bounded(self.state.market.sentiment + 1)
                self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + 1)
                self.state.player.consumption_desire = self._bounded(self.state.player.consumption_desire + 2)
                for agent in self.state.agents:
                    agent.life_satisfaction = self._bounded(agent.life_satisfaction + 1)
                    agent.consumption_desire = self._bounded(agent.consumption_desire + 2)
        elif post.category == "research":
            self.state.lab.collective_reasoning = self._bounded(self.state.lab.collective_reasoning + max(1, heat_weight))
            self.state.lab.research_progress = self._bounded(self.state.lab.research_progress + max(0, tone + 1))
        elif post.category == "policy":
            self.state.government.known_signals.insert(0, post.content[:36])
            self.state.government.known_signals = self.state.government.known_signals[:10]
        elif post.category in {"mood", "gossip"}:
            self.state.lab.team_atmosphere = self._bounded(self.state.lab.team_atmosphere + tone)
            if post.category == "gossip" and tone != 0:
                self.state.tourism.latest_signal = f"小镇微博热议：{post.content[:24]}"
                self.state.tourism.daily_messages_count += 1
                if tone > 0:
                    self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + 1)
                    for agent in self.state.agents:
                        agent.life_satisfaction = self._bounded(agent.life_satisfaction + 1)
        elif post.category == "property" and tone > 0:
            self.state.tourism.buyer_leads_total += 1
        if post.reply_to_post_id:
            parent = self._find_feed_post(post.reply_to_post_id)
            if parent and post.author_type == "agent" and parent.author_type == "player":
                agent = self.get_agent(post.author_id)
                self._adjust_player_relation(agent, 1 if tone >= 0 else 0, "你在小镇微博上的公开互动被对方看见了。", observer=True)
        self._apply_business_public_reaction(post)

    def _append_feed_post(self, post: FeedPost, remember: bool = False, apply_impacts: bool = False) -> bool:
        if getattr(self.state, "feed_timeline", None) is None:
            self.state.feed_timeline = []
        post.mood = self._normalize_feed_mood(getattr(post, "mood", "neutral"))
        if post.mood == "neutral":
            post.mood = self._infer_feed_mood(post.category, post.content)
        duplicate = next(
            (
                existing
                for existing in self.state.feed_timeline[:16]
                if existing.author_type == post.author_type
                and existing.author_id == post.author_id
                and existing.category == post.category
                and existing.content[:64] == post.content[:64]
            ),
            None,
        )
        if duplicate is not None:
            return False
        if post.author_type == "system" and post.topic_tags:
            primary_tag = post.topic_tags[1] if len(post.topic_tags) > 1 else post.topic_tags[0]
            recent_system_duplicate = next(
                (
                    existing
                    for existing in self.state.feed_timeline[:24]
                    if existing.author_type == "system"
                    and existing.category == post.category
                    and primary_tag in (existing.topic_tags or [])
                ),
                None,
            )
            if recent_system_duplicate is not None:
                return False
        self.state.feed_timeline.insert(0, post)
        self.state.feed_timeline = self.state.feed_timeline[:1000]
        if post.author_type == "business":
            business = next((item for item in self.state.businesses or [] if item.id == post.author_id), None)
            if business is not None:
                business.last_post_day = post.day
                business.last_post_slot = post.time_slot
                self._apply_business_post_language_effects(business, post)
        if apply_impacts:
            self._apply_feed_impacts(post)
        if not remember:
            return True
        memory_text = f"微博：{post.author_name}说“{post.content[:26]}”"
        if post.author_type == "agent":
            agent = self.get_agent(post.author_id)
            self._remember(agent, memory_text, 2, long_term=post.heat >= 16)
        elif post.author_type == "tourist":
            tourist = self._find_tourist(post.author_id)
            self._remember_tourist(tourist, memory_text, 2)
        elif post.author_type == "player":
            self.state.player.injected_topics.insert(0, f"微博：{post.content[:24]}")
            self.state.player.injected_topics = self.state.player.injected_topics[:10]
        if post.heat >= 18:
            for agent in self.state.agents[:2]:
                self._remember(agent, f"热帖挂在脑子里：{post.author_name}提到“{post.content[:20]}”", 1)
            self.state.tourism.latest_signal = f"微博热帖：{post.content[:24]}"
        return True

    def _build_scheduled_social_preview_post(self, item: NewsTimelineItem) -> FeedPost:
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="system",
            author_id="system-feed",
            author_name="系统新闻台",
            day=self.state.day,
            time_slot=self.state.time_slot,
            category="gossip",
            content=self._clean_feed_text(
                f"系统新闻台预告：外面已经开始热议“{item.title}”。这条社会热点还没真正落到小镇，但游客、住房、消费和谁先被卷进去，八成很快就会有人吵起来。"
            ),
            topic_tags=["社会热点", item.source or "系统新闻台", "公开讨论"],
            desire_tags=["公开讨论"],
            likes=5 + self.random.randint(0, 5),
            reposts=1 + self.random.randint(0, 3),
            views=48 + self.random.randint(0, 32),
            summary=f"外部社会热点 {item.title} 先被投进了小镇微博。",
            impacts=self._feed_impacts_for_category("gossip"),
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _seed_feed_from_external_event(self, event: LabEvent, theme: str = "") -> None:
        category = "gossip" if str(theme).startswith("社会热点") or event.category == "general" else ("market" if event.category == "market" else ("research" if event.category == "geoai" else "policy"))
        if category == "gossip":
            content = f"系统新闻台刚抛来一条社会热点：{event.title}。现在大家开始把它往住房、消费、工作节奏和谁更难这几条线上吵。"
            tags = ["社会热点", event.source or "系统新闻台", "公开讨论"]
        elif category == "market":
            content = f"系统新闻台：{event.title}。这条消息已经把市场预期拨动了一下，后面大盘和游客消费都可能跟着偏。"
            tags = ["市场", event.source or "系统新闻台", "外部消息"]
        elif category == "research":
            content = f"系统新闻台：{event.title}。这条外部信号已经被大家往 GeoAI 和空间智能主线那边接了。"
            tags = ["GeoAI", "空间智能", event.source or "系统新闻台"]
        else:
            content = f"系统新闻台：{event.title}。政策和公共服务这边已经有人开始重新盘算这件事会把谁先推紧。"
            tags = ["政策", "监管", event.source or "系统新闻台"]
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="system",
            author_id="system-feed",
            author_name="系统新闻台",
            day=self.state.day,
            time_slot=self.state.time_slot,
            category=category,
            content=self._clean_feed_text(content),
            topic_tags=tags[:4],
            desire_tags=["公开讨论"],
            likes=4 + self.random.randint(0, 4),
            reposts=1 + self.random.randint(0, 2),
            views=36 + self.random.randint(0, 24),
            summary=f"{event.title} 被投进了小镇微博。",
            impacts=self._feed_impacts_for_category(category),
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        self._append_feed_post(post, remember=True, apply_impacts=True)

    def _move_agents_autonomously(self) -> None:
        moved_agents: list[dict[str, object]] = []
        for agent in self.state.agents:
            previous = agent.position.model_copy()
            if agent.is_resting:
                self._keep_agent_resting(agent)
                continue
            if agent.state.energy <= FORCED_REST_THRESHOLD:
                self._send_agent_home(agent, "体力已经见底，得先回去睡一觉。", forced=True)
                moved_agents.append(
                    {
                        "id": agent.id,
                        "name": agent.name,
                        "from": previous.model_dump(),
                        "to": agent.position.model_dump(),
                        "location": agent.current_location,
                        "resting": agent.is_resting,
                    }
                )
                continue
            if self.state.time_slot == "night" and self._night_returns_home(agent):
                self._send_agent_home(agent, "夜里差不多该回小屋休息了。")
                if agent.position != previous:
                    moved_agents.append(
                        {
                            "id": agent.id,
                            "name": agent.name,
                            "from": previous.model_dump(),
                            "to": agent.position.model_dump(),
                            "location": agent.current_location,
                            "resting": agent.is_resting,
                        }
                    )
                continue
            hub_x, hub_y = HUBS[agent.id][self.state.time_slot]
            target = Point(x=hub_x + self.random.randint(-2, 2), y=hub_y + self.random.randint(-1, 1))
            if self.random.random() < 0.34:
                anchor_choices = SLOT_ACTIVITY_ANCHORS.get(self.state.time_slot, [])
                if anchor_choices:
                    anchor_id = self.random.choice(anchor_choices)
                    target = self._pick_activity_anchor(anchor_id, actor_position=agent.position, avoid_rooms={agent.current_location})
            target = self._nearest_walkable(target, self._room(self._room_for(target.x, target.y)))
            agent.position = self._step_toward_point(agent.position, target)
            agent.current_location = self._room_for(agent.position.x, agent.position.y)
            drain = 3 if self.state.time_slot == "night" else 1
            agent.state.energy = max(0, agent.state.energy - drain)
            agent.state.focus = max(25, min(96, agent.state.focus + self.random.choice([-1, 0, 1])))
            if self.state.time_slot == "night":
                agent.state.stress = min(100, agent.state.stress + 1)
            if self.random.random() < 0.25:
                agent.current_bubble = self._ambient_bubble_for(agent)
            if agent.state.energy <= FORCED_REST_THRESHOLD:
                self._send_agent_home(agent, "体力已经见底，得先回去睡一觉。", forced=True)
            if agent.position != previous:
                moved_agents.append(
                    {
                        "id": agent.id,
                        "name": agent.name,
                        "from": previous.model_dump(),
                        "to": agent.position.model_dump(),
                        "location": agent.current_location,
                        "resting": agent.is_resting,
                    }
                )
        if moved_agents:
            self._log("agent_autonomous_move", movements=moved_agents)

    def _trigger_ambient_interaction(self) -> None:
        pairs: list[tuple[Agent, Agent]] = []
        for index, first in enumerate(self.state.agents):
            if first.is_resting:
                continue
            for second in self.state.agents[index + 1 :]:
                if second.is_resting:
                    continue
                distance = abs(first.position.x - second.position.x) + abs(first.position.y - second.position.y)
                if distance <= 4 and first.current_location == second.current_location:
                    pairs.append((first, second))
        if not pairs:
            return
        if self.random.random() > 0.65:
            return
        first, second = self.random.choice(pairs)
        first_desire, _ = dominant_desire_for_agent(self.state, first)
        second_desire, _ = dominant_desire_for_agent(self.state, second)
        thread = self._social_thread_for(first.id, second.id)
        if abs(first.position.x - second.position.x) + abs(first.position.y - second.position.y) > 2:
            second.position = self._room(second.current_location).clamp(first.position.x + 2, first.position.y)
        topic = thread.topic if thread and self.random.random() < 0.72 else self._pick_social_topic(first, second)
        if self.random.random() < 0.58:
            topic = self._desire_topic_between(first, second, first_desire, second_desire)
        mood = self._thread_mood(first, second, topic, existing=thread, first_desire=first_desire, second_desire=second_desire)
        line_a, line_b, gray_plan = self._ambient_pair_lines(
            first,
            second,
            topic,
            mood,
            continued=thread is not None,
            first_desire=first_desire,
            second_desire=second_desire,
        )
        first.current_bubble = line_a
        second.current_bubble = line_b
        self._remember(first, f"刚刚和 {second.name} 在{ROOM_LABELS.get(first.current_location, first.current_location)}聊了“{topic}”。", 2)
        self._remember(second, f"刚刚和 {first.name} 在{ROOM_LABELS.get(second.current_location, second.current_location)}聊了“{topic}”。", 2)
        if "GeoAI" in topic or "实验" in topic:
            self._remember(first, f"“{topic}”里的想法值得留到明天继续追。", 3, long_term=True)
            self._remember(second, f"“{topic}”里的想法值得留到明天继续追。", 3, long_term=True)
            self.state.lab.collective_reasoning = min(100, self.state.lab.collective_reasoning + 1)
            self._advance_geoai_progress(1, reason=topic)
        self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + 1)
        relation_delta = 4 if mood in {"warm", "spark"} else (-4 if mood == "tense" else 2)
        self._adjust_relation(first, second, relation_delta, f"在{ROOM_LABELS.get(first.current_location, first.current_location)}围绕“{topic}”持续聊了一会儿。")
        thread = self._advance_social_thread(first, second, topic, mood, line_a, line_b)
        ambient = DialogueOutcome(
            agent_id=first.id,
            agent_name=f"{first.name} × {second.name}",
            line=f"{first.name}：{line_a} {second.name}：{line_b}",
            topic=topic,
            bubble_text=line_a,
            effects=["团队氛围 +1", "关系推进 +1" if relation_delta > 0 else "气氛拉扯"],
        )
        self.state.ambient_dialogues.insert(0, ambient)
        self.state.ambient_dialogues = self.state.ambient_dialogues[:6]
        financial_outcome = self._apply_pair_dialogue_state(first, second, topic, mood, gray_plan)
        self._apply_desire_pair_impact(first, second, first_desire, second_desire, mood)
        left_desire_label = DESIRE_LABELS.get(first_desire, first_desire)
        right_desire_label = DESIRE_LABELS.get(second_desire, second_desire)
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="gray_trade" if financial_outcome and financial_outcome.get("gray_trade") else "ambient_dialogue",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=[first.id, second.id],
                participant_names=[first.name, second.name],
                topic=topic,
                summary=self._natural_gray_trade_summary(first.name, second.name, topic) if financial_outcome and financial_outcome.get("gray_trade") else self._natural_dialogue_summary(first, second, topic, mood),
                key_point=self._ambient_dialogue_key_point(
                    first.name,
                    second.name,
                    topic,
                    mood,
                    left_desire_label,
                    right_desire_label,
                    str(financial_outcome["note"]) if financial_outcome else "",
                ),
                transcript=[f"{first.name}：{line_a}", f"{second.name}：{line_b}"],
                desire_labels={first.name: left_desire_label, second.name: right_desire_label},
                mood=mood,
                financial_note=str(financial_outcome["note"]) if financial_outcome else "",
                interest_rate=int(financial_outcome["interest_rate"]) if financial_outcome and financial_outcome.get("interest_rate") is not None else None,
                gray_trade=bool(financial_outcome and financial_outcome.get("gray_trade")),
                gray_trade_type=str(financial_outcome["gray_trade_type"]) if financial_outcome and financial_outcome.get("gray_trade_type") else "",
                gray_trade_severity=int(financial_outcome["gray_trade_severity"]) if financial_outcome and financial_outcome.get("gray_trade_severity") is not None else 0,
            )
        )
        self._log(
            "ambient_dialogue",
            participants=[
                {"id": first.id, "name": first.name, "x": first.position.x, "y": first.position.y},
                {"id": second.id, "name": second.name, "x": second.position.x, "y": second.position.y},
            ],
            topic=topic,
            mood=mood,
            dialogue={"left": line_a, "right": line_b, "thread_id": thread.id, "thread_stage": thread.stage},
        )
        self.state.events.insert(
            0,
            build_internal_event(
                title=self._thread_event_title(first, second, thread),
                summary=self._natural_dialogue_summary(first, second, topic, mood),
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._maybe_emit_relationship_scene(first, second, thread)

    def _natural_dialogue_summary(self, first: Agent, second: Agent, topic: str, mood: str) -> str:
        location = ROOM_LABELS.get(first.current_location, first.current_location)
        topic = self._humanize_dialogue_topic(topic)
        mood_tail_options = {
            "warm": [
                "两个人越说越顺，气氛慢慢松下来。",
                "说着说着就顺了，先前那点绷着的感觉也散了。",
                "这一轮聊完，彼此都松了一口气。",
            ],
            "spark": [
                "话头一下对上了，明显聊出了点火花。",
                "有个点突然接上了，两个人都愿意往下多说几句。",
                "这话题一碰上，场子一下活了。",
            ],
            "tense": [
                "两边都没真让着对方。",
                "这几句说下来，谁也没打算先退。",
                "听得出来，两边都还绷着。",
                "这几句下来，谁都没把心里的那口气放下。",
                "表面没吵起来，但谁都没想先软下来。",
            ],
            "neutral": [
                "彼此都还在试探对方到底在意什么。",
                "这轮话没闹大，但大家都还留着一点判断。",
                "面上还算平稳，心里各有各的盘算。",
                "这话题先放在这儿了，谁也没把话说死。",
                "先聊到这里，各自心里都还在往下掂量。",
            ],
        }
        mood_tail = self.random.choice(mood_tail_options.get(mood, mood_tail_options["neutral"]))
        openers = [
            f"{first.name} 和 {second.name} 在{location}聊起了“{topic}”。",
            f"{first.name} 和 {second.name} 在{location}说到了“{topic}”。",
            f"{first.name} 和 {second.name} 在{location}把话题拐到了“{topic}”上。",
        ]
        return f"{self.random.choice(openers)} {mood_tail}"

    def _humanize_dialogue_topic(self, topic: str) -> str:
        replacements = {
            "刚刚路过听到的话": "刚才听进耳朵里的那几句",
            "昨晚没说完的话": "昨晚没说完的那点事",
            "谁该先退一步": "谁该先缓一下",
            "今晚到底要不要回屋": "今晚要不要早点回去歇着",
            "今天要不要看一眼股票": "今天要不要看一眼盘面",
            "有风天气": "今天这阵风和人的心气",
            "要不要晚点一起坐会儿": "晚点要不要一起坐坐",
            "证明自己和把事情说清之间的拉扯": "到底是要证明自己，还是先把事情说清",
        }
        return replacements.get(topic, topic)

    def _dialogue_topic_from_player_text(self, player_text: str, fallback: str) -> str:
        text = re.sub(r"\s+", " ", (player_text or "").strip())
        if not text:
            return fallback
        text = text.replace("你觉得", "").replace("你说", "").replace("你看", "")
        text = text.replace("你知道吗", "").replace("能不能", "").replace("要不要", "")
        text = text.strip("，。！？,.!?：: ")
        if "最值得逛" in text and ("哪一块" in text or "哪里" in text):
            return "这边最值得逛的地方"
        m = re.search(r"如果你想(去|看|逛|找)\s+([^，。！？,.!?]{2,18})", text)
        if m:
            return self._humanize_dialogue_topic(m.group(2).strip())
        m = re.search(r"(去|看|逛|找|住)\s+([^，。！？,.!?]{2,18})", text)
        if m and len(m.group(2).strip()) >= 2:
            return self._humanize_dialogue_topic(m.group(2).strip())
        m = re.search(r"[，,:：]?\s*是(.+?)(吗)?$", text)
        if m:
            candidate = m.group(1).strip("，。！？,.!?：: ")
            if len(candidate) >= 2:
                return self._humanize_dialogue_topic(candidate[:18].rstrip("，。！？,.!?：: "))
        m = re.search(r"(想知道|在意|关心|最想知道|最在意|最关心)(的)?[，,:：]?\s*(.+)$", text)
        if m:
            candidate = m.group(3).strip("，。！？,.!?：: ")
            candidate = re.sub(r"(吗|吧|呢)$", "", candidate).strip()
            if len(candidate) >= 2:
                return self._humanize_dialogue_topic(candidate[:18].rstrip("，。！？,.!?：: "))
        pieces = [part.strip("，。！？,.!?：: ") for part in re.split(r"[，。！？?!]", text) if part.strip()]
        candidate = pieces[0] if pieces else text
        candidate = re.sub(r"^(那|所以|其实|就是|我想问问|我想知道|我想聊聊|想问问|想知道|想聊聊)", "", candidate).strip()
        candidate = re.sub(r"^(你这趟|你现在|你刚才|你今天|你最近)", "", candidate).strip()
        candidate = re.sub(r"(是不是|算不算|到底|有没有)$", "", candidate).strip()
        if len(candidate) > 18:
            candidate = candidate[:18].rstrip("，。！？,.!?：: ")
        if len(candidate) < 4:
            return fallback
        return self._humanize_dialogue_topic(candidate)

    def _pick_fresh_summary_variant(self, candidates: list[str], *, recent_window: int = 18) -> str:
        recent_summaries = [item.summary for item in self.state.dialogue_history[:recent_window] if item.summary]
        fresh = [candidate for candidate in candidates if candidate not in recent_summaries]
        pool = fresh or candidates
        return self.random.choice(pool)

    def _tourist_topic_pool_for(self, tourist: TouristAgent) -> list[str]:
        by_archetype = {
            "周末散客": ["天气、住宿和集市小吃", "湖边散步和值不值得多待", "住一晚划不划算", "这里晚上安不安静"],
            "摄影游客": ["果园、湖边和好看的角落", "哪块光线最好", "夜里哪里最有气氛", "哪处最适合慢慢走"],
            "短住买手": ["集市、价格和什么值得带回去", "房租、短住和生活成本", "哪块更适合长住", "手里的钱花在哪更值"],
            "考察访客": ["GeoAI、小镇故事和谁最懂这里", "这地方怎么一步步变成这样", "谁在推动这里变化", "科技和日常到底怎么缠在一起"],
        }
        pool = list(by_archetype.get(tourist.archetype, []))
        if tourist.visitor_tier == "buyer":
            pool.extend(["房租、挂牌和长住成本", "手里的钱到底该先买房还是先留现金"])
        if tourist.visitor_tier == "vip":
            pool.extend(["这里花钱值不值", "住得舒服和看得漂亮哪个更重要"])
        if tourist.property_interest:
            pool.extend(["房租、短住和生活成本", "哪块更适合长住"])
        if not pool:
            pool = ["这里最值得逛哪里", "这地方到底适不适合多待一阵"]
        return list(dict.fromkeys(pool))

    def _refresh_tourist_topic(self, tourist: TouristAgent) -> None:
        pool = self._tourist_topic_pool_for(tourist)
        current = tourist.favorite_topic or ""
        candidates = [topic for topic in pool if topic != current]
        tourist.favorite_topic = self.random.choice(candidates or pool)
        tourist.brief_note = self._tourist_brief_note(tourist.visitor_tier, tourist.favorite_topic)

    def _natural_tourist_dialogue_summary(self, tourist_name: str, agent_name: str, location: str, topic: str) -> str:
        variants = [
            f"{tourist_name} 在{location}和 {agent_name} 聊了几句“{topic}”，对这里的日子更有画面了。",
            f"{tourist_name} 在{location}逮着 {agent_name} 问了问“{topic}”，一下觉得这里没那么生分了。",
            f"{tourist_name} 在{location}和 {agent_name} 扯到“{topic}”，越聊越觉得这里真有人在过日子。",
            f"{tourist_name} 在{location}跟 {agent_name} 聊到“{topic}”，原本走马观花的心思慢慢沉了下来。",
            f"{tourist_name} 在{location}和 {agent_name} 说起“{topic}”，对这里的印象一下立体了不少。",
            f"{tourist_name} 在{location}问了 {agent_name} 几句“{topic}”，听完以后觉得这里比想象中更有烟火气。",
            f"{tourist_name} 在{location}和 {agent_name} 聊到“{topic}”，原本只是路过的心思慢慢放慢了。",
            f"{tourist_name} 在{location}被 {agent_name} 这几句“{topic}”说得停下了脚，开始认真打量这里。",
        ]
        return self._pick_fresh_summary_variant(variants)

    def _natural_player_tourist_summary(self, tourist_name: str, topic: str) -> str:
        variants = [
            f"你和 {tourist_name} 聊了聊“{topic}”，对方明显更愿意继续逛下去。",
            f"你和 {tourist_name} 说到“{topic}”，他这趟路忽然就没那么像随便走走了。",
            f"你陪 {tourist_name} 聊了几句“{topic}”，他对这里又多上了一层心。",
            f"你跟 {tourist_name} 提了提“{topic}”，他原本有点散的注意力一下收回来了。",
            f"你和 {tourist_name} 顺着“{topic}”多聊了几句，对方看样子愿意在这里多待一阵。",
            f"你陪 {tourist_name} 扯到“{topic}”，他看这里的眼神慢慢从路过变成了认真打量。",
            f"你和 {tourist_name} 接着聊“{topic}”，他原本只想看看就走，现在明显想再多转一圈。",
            f"你跟 {tourist_name} 多说了几句“{topic}”，他一下不急着走了，像是想把这里再看清一点。",
        ]
        return self._pick_fresh_summary_variant(variants)

    def _natural_player_tourist_key_point(self, tourist_name: str, topic: str) -> str:
        topic = self._humanize_dialogue_topic(topic)
        variants = [
            f"{tourist_name} 一直绕着“{topic}”问，说明他现在最挂心的就是这件事。",
            f"看得出来，{tourist_name} 真正在意的是“{topic}”，你这几句正好接住了他。",
            f"{tourist_name} 聊来聊去还是绕回“{topic}”，这说明他心里最放不下的就是这条线。",
            f"{tourist_name} 其实就是想把“{topic}”问明白，你这一接，他整个人都松下来了一点。",
        ]
        return self.random.choice(variants)

    def _natural_tourist_agent_key_point(self, tourist_name: str, agent_name: str, topic: str) -> str:
        topic = self._humanize_dialogue_topic(topic)
        variants = [
            f"{tourist_name} 一直追着“{topic}”问，{agent_name} 也顺手把这里的日子讲得更具体了。",
            f"{tourist_name} 真正在意的是“{topic}”，{agent_name} 这几句正好把这层意思接住了。",
            f"这轮话里，{tourist_name} 更想弄明白“{topic}”，而 {agent_name} 则是在把这里的生活感慢慢说给他听。",
            f"{tourist_name} 抓着“{topic}”不放，{agent_name} 也没敷衍，反而把细节往前递了几句。",
        ]
        return self.random.choice(variants)

    def _topic_from_player_dialogue_transcript(self, transcript: list[str], fallback: str) -> str:
        if not transcript:
            return fallback
        player_line = ""
        for line in transcript:
            if line.startswith("你："):
                player_line = line.split("：", 1)[1].strip()
                break
        if not player_line:
            return fallback
        return self._dialogue_topic_from_player_text(player_line, fallback)

    def _natural_gray_trade_summary(self, requester_name: str, donor_name: str, topic: str) -> str:
        topic = self._humanize_dialogue_topic(topic)
        variants = [
            f"{requester_name} 和 {donor_name} 背着人做了一笔和“{topic}”有关的灰市交易。",
            f"{requester_name} 和 {donor_name} 私下把“{topic}”这件事谈成了一笔见不得光的买卖。",
            f"{requester_name} 和 {donor_name} 没走明面，悄悄围着“{topic}”做成了一笔交易。",
        ]
        return self.random.choice(variants)

    def _infer_explicit_gray_trade_type(
        self,
        requester: Agent,
        donor: Agent,
        request_line: str,
        response_line: str,
        topic: str,
    ) -> str:
        joined = f"{request_line} {response_line} {topic}"
        if any(
            token in joined
            for token in [
                "正式挂牌",
                "不挂牌",
                "不走正式挂牌",
                "挂牌",
                "租约",
                "钥匙",
                "空屋",
                "房子",
                "屋子",
                "转给你",
                "转手",
                "转租",
                "租给你",
                "租出去",
                "房租",
                "房东",
                "租客",
            ]
        ):
            return "rent_rigging"
        if any(token in joined for token in ["回扣", "额外塞一点", "账外", "不走台账", "派单", "轻活", "多塞一点活"]):
            return "wage_kickback"
        if any(token in joined for token in ["私货", "来路不明", "货箱", "塞到你屋后", "箱子", "假货"]):
            return "counterfeit_goods"
        if any(token in joined for token in ["拉高出货", "往上顶", "高位", "盘前", "那只票", "灰盘"]):
            return "pump_dump"
        if requester.current_location == "compute" or donor.current_location == "compute":
            return "wage_kickback"
        return "under_table_exchange"

    def _natural_bank_borrow_summary(self, borrower_name: str, bank_name: str, amount: int, term_days: int, amount_due: int) -> str:
        variants = [
            f"{borrower_name} 刚从{bank_name}周转了 ${amount}，准备 {term_days} 天内还上 ${amount_due}。",
            f"{borrower_name} 手头发紧，刚向{bank_name}借了 ${amount}，{term_days} 天后要还 ${amount_due}。",
            f"{borrower_name} 刚去{bank_name}补了一口现金，借到 ${amount}，到期要还 ${amount_due}。",
        ]
        return self.random.choice(variants)

    def _natural_bank_repay_summary(self, borrower_name: str, paid: int, remaining: int) -> str:
        if remaining <= 0:
            variants = [
                f"{borrower_name} 已经把这笔银行贷款结清了。",
                f"{borrower_name} 总算把这笔银行贷款还完了。",
                f"{borrower_name} 刚把欠银行的这笔钱清掉了。",
            ]
            return self.random.choice(variants)
        variants = [
            f"{borrower_name} 先还了银行 ${paid}，但这笔贷款还没彻底结清。",
            f"{borrower_name} 刚往银行回了 ${paid}，剩下的还得接着扛。",
            f"{borrower_name} 先把银行这边补了 ${paid}，后面还有尾账没清。",
        ]
        return self.random.choice(variants)

    def _normalize_recent_dialogue_history(self) -> None:
        for tourist in self._active_tourists():
            if tourist.favorite_topic:
                tourist.favorite_topic = tourist.favorite_topic.replace("园区", "小镇")
            if tourist.brief_note:
                tourist.brief_note = tourist.brief_note.replace("园区", "小镇")
            if tourist.current_activity:
                tourist.current_activity = tourist.current_activity.replace("园区", "小镇")
        for item in self.state.dialogue_history[:200]:
            summary = item.summary or ""
            if summary:
                item.summary = summary.replace("园区", "小镇")
            if item.key_point:
                item.key_point = item.key_point.replace("园区", "小镇")
                if "更受“" in item.key_point and "驱动" in item.key_point:
                    names = item.participant_names or ["有人", "另一个人"]
                    first_name = names[0]
                    second_name = names[1] if len(names) > 1 else "另一个人"
                    item.key_point = self._ambient_dialogue_key_point(
                        first_name,
                        second_name,
                        item.topic or "眼前这件事",
                        item.mood or "neutral",
                        item.desire_labels.get(first_name, "眼前这件事") if item.desire_labels else "眼前这件事",
                        item.desire_labels.get(second_name, "眼前这件事") if item.desire_labels else "眼前这件事",
                        item.financial_note or "",
                    )
                elif "主要在意“" in item.key_point and "更愿意继续停留和消费" in item.key_point and item.participant_names:
                    tourist_name = item.participant_names[-1]
                    item.key_point = self._natural_player_tourist_key_point(tourist_name, item.topic or "旅途体验")
                elif "主要在问“" in item.key_point and "顺手把小镇的节奏讲给他听" in item.key_point and len(item.participant_names) >= 2:
                    item.key_point = self._natural_tourist_agent_key_point(item.participant_names[0], item.participant_names[1], item.topic or "这里值得看什么")
            if item.topic:
                item.topic = item.topic.replace("园区", "小镇")
            if item.kind == "player_dialogue" and "player" in item.participants and len(item.participant_names) >= 2:
                inferred_topic = self._topic_from_player_dialogue_transcript(item.transcript or [], item.topic or "旅途见闻")
                if inferred_topic and inferred_topic != (item.topic or ""):
                    item.topic = inferred_topic
                    tourist_name = item.participant_names[-1]
                    item.summary = self._natural_player_tourist_summary(tourist_name, inferred_topic)
                    item.key_point = self._natural_player_tourist_key_point(tourist_name, inferred_topic)
            if "围绕“" in summary and "接了一轮，整体气氛偏" in summary and len(item.participant_names) >= 2:
                item.summary = self._natural_dialogue_summary(
                    self._find_agent(item.participants[0]) if item.participants and item.participants[0] in {a.id for a in self.state.agents} else self.state.agents[0],
                    self._find_agent(item.participants[1]) if len(item.participants) > 1 and item.participants[1] in {a.id for a in self.state.agents} else self.state.agents[0],
                    item.topic or "眼前这件事",
                    item.mood or "neutral",
                )
                continue
            if "游客对园区的印象被进一步拉高" in summary and len(item.participant_names) >= 2:
                tourist_name = item.participant_names[-1]
                item.summary = self._natural_player_tourist_summary(tourist_name, item.topic or "旅途见闻")
                continue
            if "短聊了一轮，游客视角给了园区一点新鲜感" in summary and len(item.participant_names) >= 2:
                tourist_name, agent_name = item.participant_names[0], item.participant_names[1]
                item.summary = self._natural_tourist_dialogue_summary(tourist_name, agent_name, ROOM_LABELS.get("foyer", "小镇里"), item.topic or "旅途见闻")
                continue
            if item.gray_trade and item.gray_trade_type and len(item.participant_names) >= 2:
                item.summary = self._natural_gray_trade_summary(item.participant_names[0], item.participant_names[1], item.topic or "眼前这件事")
                continue
        for post in self.state.feed_timeline[:300]:
            if post.content:
                post.content = post.content.replace("园区", "小镇")
            if post.summary:
                post.summary = post.summary.replace("园区", "小镇")
            if post.topic_tags:
                post.topic_tags = [tag.replace("园区", "小镇") for tag in post.topic_tags]
            if item.topic == "银行借贷" and "刚向青松合作银行借到" in summary:
                borrower_name = item.participant_names[0] if item.participant_names else "有人"
                m = re.search(r"借到 \$(\d+).*?(\d+) 天后归还 \$(\d+)", summary)
                if m:
                    item.summary = self._natural_bank_borrow_summary(borrower_name, self.state.bank.name, int(m.group(1)), int(m.group(2)), int(m.group(3)))
                continue
            if item.topic == "银行借贷" and ("已经把这笔银行贷款还清" in summary or "先补还了一部分逾期银行贷款" in summary or "先提前归还了一部分银行贷款" in summary):
                borrower_name = item.participant_names[0] if item.participant_names else "有人"
                m = re.search(r"本次处理 (\d+)", item.financial_note or "")
                remaining = 0
                m2 = re.search(r"剩余 \$(\d+)", item.financial_note or "")
                if m2:
                    remaining = int(m2.group(1))
                paid = int(m.group(1)) if m else 0
                item.summary = self._natural_bank_repay_summary(borrower_name, paid, remaining)

    def _soft_shift_player_pressure(self) -> None:
        if self.random.random() < 0.22:
            self.state.lab.research_progress = min(100, self.state.lab.research_progress + 1)
        if self.random.random() < 0.16:
            self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + 1)
        for thread in self.state.social_threads[:]:
            if thread.momentum <= 0:
                self.state.social_threads.remove(thread)

    def _apply_team_cash_delta(self, total_delta: int, reason: str, include_player: bool = True) -> int:
        if total_delta == 0:
            return 0
        members: list[object] = [*self.state.agents]
        if include_player:
            members.append(self.state.player)
        if not members:
            return 0
        if total_delta > 0:
            share = total_delta // len(members)
            remainder = total_delta % len(members)
            for index, member in enumerate(members):
                member.cash += share + (1 if index < remainder else 0)
            return total_delta
        remaining = abs(total_delta)
        members = sorted(members, key=lambda item: getattr(item, "cash", 0), reverse=True)
        deducted = 0
        while remaining > 0:
            moved = False
            for member in members:
                if member.cash <= 0 or remaining <= 0:
                    continue
                step = min(max(1, remaining // max(1, len(members))), member.cash, remaining)
                member.cash -= step
                remaining -= step
                deducted += step
                moved = True
            if not moved:
                break
        self._log("team_cash_shift", delta=-deducted, reason=reason)
        return -deducted

    def _maybe_trigger_random_lab_event(self) -> None:
        if self.random.random() > 0.1:
            return
        active_gray = sum(1 for case in self.state.gray_cases if case.status == "active")
        clean_lab = active_gray == 0
        options: list[dict[str, object]] = [
            {
                "title": "校园开放日突然带来一波人气",
                "summary": "来访者把研究站逛热了，顺手带来了赞助和讨论热度。",
                "category": "general",
                "tone": 2,
                "target": "AGR",
                "strength": 3,
                "cash": 28,
                "reputation": 5,
                "atmosphere": 2,
                "research": 1,
            },
            {
                "title": "老校友临时追加了一笔小赞助",
                "summary": "一位老校友听说你们最近势头不错，直接打来一笔小额支持。",
                "category": "geoai",
                "tone": 2,
                "target": "GEO",
                "strength": 4,
                "cash": 36,
                "reputation": 4,
                "research": 2,
                "knowledge": 2,
            },
            {
                "title": "冷藏和供电一起出了点小故障",
                "summary": "设备维修和耗材报废让大家今天得先掏钱填坑。",
                "category": "general",
                "tone": -1,
                "target": "AGR",
                "strength": 3,
                "cash": -18,
                "reputation": -2,
                "atmosphere": -1,
            },
            {
                "title": "社交媒体上冒出一条误传",
                "summary": "外面有人把实验室说得有点离谱，短时间内弄乱了外界观感。",
                "category": "market",
                "tone": -2,
                "target": "SIG",
                "strength": 4,
                "cash": -8,
                "reputation": -5,
                "atmosphere": -2,
            },
            {
                "title": "周边市集邀你们临时摆了个小摊",
                "summary": "原本只是去看看，结果意外卖掉了一些衍生小玩意和体验名额。",
                "category": "general",
                "tone": 1,
                "target": "AGR",
                "strength": 2,
                "cash": 16,
                "reputation": 2,
                "atmosphere": 1,
            },
            {
                "title": "市政测绘合作突然延期",
                "summary": "原本快敲定的合作被拖住，团队现金流和外部预期都受了点影响。",
                "category": "geoai",
                "tone": -2,
                "target": "GEO",
                "strength": 4,
                "cash": -22,
                "reputation": -3,
                "research": -1,
            },
        ]
        if clean_lab:
            options.append(
                {
                    "title": "合规抽查看下来比预期干净",
                    "summary": "检查的人挑不出什么毛病，反倒让实验室口碑回暖了一截。",
                    "category": "general",
                    "tone": 2,
                    "target": "broad",
                    "strength": 3,
                    "cash": 8,
                    "reputation": 6,
                    "atmosphere": 1,
                }
            )
        else:
            options.append(
                {
                    "title": "合规抽查让实验室神经紧了起来",
                    "summary": "外部抽查撞上了几条说不清的灰线，大家只好先掏钱补洞。",
                    "category": "market",
                    "tone": -2,
                    "target": "broad",
                    "strength": 4,
                    "cash": -14,
                    "reputation": -6,
                    "atmosphere": -2,
                }
            )
        event_plan = self.random.choice(options)
        event = LabEvent(
            id=f"event-{uuid4().hex[:8]}",
            category=str(event_plan["category"]),
            title=str(event_plan["title"]),
            summary=str(event_plan["summary"]),
            source="系统奇遇",
            time_slot=self.state.time_slot,
            impacts={
                "collective_reasoning": 1 if int(event_plan.get("tone", 0)) > 0 else 0,
                "research_progress": max(-1, min(2, int(event_plan.get("research", 0)))),
            },
            participants=[],
            tone_hint=int(event_plan["tone"]),
            market_target=str(event_plan["target"]),
            market_strength=int(event_plan["strength"]),
        )
        self._ingest_event(event, player_injected=False)
        cash_delta = self._apply_team_cash_delta(int(event_plan.get("cash", 0)), reason=event.title, include_player=True)
        self.state.lab.reputation = self._bounded(self.state.lab.reputation + int(event_plan.get("reputation", 0)))
        self.state.lab.team_atmosphere = self._bounded(self.state.lab.team_atmosphere + int(event_plan.get("atmosphere", 0)))
        self.state.lab.knowledge_base = self._bounded(self.state.lab.knowledge_base + int(event_plan.get("knowledge", 0)))
        self.state.lab.research_progress = self._bounded(self.state.lab.research_progress + int(event_plan.get("research", 0)))
        for agent in self.state.agents:
            if cash_delta > 0:
                agent.current_bubble = "今天外面真给面子。"
            elif cash_delta < 0:
                agent.current_bubble = "这波意外有点伤现金。"
        self._log(
            "random_lab_event",
            event={"title": event.title, "category": event.category, "tone": event.tone_hint},
            effects={
                "cash_delta": cash_delta,
                "reputation_delta": int(event_plan.get("reputation", 0)),
                "atmosphere_delta": int(event_plan.get("atmosphere", 0)),
                "research_delta": int(event_plan.get("research", 0)),
            },
        )

    def _roll_weather(self) -> str:
        weather_cycle = ["sunny", "breezy", "cloudy", "drizzle"]
        seed = (self.state.day * 7) + len(self.state.events) + len(self.state.ambient_dialogues) + self.random.randint(0, 5)
        return weather_cycle[seed % len(weather_cycle)]

    def _maybe_generate_system_news(self) -> None:
        if not self.state.market.is_open or self.random.random() > 0.16:
            return
        target = self.random.choice(["broad", self.state.market.rotation_leader or "GEO", "GEO", "AGR", "SIG"])
        regime = self.state.market.regime or "bull"
        market_bias = 1 if self.state.market.sentiment >= -8 else -1
        if self.random.random() < 0.26:
            tone_hint = 0
        else:
            positive_rate = 0.72 if regime == "bull" else 0.5 if regime == "sideways" else 0.34
            if market_bias < 0:
                positive_rate -= 0.12
            tone_hint = 1 if self.random.random() < positive_rate else -1
        strength = 2 if self.random.random() < 0.54 else 3
        title_bank = {
            ("broad", 1): "宏观数据释放温和回暖信号",
            ("broad", -1): "市场开始担心阶段性需求放缓",
            ("broad", 0): "资金面对下一阶段政策判断分歧加大",
            ("GEO", 1): "空间智能公司传出新订单增长",
            ("GEO", -1): "GeoAI 项目预算审查趋严",
            ("GEO", 0): "GeoAI 新项目落地节奏出现分歧",
            ("AGR", 1): "农产品与消费链预期边际改善",
            ("AGR", -1): "天气与运输扰动压住农业链情绪",
            ("AGR", 0): "农业链对下一轮需求判断分化",
            ("SIG", 1): "算力与信号服务板块获增量关注",
            ("SIG", -1): "科技成长股承压，信号服务板块回撤",
            ("SIG", 0): "科技资金轮动加快，短线分歧放大",
        }
        summary_bank = {
            1: "系统监测到一条偏利好的外部经济新闻，市场风险偏好略有抬升。",
            -1: "系统捕捉到一条偏利空的经济新闻，盘中避险情绪短暂升温。",
            0: "系统捕捉到一条分歧型经济新闻，市场短线波动明显加大。",
        }
        category = "market" if target in {"broad", "SIG", "AGR"} else "tech"
        event = LabEvent(
            id=f"event-{uuid4().hex[:8]}",
            category=category,
            title=title_bank[(target, tone_hint)],
            summary=summary_bank[tone_hint],
            source="系统新闻台",
            time_slot=self.state.time_slot,
            impacts={"collective_reasoning": 1, "research_progress": 1 if tone_hint >= 0 else 0},
            participants=[],
            tone_hint=tone_hint,
            market_target=target,
            market_strength=strength,
        )
        self._ingest_event(event, player_injected=False)

    def _money_pressure(self, agent: Agent) -> int:
        pressure = agent.money_desire
        total_funds = self._agent_total_funds(agent)
        if total_funds < self.state.company.low_cash_threshold:
            pressure = max(pressure, 88)
        if total_funds < 10:
            pressure = max(pressure, 96)
        elif total_funds < 25:
            pressure = max(pressure, 82)
        if any(loan.borrower_id == agent.id and loan.status in {"active", "overdue"} for loan in self.state.loans):
            pressure = max(pressure, 74)
        return min(100, pressure)

    def _agent_net_worth(self, agent: Agent) -> int:
        holdings_value = 0
        for symbol, shares in agent.portfolio.items():
            quote = self._quote(symbol)
            if quote is not None:
                holdings_value += int(round(quote.price * shares))
        return agent.cash + agent.deposit_balance + holdings_value - self._bank_liability_for("agent", agent.id)

    def _agent_total_funds(self, agent: Agent) -> int:
        return agent.cash + agent.deposit_balance

    def _player_net_worth(self) -> int:
        holdings_value = 0
        for symbol, shares in self.state.player.portfolio.items():
            quote = self._quote(symbol)
            if quote is not None:
                holdings_value += int(round(quote.price * shares))
        return self.state.player.cash + self.state.player.deposit_balance + holdings_value - self._bank_liability_for("player", self.state.player.id)

    def _player_total_funds(self) -> int:
        return self.state.player.cash + self.state.player.deposit_balance

    def _player_total_assets(self) -> int:
        property_value = sum(asset.estimated_value for asset in self.state.properties if asset.owner_type == "player" and asset.owner_id == self.state.player.id and asset.status == "owned")
        return self._player_net_worth() + property_value

    def _agent_total_assets(self, agent: Agent) -> int:
        property_value = sum(asset.estimated_value for asset in self.state.properties if asset.owner_type == "agent" and asset.owner_id == agent.id and asset.status == "owned")
        return self._agent_net_worth(agent) + property_value

    def _team_net_worth(self) -> int:
        return sum(self._agent_net_worth(agent) for agent in self.state.agents)

    def _team_cash_total(self) -> int:
        return sum(agent.cash for agent in self.state.agents)

    def _team_total_funds(self) -> int:
        return sum(self._agent_total_funds(agent) for agent in self.state.agents)

    def _bank_liability_for(self, borrower_type: str, borrower_id: str) -> int:
        return sum(
            loan.amount_due
            for loan in self.state.bank_loans
            if loan.borrower_type == borrower_type and loan.borrower_id == borrower_id and loan.status in {"active", "overdue"}
        )

    def _team_liquid_capital(self) -> int:
        team_cash = self._team_cash_total()
        outstanding_bank = sum(loan.amount_due for loan in self.state.bank_loans if loan.borrower_type == "agent" and loan.status in {"active", "overdue"})
        return team_cash - outstanding_bank

    def _market_cap(self, quote) -> float:
        shares = quote.shares_outstanding or BASE_SHARES_OUTSTANDING.get(quote.symbol, 100000)
        return quote.price * shares

    def _base_market_cap(self, quote) -> float:
        shares = quote.shares_outstanding or BASE_SHARES_OUTSTANDING.get(quote.symbol, 100000)
        base_price = quote.base_price or BASE_PRICES.get(quote.symbol, quote.open_price or quote.price or 10.0)
        return base_price * shares

    def _fair_value_for_quote(self, quote) -> float:
        base_price = quote.base_price or BASE_PRICES.get(quote.symbol, quote.open_price or quote.price or 10.0)
        regime = self.state.market.regime or "bull"
        inflation_drag = -max(0.0, ((self.state.market.inflation_index or 100.0) - 112.0) / 340)
        tax_drag = -(
            self.state.government.securities_tax_rate_pct
            + self.state.government.property_holding_tax_rate_pct * 0.35
            + self.state.government.consumption_tax_rate_pct * 0.28
        ) / 260
        regime_bias = {"bull": 0.08, "sideways": 0.0, "risk": -0.1}.get(regime, 0.0)
        if quote.symbol == "GEO":
            geo_signal = (self.state.lab.geoai_progress - 30) / 210
            reasoning_signal = (self.state.lab.collective_reasoning - 34) / 230
            reputation_signal = (self.state.lab.reputation - 24) / 320
            growth_bias = max(-0.12, min(1.35, geo_signal + reasoning_signal + reputation_signal * 0.55))
        elif quote.symbol == "AGR":
            weather_signal = {"sunny": 0.1, "breezy": 0.08, "cloudy": -0.03, "drizzle": -0.08}[self.state.weather]
            atmosphere_signal = (self.state.lab.team_atmosphere - 62) / 340
            shelter_bid = 0.07 if regime == "risk" else 0.0
            growth_bias = max(-0.16, min(0.95, weather_signal + atmosphere_signal + shelter_bid))
        else:
            external_signal = (self.state.lab.external_sensitivity - 22) / 165
            hype_signal = abs(self.state.market.sentiment or 0) / 180
            gray_drag = -sum(1 for case in self.state.gray_cases if case.status == "active") / 48
            growth_bias = max(-0.18, min(1.45, external_signal + hype_signal + gray_drag))
        fair_multiplier = max(0.72, 1 + regime_bias + inflation_drag + tax_drag + growth_bias)
        return round(base_price * fair_multiplier, 2)

    def _market_index_from_quotes(self) -> float:
        if not self.state.market.stocks:
            return self.state.market.index_value
        current_cap = sum(self._market_cap(quote) for quote in self.state.market.stocks)
        base_cap = sum(self._base_market_cap(quote) for quote in self.state.market.stocks)
        if base_cap <= 0:
            return round(max(40.0, self.state.market.index_value), 2)
        value = 100.0 * (current_cap / base_cap)
        return round(max(40.0, value), 2)

    def _recent_intraday_index_move(self) -> float:
        history = self.state.market.index_history or []
        if len(history) < 2:
            return 0.0
        window = history[-6:]
        start = window[0].open
        end = window[-1].close
        if not start:
            return 0.0
        return ((end - start) / start) * 100

    def _recent_intraday_volatility(self) -> float:
        history = self.state.market.index_history or []
        if len(history) < 4:
            return max(0.85, self.state.market.realized_volatility_pct or 0.85)
        window = history[-8:]
        returns: list[float] = []
        for candle in window:
            if candle.open:
                returns.append(abs(((candle.close - candle.open) / candle.open) * 100))
        if not returns:
            return max(0.85, self.state.market.realized_volatility_pct or 0.85)
        avg = sum(returns) / len(returns)
        return max(0.55, min(2.8, avg))

    def _apply_opening_gap(self) -> None:
        previous_close_map = {quote.symbol: quote.price for quote in self.state.market.stocks}
        recent_return = self._recent_market_return()
        regime = self.state.market.regime or "bull"
        overnight_bias = {"bull": 0.18, "sideways": 0.02, "risk": -0.2}.get(regime, 0.04)
        sentiment_bias = (self.state.market.sentiment or 0) / 120
        macro_bias = max(-0.8, min(0.8, recent_return / 8))
        volatility = self._recent_intraday_volatility()
        for quote in self.state.market.stocks:
            fair_value = self._fair_value_for_quote(quote)
            quote.fair_value = fair_value
            valuation_gap = ((fair_value - quote.price) / max(0.01, quote.price)) * 100
            sector_gap = {
                "GEO": 0.22 if self.state.lab.geoai_progress >= 50 else 0.0,
                "AGR": 0.18 if self.state.weather in {"sunny", "breezy"} else -0.12,
                "SIG": 0.14 if self.state.lab.external_sensitivity >= 30 else 0.0,
            }.get(quote.symbol, 0.0)
            valuation_pull = max(-0.8, min(0.8, valuation_gap / 7))
            gap = self.random.gauss(
                overnight_bias + sentiment_bias + macro_bias + sector_gap + valuation_pull,
                0.26 + volatility * 0.16 + max(0.0, quote.volatility_score - 0.7) * 0.08,
            )
            gap = max(-2.8, min(2.8, gap))
            quote.price = max(4.0, round(previous_close_map[quote.symbol] * (1 + gap / 100), 2))
            quote.change_pct = round(gap, 2)
            quote.day_change_pct = 0.0
            quote.open_price = quote.price
            quote.volume = 0
            quote.turnover_pct = 0.0

    def _update_index_history(self, limit_state: str = "normal", append: bool = True) -> None:
        value = round(max(40.0, self._market_index_from_quotes()), 2)
        self.state.market.index_value = value
        history = self.state.market.index_history or []
        if not history or history[-1].day != self.state.day:
            self.state.market.index_history = [IndexCandle(day=self.state.day, open=value, high=value, low=value, close=value, limit_state=limit_state)]
            return
        candle = history[-1]
        if not append:
            candle.close = value
            candle.high = max(candle.high, value)
            candle.low = min(candle.low, value)
            if limit_state != "normal":
                candle.limit_state = limit_state
            return
        self.state.market.index_history.append(
            IndexCandle(
                day=self.state.day,
                open=candle.close,
                high=max(candle.close, value),
                low=min(candle.close, value),
                close=value,
                limit_state=limit_state,
            )
        )
        self.state.market.index_history = self.state.market.index_history[-42:]

    def _update_daily_index_history(self, limit_state: str = "normal") -> None:
        value = round(max(40.0, self._market_index_from_quotes()), 2)
        self.state.market.index_value = value
        history = self.state.market.daily_index_history or []
        if not history:
            self.state.market.daily_index_history = [IndexCandle(day=self.state.day, open=value, high=value, low=value, close=value, limit_state=limit_state)]
            return
        candle = history[-1]
        if candle.day != self.state.day:
            self.state.market.daily_index_history.append(
                IndexCandle(day=self.state.day, open=value, high=value, low=value, close=value, limit_state=limit_state)
            )
            return
        candle.close = value
        candle.high = max(candle.high, value)
        candle.low = min(candle.low, value)
        if limit_state != "normal":
            candle.limit_state = limit_state

    def _refresh_market_microstructure(self) -> None:
        stocks = self.state.market.stocks or []
        if not stocks:
            self.state.market.turnover_total = 0.0
            self.state.market.turnover_ratio_pct = 0.0
            self.state.market.realized_volatility_pct = 0.8
            self.state.market.advancers = 0
            self.state.market.decliners = 0
            return
        market_cap = sum(self._market_cap(quote) for quote in stocks)
        turnover_total = sum(quote.price * max(0, quote.volume) for quote in stocks)
        advancers = sum(1 for quote in stocks if quote.day_change_pct > 0.12)
        decliners = sum(1 for quote in stocks if quote.day_change_pct < -0.12)
        self.state.market.turnover_total = round(turnover_total, 2)
        self.state.market.turnover_ratio_pct = round((turnover_total / market_cap) * 100, 2) if market_cap else 0.0
        self.state.market.advancers = advancers
        self.state.market.decliners = decliners
        self.state.market.realized_volatility_pct = round(self._recent_intraday_volatility(), 2)

    def _normalize_market_quotes_for_realism(self) -> None:
        market_anchor = max(0.72, min(1.85, (self.state.market.index_value or 100.0) / 100))
        sector_anchor = {
            "GEO": 1 + max(-0.12, min(0.55, (self.state.lab.geoai_progress - 30) / 180)),
            "AGR": 1 + {"sunny": 0.08, "breezy": 0.06, "cloudy": -0.02, "drizzle": -0.08}[self.state.weather],
            "SIG": 1 + max(-0.1, min(0.45, (self.state.lab.external_sensitivity - 22) / 120)),
        }
        for quote in self.state.market.stocks or []:
            base_price = BASE_PRICES.get(quote.symbol, max(8.0, quote.open_price or quote.price or 10.0))
            move_multiplier = 1 + max(-0.22, min(0.22, (quote.day_change_pct or 0.0) / 100))
            target_price = round(base_price * market_anchor * sector_anchor.get(quote.symbol, 1.0) * move_multiplier, 2)
            quote.base_price = base_price
            quote.open_price = round(max(4.0, target_price / max(0.75, 1 + (quote.day_change_pct or 0.0) / 100)), 2)
            quote.price = max(4.0, target_price)
            quote.fair_value = self._fair_value_for_quote(quote)
            quote.shares_outstanding = BASE_SHARES_OUTSTANDING.get(quote.symbol, quote.shares_outstanding or 100000)
            quote.avg_volume = BASE_AVG_VOLUME.get(quote.symbol, quote.avg_volume or 4200)
            quote.volume = min(max(quote.volume or 0, quote.avg_volume // 2), quote.avg_volume * 4)
            quote.turnover_pct = round((quote.volume / max(1, quote.shares_outstanding)) * 100, 2)
            quote.volatility_score = max(0.68, min(1.45, quote.volatility_score or 0.9))
        current_index = round(self._market_index_from_quotes(), 2)
        self.state.market.index_value = current_index
        self.state.market.index_history = [IndexCandle(day=self.state.day, open=current_index, high=current_index, low=current_index, close=current_index, limit_state="normal")]
        self.state.market.daily_index_history = [IndexCandle(day=self.state.day, open=current_index, high=current_index, low=current_index, close=current_index, limit_state="normal")]
        self._refresh_market_microstructure()

    def _recent_market_return(self) -> float:
        history = self.state.market.daily_index_history or []
        if len(history) < 2:
            return 0.0
        window = history[-3:]
        start = window[0].open
        end = window[-1].close
        if not start:
            return 0.0
        return ((end - start) / start) * 100

    def _refresh_market_regime(self, force_roll: bool) -> None:
        market = self.state.market
        current = market.regime or "bull"
        age = max(1, market.regime_age or 1)
        recent_return = self._recent_market_return()
        sentiment = market.sentiment
        next_regime = current

        if current == "bull":
            if sentiment <= -16 or recent_return <= -3.4:
                next_regime = "risk"
            elif age >= 3 and (abs(recent_return) <= 1.1 or -10 <= sentiment <= 10):
                next_regime = "sideways"
        elif current == "sideways":
            if sentiment >= 18 or recent_return >= 2.6:
                next_regime = "bull"
            elif sentiment <= -18 or recent_return <= -2.8:
                next_regime = "risk"
        else:
            if sentiment >= 18 and recent_return >= 3.2:
                next_regime = "bull"
            elif sentiment >= 6 or recent_return >= 1.0:
                next_regime = "sideways"

        if force_roll and next_regime == current:
            roll = self.random.random()
            if current == "bull" and age >= 4 and roll < 0.18:
                next_regime = "sideways"
            elif current == "sideways":
                if roll < 0.14:
                    next_regime = "bull"
                elif roll > 0.88:
                    next_regime = "risk"
            elif current == "risk" and age >= 3 and roll < 0.22:
                next_regime = "sideways"

        if next_regime != current:
            market.regime = next_regime
            market.regime_age = 1
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"市场阶段切换为{self._market_regime_label(next_regime)}",
                    summary=f"当前市场已经进入{self._market_regime_label(next_regime)}，盘面节奏和新闻反应会随之变化。",
                    slot=self.state.time_slot,
                    category="market",
                ),
            )
            self.state.events = self.state.events[:8]
        elif force_roll:
            market.regime_age = age + 1

    def _market_regime_label(self, regime: str) -> str:
        return {
            "bull": "牛市",
            "sideways": "震荡市",
            "risk": "风险市",
        }.get(regime, regime)

    def _rotation_label(self, symbol: str) -> str:
        return {
            "GEO": "GeoGrid",
            "AGR": "AgriLoop",
            "SIG": "SignalWorks",
        }.get(symbol, symbol)

    def _pick_rotation_target(self, regime: str) -> str:
        weights = {
            "bull": [("GEO", 0.44), ("SIG", 0.34), ("AGR", 0.22)],
            "sideways": [("AGR", 0.38), ("GEO", 0.34), ("SIG", 0.28)],
            "risk": [("AGR", 0.48), ("GEO", 0.30), ("SIG", 0.22)],
        }[regime]
        roll = self.random.random()
        cursor = 0.0
        for symbol, weight in weights:
            cursor += weight
            if roll <= cursor:
                return symbol
        return weights[-1][0]

    def _refresh_sector_rotation(self, force_roll: bool) -> None:
        market = self.state.market
        current = market.rotation_leader or "GEO"
        age = max(1, market.rotation_age or 1)
        regime = market.regime or "bull"
        desired = self._pick_rotation_target(regime)
        if regime == "risk" and force_roll and current != "AGR":
            desired = "AGR"
        elif regime == "bull" and force_roll and age >= 2:
            desired = "SIG" if current == "GEO" else "GEO"
        elif regime == "sideways" and force_roll and age >= 2 and current == "SIG":
            desired = "AGR"

        current_quote = self._quote(current)
        desired_quote = self._quote(desired)
        should_rotate = False
        if force_roll and age >= 2 and desired != current:
            should_rotate = True
        elif current_quote and current_quote.day_change_pct <= -4.2 and desired != current:
            should_rotate = True
        elif desired_quote and current_quote and desired_quote.day_change_pct - current_quote.day_change_pct >= 2.6:
            should_rotate = True

        if should_rotate:
            market.rotation_leader = desired
            market.rotation_age = 1
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"板块轮动切到 {self._rotation_label(desired)}",
                    summary=f"当前市场主线开始偏向 {self._rotation_label(desired)}，其余板块可能进入跟涨或补跌阶段。",
                    slot=self.state.time_slot,
                    category="market",
                ),
            )
            self.state.events = self.state.events[:8]
        elif force_roll:
            market.rotation_age = age + 1

    def _refresh_tasks(self) -> None:
        team_funds = self._team_total_funds()
        for task in self.state.tasks:
            if task.id == "task-geo-baseline":
                baseline = task.start_value or 500
                target_total = task.goal_value or 650
                progress = int(max(0, min(100, ((team_funds - baseline) / max(1, target_total - baseline)) * 100)))
                task.progress = progress
                task.metric_key = task.metric_key or "team_total_funds"
                task.start_value = baseline
                task.goal_value = target_total
                task.description = f"把团队总资金从 ${baseline} 慢慢推到 ${target_total}。当前团队总资金约 ${team_funds}，重点靠稳健打工、白天兑现收益、银行存款和协作经营。"
            elif task.category == "main":
                start_value = task.start_value
                goal_value = task.goal_value
                if goal_value <= start_value:
                    start_value, goal_value = self._derive_main_task_bounds(task, team_funds)
                    task.start_value = start_value
                    task.goal_value = goal_value
                task.metric_key = task.metric_key or "team_total_funds"
                task.progress = int(max(0, min(100, ((team_funds - start_value) / max(1, goal_value - start_value)) * 100)))
                task.description = self._main_task_description(task, team_funds)
            elif task.id == "task-news":
                task.description = "注入一条真正会影响市场或团队情绪的外部信息，让股价和大家的判断发生波动。"
        self._archive_completed_tasks()
        self._ensure_task_pipeline()

    def _main_task_description(self, task: Task | None = None, team_funds: int | None = None, main_round: int | None = None) -> str:
        current_funds = team_funds if team_funds is not None else self._team_total_funds()
        resolved_round = main_round
        if resolved_round is None:
            resolved_round = next(
                (int(match.group(1)) for match in [re.search(r"第\s*(\d+)\s*轮", (task.title if task else "") or "")] if match),
                1 + sum(1 for archived in self.state.archived_tasks if archived.category == "main"),
            )
        start_value, next_target_funds = self._derive_main_task_bounds(task, current_funds, resolved_round)
        return f"把团队总资金从 ${start_value} 推到 ${next_target_funds}。当前团队总资金约 ${current_funds}。这轮重点靠地产收益、稳健交易、游客消费、银行存款和额度管理。"

    def _derive_main_task_bounds(
        self,
        task: Task | None = None,
        team_funds: int | None = None,
        main_round: int | None = None,
    ) -> tuple[int, int]:
        current_funds = team_funds if team_funds is not None else self._team_total_funds()
        if task and task.start_value and task.goal_value > task.start_value:
            return task.start_value, task.goal_value
        parsed_values = []
        if task and task.description:
            parsed_values = [int(value.replace(",", "")) for value in re.findall(r"\$([\d,]+)", task.description)]
        if len(parsed_values) >= 2:
            return parsed_values[0], max(parsed_values[1], parsed_values[0] + 1)
        resolved_round = main_round
        if resolved_round is None:
            resolved_round = next(
                (int(match.group(1)) for match in [re.search(r"第\s*(\d+)\s*轮", (task.title if task else "") or "")] if match),
                1 + sum(1 for archived in self.state.archived_tasks if archived.category == "main"),
            )
        step = 120 + max(0, resolved_round - 1) * 20
        start_value = current_funds
        goal_value = max(start_value + step, 650 + (max(1, resolved_round) - 1) * 140)
        return start_value, goal_value

    def _apply_lab_rewards(self, rewards: dict[str, int], reason: str) -> None:
        if not rewards:
            return
        if rewards.get("reputation"):
            self.state.lab.reputation = self._bounded(self.state.lab.reputation + rewards["reputation"])
        if rewards.get("knowledge_base"):
            self.state.lab.knowledge_base = self._bounded(self.state.lab.knowledge_base + rewards["knowledge_base"])
        if rewards.get("team_atmosphere"):
            self.state.lab.team_atmosphere = self._bounded(self.state.lab.team_atmosphere + rewards["team_atmosphere"])
        if rewards.get("external_sensitivity"):
            self.state.lab.external_sensitivity = self._bounded(self.state.lab.external_sensitivity + rewards["external_sensitivity"])
        if rewards.get("research_progress"):
            self.state.lab.research_progress = self._bounded(self.state.lab.research_progress + rewards["research_progress"])
        if rewards.get("collective_reasoning"):
            self.state.lab.collective_reasoning = self._bounded(self.state.lab.collective_reasoning + rewards["collective_reasoning"])
        self._log("lab_rewards_applied", rewards=rewards, reason=reason)

    def _archive_completed_tasks(self) -> None:
        active: list = []
        for task in self.state.tasks:
            if task.progress < task.target:
                active.append(task)
                continue
            if task.completed_day is None:
                task.completed_day = self.state.day
                task.archived_note = f"第 {self.state.day} 天完成，已转入归档。"
                self._apply_lab_rewards(task.rewards, f"任务完成：{task.title}")
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=f"任务完成：{task.title}",
                        summary=f"{task.title} 已达成，现已归档。实验室因此拿到了一轮正向口碑和运营收益。",
                        slot=self.state.time_slot,
                        category="general",
                    ),
                )
                self.state.events = self.state.events[:8]
            if not any(existing.id == task.id for existing in self.state.archived_tasks):
                self.state.archived_tasks.insert(0, task.model_copy(deep=True))
        self.state.archived_tasks = self.state.archived_tasks[:12]
        self.state.tasks = active

    def _ensure_task_pipeline(self) -> None:
        categories = {task.category for task in self.state.tasks}
        if "main" not in categories:
            self.state.tasks.insert(0, self._build_next_main_task())
        categories = {task.category for task in self.state.tasks}
        if "social" not in categories:
            self.state.tasks.append(self._build_next_social_task())
        categories = {task.category for task in self.state.tasks}
        if "external" not in categories:
            self.state.tasks.append(self._build_next_external_task())
        categories = {task.category for task in self.state.tasks}
        if "daily" not in categories:
            self.state.tasks.append(self._build_next_daily_task())

    def _build_next_main_task(self) -> Task:
        team_funds = self._team_total_funds()
        main_round = 1 + sum(1 for task in self.state.archived_tasks if task.category == "main")
        start_value, goal_value = self._derive_main_task_bounds(team_funds=team_funds, main_round=main_round)
        task_id = f"task-main-{self.state.day}-{main_round}"
        return Task(
            id=task_id,
            title=f"团队资金扩张 · 第 {main_round} 轮",
            category="main",
            description=self._main_task_description(team_funds=team_funds, main_round=main_round),
            progress=0,
            target=100,
            metric_key="team_total_funds",
            start_value=start_value,
            goal_value=goal_value,
            participants=[agent.id for agent in self.state.agents],
            rewards={"reputation": 8 + min(8, main_round), "knowledge_base": 4 + min(6, main_round)},
        )

    def _build_next_social_task(self) -> Task:
        social_round = 1 + sum(1 for task in self.state.archived_tasks if task.category == "social")
        target_agent = min(self.state.agents, key=lambda agent: agent.life_satisfaction + agent.relations.get("player", 0) // 2)
        return Task(
            id=f"task-social-{self.state.day}-{social_round}",
            title=f"关系修复窗口 · 第 {social_round} 轮",
            category="social",
            description=f"优先和 {target_agent.name} 以及另一名同事形成两轮有效互动，缓和压力、稳定关系和实验室氛围。",
            progress=0,
            target=100,
            participants=[target_agent.id],
            rewards={"team_atmosphere": 10, "reputation": 3},
        )

    def _build_next_external_task(self) -> Task:
        external_round = 1 + sum(1 for task in self.state.archived_tasks if task.category == "external")
        target_sector = self.state.market.rotation_leader or "GEO"
        return Task(
            id=f"task-external-{self.state.day}-{external_round}",
            title=f"外部风向扫描 · 第 {external_round} 轮",
            category="external",
            description=f"捕捉一条会影响 {self._rotation_label(target_sector)} 或团队判断的外部信号，让市场和实验室预期发生真实波动。",
            progress=0,
            target=100,
            participants=["kai"],
            rewards={"external_sensitivity": 12, "research_progress": 6},
        )

    def _build_next_daily_task(self) -> Task:
        daily_round = 1 + sum(1 for task in self.state.archived_tasks if task.category == "daily")
        return Task(
            id=f"task-daily-{self.state.day}-{daily_round}",
            title=f"生活面维稳 · 第 {daily_round} 轮",
            category="daily",
            description="让至少两个人顺利休息、结清一笔生活或银行压力，并把团队平均生活满意度再往上托一点。",
            progress=0,
            target=100,
            participants=["player", "rae"],
            rewards={"team_atmosphere": 6, "reputation": 2},
        )

    def _refresh_agents_for_new_day(self) -> None:
        weather_bonus = {"sunny": 3, "breezy": 2, "cloudy": 0, "drizzle": -1}[self.state.weather]
        active_gray_cases = sum(1 for case in self.state.gray_cases if case.status == "active")
        if active_gray_cases == 0 and self.state.lab.team_atmosphere >= 58:
            self.state.lab.reputation = self._bounded(self.state.lab.reputation + 1)
        elif active_gray_cases <= 1 and self.state.lab.team_atmosphere >= 72 and self.state.lab.research_progress >= 30:
            self.state.lab.reputation = self._bounded(self.state.lab.reputation + 1)
        player_relation_avg = int(sum(self.state.player.social_links.values()) / max(1, len(self.state.player.social_links))) if self.state.player.social_links else 0
        recent_interventions = sum(1 for action in self.state.player.daily_actions if action.startswith("intervene:"))
        self.state.player.life_satisfaction = self._bounded(
            self.state.player.life_satisfaction
            + (2 if self.state.player.housing_quality >= 55 else -1)
            + (1 if self.state.player.cash >= 40 else -2 if self.state.player.cash <= 12 else 0)
            + (1 if player_relation_avg >= 18 else -1 if player_relation_avg <= -8 else 0)
        )
        reputation_recovery = 0
        if recent_interventions == 0 and player_relation_avg >= 18:
            reputation_recovery += 1
        if self.state.tourism.daily_revenue >= 40:
            reputation_recovery += 1
        if active_gray_cases == 0 and self.state.lab.team_atmosphere >= 70:
            reputation_recovery += 1
        if reputation_recovery:
            self.state.player.reputation_score = self._bounded(self.state.player.reputation_score + min(2, reputation_recovery))
        for agent in self.state.agents:
            if agent.is_resting:
                continue
            loan_load = sum(1 for loan in self.state.loans if loan.status in {"active", "overdue"} and loan.borrower_id == agent.id)
            agent.state.mood = self._bounded(agent.state.mood + weather_bonus + (1 if agent.credit_score >= 75 else -2 if agent.credit_score <= 35 else 0))
            agent.state.stress = self._bounded(agent.state.stress - 4 + loan_load * 2)
            agent.state.focus = self._bounded(agent.state.focus + 2 - (2 if loan_load else 0))
            agent.state.curiosity = self._bounded(agent.state.curiosity + (2 if self.state.market.is_open else 0))
            agent.life_satisfaction = self._bounded(
                agent.life_satisfaction
                + (2 if agent.housing_quality >= 55 else -1)
                + (1 if agent.cash >= 36 else -2 if agent.cash <= 10 else 0)
                + (1 if agent.state.energy >= 60 else -1)
            )
            agent.current_bubble = "新一天开始了。"
            agent.last_interaction = f"第 {self.state.day} 天开始，正在重新判断今天该靠近谁。"
            self._remember(agent, f"第 {self.state.day} 天开始了。天气是{weather_label(self.state.weather)}，你在重新判断今天的节奏。", 2)
        self._log("daily_agent_refresh", day=self.state.day, weather=self.state.weather)

    def _generate_lab_daily(self, previous_day: int) -> None:
        if previous_day <= 0:
            return
        if any(brief.day == self.state.day for brief in self.state.daily_briefings):
            return
        items: list[str] = []
        entries: list[DailyBriefItem] = []

        def add_entry(
            text: str,
            target_kind: str = "",
            target_id: str = "",
            target_filter: str = "",
            title: str = "",
            summary: str = "",
            result: str = "",
            impact: str = "",
        ) -> None:
            items.append(text)
            entries.append(
                DailyBriefItem(
                    id=f"brief-item-{uuid4().hex[:8]}",
                    text=text,
                    title=title,
                    summary=summary,
                    result=result,
                    impact=impact,
                    target_kind=target_kind,
                    target_id=target_id,
                    target_filter=target_filter,
                )
            )

        yesterday_dialogues = [record for record in self.state.dialogue_history if record.day == previous_day]
        conflict = next((record for record in yesterday_dialogues if record.mood == "tense"), None)
        gray_trade = next((record for record in yesterday_dialogues if record.gray_trade), None)
        loan_record = next((record for record in yesterday_dialogues if record.kind == "loan" or record.interest_rate is not None), None)
        warm_pair = next((record for record in yesterday_dialogues if record.mood in {"warm", "spark"} and record.kind == "ambient_dialogue"), None)
        geoai_milestone = next((event for event in self.state.events if event.category == "geoai" and "里程碑" in event.title), None)
        previous_candle = next((candle for candle in reversed(self.state.market.daily_index_history or []) if candle.day == previous_day), None)
        previous_tax_revenue = sum(
            max(0, -record.amount)
            for record in self.state.finance_history
            if record.day == previous_day and record.category == "tax"
        )
        previous_tourist_revenue = sum(
            abs(record.amount)
            for record in self.state.finance_history
            if record.day == previous_day and record.category == "tourism" and record.action == "spend"
        )
        previous_tourist_signals = [event for event in self.state.events if event.title.startswith("游客消息：")]
        policy_event = next((event for event in self.state.events if event.category == "general" and ("税制" in event.title or "监管" in event.title)), None)
        audit_event = next((event for event in self.state.events if "监管抽查" in event.title), None)
        if previous_candle is not None:
            day_change = ((previous_candle.close - previous_candle.open) / max(1, previous_candle.open)) * 100
            market_tone = "大盘走强" if day_change >= 1.2 else "大盘承压" if day_change <= -1.2 else "大盘震荡"
            add_entry(
                f"股市速写：{market_tone}，指数收在 {previous_candle.close:.2f}，昨日日内 {day_change:+.2f}%。",
                target_kind="market",
                title="股市速写",
                summary=f"昨天市场整体呈现“{market_tone}”，收盘指数在 {previous_candle.close:.2f}。",
                result=f"单日振幅落到 {day_change:+.2f}%，说明资金情绪已经偏向 {'追高' if day_change >= 1.2 else '谨慎' if day_change <= -1.2 else '观望'}。",
                impact="今天一早关于仓位、止盈和要不要继续追板块主线的讨论会明显变多。",
            )
        leader = self.state.market.rotation_leader or "GEO"
        add_entry(
            f"板块主线：{leader} 仍是大家盯得最紧的方向，轮动已经持续 {self.state.market.rotation_age} 天。",
            target_kind="market",
            title="板块主线",
            summary=f"{leader} 还在领跑当前轮动，已经连续走了 {self.state.market.rotation_age} 天。",
            result="这说明注意力没有散掉，大家还在围着同一条叙事算下一步。",
            impact="市场聊天、微博热帖和游客试水投资都会更容易往这只票上聚。",
        )
        if previous_tax_revenue > 0:
            add_entry(
                f"财政速递：昨日政府合计收税 ${previous_tax_revenue}，累计财政收入来到 ${self.state.government.total_revenue}。",
                target_kind="market",
                title="财政速递",
                summary=f"昨天政府又收进 ${previous_tax_revenue} 的税费，财政盘子继续变厚。",
                result=f"累计财政收入来到 ${self.state.government.total_revenue}，政府调税、补贴和建设都有了更大腾挪空间。",
                impact="居民会更关注后续税率、补贴和建设动作，政府支持度也会跟着波动。",
            )
        if previous_tourist_revenue > 0:
            add_entry(
                f"游客速递：昨天游客带来约 ${previous_tourist_revenue} 的本地收入，{self.state.tourism.market_name} 和 {self.state.tourism.inn_name} 都更热闹了；累计回头客 {self.state.tourism.repeat_customers_total}、高消费客户 {self.state.tourism.vip_customers_total}。",
                target_kind="market",
                title="游客速递",
                summary=f"昨天游客消费又给小镇带来 ${previous_tourist_revenue} 的收入，旅馆和集市都吃到了热度。",
                result=f"累计回头客已经到 {self.state.tourism.repeat_customers_total}，高消费客户来到 {self.state.tourism.vip_customers_total}。",
                impact="今天的消费、看房和微博讨论会继续被游客体验带着走。",
            )
        hot_feed = next(
            (
                post
                for post in sorted(self.state.feed_timeline, key=lambda item: (item.day, item.heat), reverse=True)
                if post.day == previous_day
            ),
            None,
        )
        if hot_feed is not None:
            add_entry(
                f"微博热帖：{hot_feed.author_name} 昨天围绕“{self._feed_title_topic(hot_feed.content, hot_feed.category)}”发声，热度冲到 {hot_feed.heat}，很多人今天还在接着讨论。",
                target_kind="feed",
                target_id=hot_feed.id,
                title="微博热帖",
                summary=f"{hot_feed.author_name} 昨天那条围绕“{self._feed_title_topic(hot_feed.content, hot_feed.category)}”的帖子，热度已经冲到 {hot_feed.heat}。",
                result="公开讨论没有在夜里散掉，今天还会继续发酵。",
                impact="它会继续影响市场情绪、游客判断，甚至可能把政府也拖进回应里。",
            )
        if previous_tourist_signals:
            latest_signal = previous_tourist_signals[0]
            add_entry(
                f"游客耳语：{latest_signal.title}，这条外来消息昨天已经影响到小镇判断和盘面气氛。",
                target_kind="event",
                target_id=latest_signal.id,
                title="游客耳语",
                summary=f"昨天最显眼的外来消息是“{latest_signal.title}”，而且已经顺着游客嘴里扩散开了。",
                result="这类消息没有正式文件背书，但已经足够改变大家的判断方式。",
                impact="今天无论是微博、市场还是房产讨论，都会带着一点这条消息留下的偏向。",
            )
        if policy_event is not None:
            add_entry(
                f"监管速递：{policy_event.title}，当前监管强度 {self.state.government.enforcement_level}，备注是“{self.state.government.last_policy_note}”。",
                target_kind="event",
                target_id=policy_event.id,
                title="监管速递",
                summary=f"昨天最硬的一条制度动作是“{policy_event.title}”。",
                result=f"当前监管强度已经到 {self.state.government.enforcement_level}，而且政府还留下了“{self.state.government.last_policy_note}”的备注。",
                impact="今天灰市、赌场和高风险投机这几条线都会更收着点，市场情绪也会更谨慎。",
            )
        elif audit_event is not None:
            add_entry(
                f"监管速递：{audit_event.title}，大家都在讨论监管和罚缴会不会继续压情绪与盘面。",
                target_kind="event",
                target_id=audit_event.id,
                title="监管速递",
                summary=f"{audit_event.title} 在昨天晚上已经成了公开话题。",
                result="大家开始重新估算监管继续收紧的概率。",
                impact="今天无论是股市、赌场还是灰色交易，都会多一层被盯着看的紧张感。",
            )
        if geoai_milestone is not None:
            add_entry(
                f"研究头条：{geoai_milestone.title}，实验室里已经有人开始押注 GEO 继续被重估。",
                target_kind="event",
                target_id=geoai_milestone.id,
                title="研究头条",
                summary=f"昨天最像里程碑的一件事，是“{geoai_milestone.title}”。",
                result="研究讨论已经开始外溢到投资判断，大家不只是聊技术，也在聊它值多少钱。",
                impact="今天的市场、微博和人物对话里，GeoAI 相关内容会更容易被放大。",
            )
        else:
            add_entry(
                f"研究头条：空间智能累计推进到 {self.state.lab.geoai_progress} 点，GeoAI 主线还在缓慢发酵。",
                target_kind="market",
                title="研究头条",
                summary=f"空间智能累计推进已经来到 {self.state.lab.geoai_progress} 点。",
                result="虽然没有新的爆点，但这条主线没有熄火，还在慢慢积累注意力。",
                impact="它会继续托着相关讨论和部分投资偏好，不至于一下退场。",
            )
        if loan_record is not None:
            add_entry(
                f"借贷消息：{loan_record.financial_note or loan_record.key_point}",
                target_kind="dialogue",
                target_id=loan_record.id,
                target_filter="loan",
                title="借贷消息",
                summary=loan_record.financial_note or loan_record.key_point,
                result="现金紧的人已经先动手借钱了，说明生活和投机压力都还在。",
                impact="今天关于利率、还款、存款和要不要继续借的讨论会更密。",
            )
        else:
            active_loans = [loan for loan in self.state.loans if loan.status in {'active', 'overdue'}]
            if active_loans:
                add_entry(
                    f"借贷消息：实验室里还有 {len(active_loans)} 笔借款挂着，口碑和现金流都在被盯。",
                    target_kind="dialogue",
                    target_filter="loan",
                    title="借贷消息",
                    summary=f"实验室里还挂着 {len(active_loans)} 笔活跃借款。",
                    result="借贷这条线并没有过去，现金流和口碑仍然在承压。",
                    impact="今天银行、存款和资金调度相关的动作会更频繁。",
                )
        if gray_trade is not None:
            add_entry(
                f"小道消息：{gray_trade.key_point}",
                target_kind="dialogue",
                target_id=gray_trade.id,
                target_filter="gray",
                title="小道消息",
                summary=gray_trade.key_point,
                result="说明昨晚的地下交易没有真的藏住，风声已经漏出来了。",
                impact="今天微博、灰案和监管观察都会更容易顺着这条线继续发酵。",
            )
        if conflict is not None:
            add_entry(
                f"关系风波：{conflict.key_point}",
                target_kind="dialogue",
                target_id=conflict.id,
                target_filter="desire",
                title="关系风波",
                summary=conflict.key_point,
                result="分歧已经不只是情绪，而是开始影响接下来的合作方式。",
                impact="今天人物互动、站队和微博表态都可能继续沿着这条裂缝发展。",
            )
        if warm_pair is not None:
            add_entry(
                f"八卦速递：{warm_pair.participant_names[0]} 和 {warm_pair.participant_names[1]} 昨天聊得很顺，圈子里都看出来了。",
                target_kind="dialogue",
                target_id=warm_pair.id,
                title="八卦速递",
                summary=f"{warm_pair.participant_names[0]} 和 {warm_pair.participant_names[1]} 昨天那轮对话很顺，别人也都看出来了。",
                result="这种顺气的关系会继续往外传，慢慢改掉周围人看他们的方式。",
                impact="今天社交圈的站位和亲近感会继续被这条线轻轻往前推。",
            )
        if self.state.story_beats:
            lead_story = self.state.story_beats[0]
            add_entry(
                f"故事线更新：{lead_story.title}，已经推进到第 {lead_story.stage} 段。",
                target_kind="story",
                target_id=lead_story.id,
                title="故事线更新",
                summary=f"{lead_story.title} 已经推进到第 {lead_story.stage} 段。",
                result="这说明主线没有停，而是在继续累积后果和新动作。",
                impact="今天任务、人物计划和微博讨论会继续围着这条故事线转。",
            )
        recent_events = [event for event in self.state.events[:6] if event.time_slot != "morning" or event.category != "general"]
        for event in recent_events:
            if len(items) >= 12:
                break
            if event.title not in "".join(items):
                add_entry(
                    f"新闻摘录：{event.title} 还在被大家反复提起。",
                    target_kind="event",
                    target_id=event.id,
                    title="新闻摘录",
                    summary=f"昨天留下的“{event.title}”并没有散掉，今天一早还在被反复提起。",
                    result="这说明它已经从单条消息变成持续背景。",
                    impact="今天很多判断和互动，都会带着这条消息留下的阴影或期待。",
                )
        while len(items) < 6:
            fallback = [
                f"日常杂闻：昨天是{weather_label(self.state.weather)}的一天，大家整体节奏比前天更慢一点。",
                "茶水间八卦：有人昨晚没回屋，今天一早已经被大家默默记上了。",
                "走廊传闻：最近谁跟谁靠得更近，大家心里其实都有数。",
                "情绪观察：高压的人昨天明显更想谈钱和体力，而不是谈理想。",
            ][len(items) % 4]
            if fallback not in items:
                title, summary = fallback.split("：", 1)
                add_entry(
                    fallback,
                    title=title,
                    summary=summary,
                    result="它不一定最响，但足够说明昨天的小镇气氛往哪边偏了。",
                    impact="今天的闲聊、误会和临时决定，往往就会从这种小线索里长出来。",
                )
        briefing = DailyBriefing(
            id=f"brief-{uuid4().hex[:8]}",
            day=self.state.day,
            title=f"Lab Daily · 第 {self.state.day} 天晨报",
            lead=f"给第 {self.state.day} 天开场的晨间简报，回看第 {previous_day} 天的重要动静。",
            items=items[:12],
            entries=entries[:12],
        )
        self.state.daily_briefings.insert(0, briefing)
        self.state.daily_briefings = self.state.daily_briefings[:7]
        combined_memory = "；".join(briefing.items[:6])
        for agent in self.state.agents:
            self._remember(agent, f"Lab Daily：{combined_memory}", 3, long_term=True)
            agent.current_bubble = "先看今天的 Lab Daily。"
        self._log("lab_daily_generated", day=self.state.day, items=briefing.items)

    def _sync_market_clock(self) -> None:
        self.state.market.is_open = self.state.time_slot != "night"

    def _quote(self, symbol: str):
        return next((quote for quote in self.state.market.stocks if quote.symbol == symbol), None)

    def _apply_quote_move(self, symbol: str, pct_delta: float, reason: str) -> None:
        quote = self._quote(symbol)
        if quote is None:
            return
        next_price = max(4.0, round(quote.price * (1 + pct_delta / 100), 2))
        daily_floor = round(quote.open_price * 0.88, 2)
        if pct_delta < 0 and next_price < daily_floor:
            next_price = daily_floor
        quote.price = next_price
        quote.change_pct = round(pct_delta, 2)
        quote.day_change_pct = round(((quote.price - quote.open_price) / quote.open_price) * 100, 2)
        quote.last_reason = reason

    def _update_market_intraday(self) -> None:
        if not self.state.market.is_open:
            return
        self.state.market.tick += 1
        regime = self.state.market.regime or "bull"
        leader = self.state.market.rotation_leader or "GEO"
        recent_return = self._recent_intraday_index_move()
        volatility = self._recent_intraday_volatility()
        team_support = 0.18 if self._team_net_worth() <= 620 else 0.0
        regime_profile = {
            "bull": {"drift": 0.1, "sigma": 0.64, "tail_up": 0.13, "tail_down": 0.06, "correlation": 0.58},
            "sideways": {"drift": 0.0, "sigma": 0.82, "tail_up": 0.09, "tail_down": 0.1, "correlation": 0.42},
            "risk": {"drift": -0.1, "sigma": 1.08, "tail_up": 0.05, "tail_down": 0.2, "correlation": 0.78},
        }[regime]
        sentiment_bias = (self.state.market.sentiment or 0) / 150
        weather_bias = {"sunny": 0.06, "breezy": 0.03, "cloudy": -0.04, "drizzle": -0.1}[self.state.weather]
        momentum_pull = max(-0.75, min(0.75, recent_return / 6))
        mean_revert = -max(-0.65, min(0.65, recent_return / 8))
        leverage_penalty = max(0.0, -recent_return / 6)
        sigma = regime_profile["sigma"] + volatility * 0.22 + leverage_penalty * 0.28
        market_factor = self.random.gauss(regime_profile["drift"] + sentiment_bias + weather_bias + team_support + momentum_pull + mean_revert, sigma)
        tail_roll = self.random.random()
        if tail_roll < regime_profile["tail_down"]:
            market_factor += self.random.uniform(-2.6, -1.2)
        elif tail_roll > 1 - regime_profile["tail_up"]:
            market_factor += self.random.uniform(1.0, 2.4)
        for quote in self.state.market.stocks:
            fair_value = self._fair_value_for_quote(quote)
            quote.fair_value = fair_value
            valuation_gap = ((fair_value - quote.price) / max(0.01, quote.price)) * 100
            sector_bias = {
                "GEO": 0.34 if self.state.lab.geoai_progress >= 30 else 0.06,
                "AGR": 0.28 if self.state.weather in {"sunny", "breezy"} else -0.1,
                "SIG": 0.26 if self.state.lab.external_sensitivity >= 25 else 0.04,
            }.get(quote.symbol, 0.0)
            rotation_bias = 0.54 if quote.symbol == leader else -0.12
            if regime == "risk" and quote.symbol == "AGR":
                rotation_bias += 0.18
            if regime == "bull" and quote.symbol == "SIG" and leader != "SIG":
                rotation_bias += 0.06
            mean_reversion = -(quote.day_change_pct / 3.2)
            extension_pull = 0.0
            if quote.day_change_pct >= 5.5:
                extension_pull -= self.random.uniform(0.8, 1.9)
            elif quote.day_change_pct <= -5.5:
                extension_pull += self.random.uniform(0.9, 2.1)
            support_bid = 0.0
            if self.state.market.index_value < 96:
                support_bid += 0.24
            if quote.day_change_pct <= -4.5:
                support_bid += 0.66
            beta = SECTOR_BETA.get(quote.symbol, 1.0)
            valuation_pull = max(-1.2, min(1.2, valuation_gap * 0.18))
            idio_sigma = IDIOSYNCRATIC_VOL.get(quote.symbol, 0.7) + volatility * 0.08 + max(0.0, quote.volatility_score - 0.8) * 0.2
            idiosyncratic = self.random.gauss(0, idio_sigma * max(0.24, 1 - regime_profile["correlation"]))
            spread_drag = -0.18 if regime == "risk" and quote.symbol == "SIG" else 0.0
            drift = (
                market_factor * beta * regime_profile["correlation"]
                + sector_bias
                + rotation_bias
                + mean_reversion
                + extension_pull
                + support_bid
                + spread_drag
                + valuation_pull
                + idiosyncratic
            )
            drift = max(-5.4, min(5.4, drift))
            self._apply_quote_move(quote.symbol, drift, "白天盘中波动")
            volume_boost = (
                1.0
                + abs(drift) / 1.8
                + abs(valuation_gap) / 15
                + (0.42 if quote.symbol == leader else 0.0)
                + (0.25 if regime == "risk" and drift < 0 else 0.0)
            )
            base_volume = quote.avg_volume or BASE_AVG_VOLUME.get(quote.symbol, 4200)
            quote.volume = max(0, int(round(base_volume * volume_boost * self.random.uniform(0.78, 1.32))))
            quote.turnover_pct = round((quote.volume / max(1, quote.shares_outstanding or BASE_SHARES_OUTSTANDING.get(quote.symbol, 100000))) * 100, 2)
            quote.volatility_score = round(
                max(
                    0.55,
                    min(
                        2.8,
                        quote.volatility_score * 0.82
                        + abs(drift) * 0.12
                        + (0.18 if drift < -1.5 else 0.0),
                    ),
                ),
                2,
            )
        self._refresh_market_microstructure()
        self._update_index_history()
        self._update_daily_index_history()

    def _event_tone(self, event: LabEvent) -> int:
        text = f"{event.title} {event.summary}"
        positive = self._keyword_hits(text, ["突破", "增长", "合作", "提升", "利好", "上涨", "新机会", "进展"])
        negative = self._keyword_hits(text, ["风险", "裁员", "暴跌", "下滑", "争执", "封禁", "失败", "收紧"])
        return max(-2, min(2, positive - negative))

    def _apply_event_to_market(self, event: LabEvent) -> None:
        self._sync_market_clock()
        regime = self.state.market.regime or "bull"
        leader = self.state.market.rotation_leader or "GEO"
        tone = event.tone_hint if event.tone_hint else self._event_tone(event)
        strength = max(1, min(5, getattr(event, "market_strength", 2)))
        target = getattr(event, "market_target", "broad")
        deltas: dict[str, float] = {"GEO": 0.0, "AGR": 0.0, "SIG": 0.0}
        text = f"{event.title} {event.summary}"
        limit_state = "normal"
        if event.category == "geoai":
            deltas["GEO"] += 1.2 + tone * 1.4
            deltas["SIG"] += 0.3 + tone * 0.8
        elif event.category == "tech":
            deltas["SIG"] += 1.0 + tone * 1.2
            deltas["GEO"] += 0.4 + tone * 0.7
        elif event.category == "market":
            deltas["SIG"] += 1.1 + tone * 1.5
            deltas["AGR"] += 0.2 + tone * 0.9
        elif event.category == "general":
            deltas["AGR"] += 0.2 + tone * 0.7
        elif event.category == "gaming":
            deltas["SIG"] += 0.3 + tone * 0.5
        if tone < 0:
            risk_off = abs(tone) * 0.28
            deltas["GEO"] -= risk_off
            deltas["AGR"] -= risk_off * 0.75
            deltas["SIG"] -= risk_off * 0.95
        intensity_scale = 0.6 + (strength * 0.28)
        for symbol in deltas:
            deltas[symbol] *= intensity_scale
            if deltas[symbol] > 0:
                deltas[symbol] *= 1.18 if regime == "bull" else 0.94 if regime == "risk" else 1.02
            elif deltas[symbol] < 0:
                deltas[symbol] *= 0.92 if regime == "risk" else 0.68 if regime == "bull" else 0.8
        if target != "broad":
            for symbol in deltas:
                if symbol == target:
                    deltas[symbol] *= 1.75
                else:
                    deltas[symbol] *= 0.45
        elif tone == 0:
            swing = 0.7 + strength * 0.35
            deltas["GEO"] += self.random.uniform(-swing, swing)
            deltas["AGR"] += self.random.uniform(-swing * 0.9, swing * 0.9)
            deltas["SIG"] += self.random.uniform(-swing * 1.1, swing * 1.1)
        if leader in deltas:
            if tone >= 0:
                deltas[leader] += 0.8
            else:
                deltas[leader] *= 0.86
        strong_up = any(keyword in text for keyword in ["涨停", "爆单", "突破", "政策利好", "融资"])
        strong_down = any(keyword in text for keyword in ["跌停", "暴跌", "封禁", "监管", "收紧", "事故"])
        if strong_up or strong_down or (tone >= 2 and self.random.random() < 0.16) or (tone <= -2 and self.random.random() < 0.05):
            symbol = "SIG" if event.category in {"market", "tech"} else "GEO" if event.category == "geoai" else "AGR"
            deltas[symbol] = LIMIT_MOVE_PCT if (strong_up or tone > 0) and not strong_down else -LIMIT_MOVE_PCT
            limit_state = "up" if deltas[symbol] > 0 else "down"
        sentiment_shift = tone * 8
        self.state.market.sentiment = max(-100, min(100, self.state.market.sentiment + sentiment_shift))
        for symbol, delta in deltas.items():
            if abs(delta) >= 0.1:
                if abs(delta) >= LIMIT_MOVE_PCT:
                    self._apply_quote_move(symbol, delta, f"受“{event.title}”影响，出现{'涨停' if delta > 0 else '跌停'}")
                else:
                    self._apply_quote_move(symbol, delta, f"受“{event.title}”影响")
                quote = self._quote(symbol)
                if quote is not None:
                    quote.fair_value = self._fair_value_for_quote(quote)
                    quote.volume = max(quote.volume or 0, int(round((quote.avg_volume or BASE_AVG_VOLUME.get(symbol, 4200)) * (1.1 + abs(delta) / 2))))
                    quote.turnover_pct = round((quote.volume / max(1, quote.shares_outstanding or BASE_SHARES_OUTSTANDING.get(symbol, 100000))) * 100, 2)
                    quote.volatility_score = round(max(0.6, min(2.9, quote.volatility_score * 0.84 + abs(delta) * 0.14)), 2)
        self._refresh_market_microstructure()
        self._update_index_history(limit_state=limit_state)
        self._update_daily_index_history(limit_state=limit_state)

    def _trigger_market_activity(self) -> None:
        if not self.state.market.is_open:
            return
        for agent in self.state.agents:
            trade_bias = 0.09 + agent.risk_appetite / 240 + agent.money_urgency / 420
            if agent.is_resting or self.random.random() >= min(0.28, trade_bias):
                continue
            trade = self._decide_market_trade(agent)
            if trade is None:
                continue
            self._execute_trade_for_agent(agent, *trade)

    def _decide_market_trade(self, agent: Agent) -> tuple[str, str, int, str] | None:
        pressure = self._money_pressure(agent)
        agent.money_urgency = pressure
        if not self.state.market.stocks:
            return None
        if pressure >= 92:
            for symbol, shares in sorted(agent.portfolio.items(), key=lambda item: item[1], reverse=True):
                if shares > 0:
                    return (symbol, "sell", min(shares, 2), "手头现金快见底了，先套一点现。")
        preferred_symbol = MARKET_SYMBOL_PREFERENCE.get(agent.persona, "GEO")
        if agent.persona == "opportunist":
            preferred_symbol = max(
                self.state.market.stocks,
                key=lambda quote: quote.change_pct + quote.turnover_pct * 0.35 + max(0.0, (quote.fair_value - quote.price) / max(0.01, quote.price) * 100) * 0.3,
            ).symbol
        quote = self._quote(preferred_symbol) or self.state.market.stocks[0]
        held = agent.portfolio.get(quote.symbol, 0)
        valuation_gap = ((quote.fair_value - quote.price) / max(0.01, quote.price)) * 100
        signal = quote.change_pct + valuation_gap * 0.45 + quote.turnover_pct * 0.16 + (self.state.market.sentiment / 28) + ((agent.risk_appetite - 50) / 40)
        if held > 0 and (quote.change_pct <= -1.6 or (pressure >= 80 and agent.cash < 25) or quote.day_change_pct >= 3.8):
            return (quote.symbol, "sell", min(held, max(1, 1 + held // 2)), "走势不稳，或者得先把现金留出来。")
        if signal <= 0.05 or agent.cash < quote.price:
            return None
        budget = max(quote.price, min(agent.cash, 18 + agent.risk_appetite // 3 + pressure // 5))
        shares = int(budget // quote.price)
        shares = max(1, min(4, shares))
        return (quote.symbol, "buy", shares, "白天盘面和外部消息都还算顺，先小仓位试一下。")

    def _execute_trade_for_agent(self, agent: Agent, symbol: str, side: str, shares: int, reason: str) -> bool:
        quote = self._quote(symbol)
        if quote is None or shares <= 0:
            return False
        amount = int(round(quote.price * shares))
        if side == "buy":
            affordable = int(agent.cash // quote.price)
            shares = min(shares, affordable)
            if shares <= 0:
                return False
            amount = int(round(quote.price * shares))
            agent.cash -= amount
            agent.portfolio[symbol] = agent.portfolio.get(symbol, 0) + shares
            agent.current_bubble = f"先买 {shares} 手 {symbol}"
            agent.current_activity = f"刚在盘中买入 {shares} 股 {quote.name}。"
            agent.last_trade_summary = f"买入 {quote.name} {shares} 股，花了 ${amount}。"
            self._remember(agent, f"你刚买入了 {quote.name} {shares} 股，理由是：{reason}", 2)
        else:
            held = agent.portfolio.get(symbol, 0)
            shares = min(shares, held)
            if shares <= 0:
                return False
            amount = int(round(quote.price * shares))
            agent.portfolio[symbol] = held - shares
            if agent.portfolio[symbol] <= 0:
                agent.portfolio.pop(symbol, None)
            agent.cash += amount
            agent.current_bubble = f"先卖掉 {shares} 手 {symbol}"
            agent.current_activity = f"刚在盘中卖出 {shares} 股 {quote.name}。"
            agent.last_trade_summary = f"卖出 {quote.name} {shares} 股，回收 ${amount}。"
            self._remember(agent, f"你刚卖出了 {quote.name} {shares} 股，理由是：{reason}", 2)
        market_tax = self._collect_tax(
            payer_type="agent",
            payer_id=agent.id,
            payer_name=agent.name,
            revenue_key="market",
            label="证券交易",
            base_amount=amount,
            rate_pct=self.state.government.securities_tax_rate_pct,
        )
        agent.last_trade_summary = f"{agent.last_trade_summary[:-1]}，另缴税 ${market_tax}。"
        realized_joy = 2 if side == "sell" and quote.day_change_pct >= 2.5 else 1 if side == "buy" and quote.change_pct > 0 else 0
        relief = 2 if side == "sell" else 0
        self._shift_agent_state(
            agent,
            mood=1 + realized_joy if side == "buy" else max(0, realized_joy),
            stress=1 if side == "buy" and quote.change_pct < 0 else -relief,
            curiosity=1,
        )
        self._adjust_agent_satisfaction(agent, 2 if realized_joy >= 2 else 1 if side == "buy" or side == "sell" else 0)
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"{agent.name}{'买入' if side == 'buy' else '卖出'}了 {quote.name}",
                summary=f"{agent.name} 在白天盘中{'买入' if side == 'buy' else '卖出'} {shares} 股 {quote.name}，金额约 ${amount}。{reason}",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]
        self._log(
            "market_trade",
            agent={"id": agent.id, "name": agent.name},
            trade={"symbol": symbol, "name": quote.name, "side": side, "shares": shares, "amount": amount, "reason": reason},
        )
        self._append_finance_record(
            actor_id=agent.id,
            actor_name=agent.name,
            category="market",
            action="buy" if side == "buy" else "sell",
            summary=f"{agent.name}{'买入' if side == 'buy' else '卖出'}了 {quote.name} {shares} 股，金额约 ${amount}，税费 ${market_tax}。",
            amount=amount + market_tax if side == "buy" else max(0, amount - market_tax),
            asset_name=quote.name,
            counterparty="Pixel Exchange",
        )
        quote.volume = max(0, (quote.volume or 0) + shares)
        quote.turnover_pct = round((quote.volume / max(1, quote.shares_outstanding or BASE_SHARES_OUTSTANDING.get(symbol, 100000))) * 100, 2)
        quote.volatility_score = round(max(0.55, min(2.8, quote.volatility_score * 0.96 + shares * 0.02)), 2)
        self._refresh_market_microstructure()
        self._update_index_history(append=False)
        self._update_daily_index_history()
        self._refresh_tasks()
        return True

    def _decide_player_trade(self) -> tuple[str, str, int, str]:
        if not self.state.market.stocks:
            return ("GEO", "buy", 0, "暂无盘面")
        preferred = max(
            self.state.market.stocks,
            key=lambda quote: quote.change_pct + quote.day_change_pct * 0.32 + quote.turnover_pct * 0.22 + max(0.0, (quote.fair_value - quote.price) / max(0.01, quote.price) * 100) * 0.34,
        )
        held = self.state.player.portfolio.get(preferred.symbol, 0)
        total_funds = max(1, self.state.player.cash + self.state.player.deposit_balance)
        current_equity = 0
        for symbol, shares in self.state.player.portfolio.items():
            quote = self._quote(symbol)
            if quote is not None:
                current_equity += int(round(quote.price * shares))
        reserve_cash = max(40, int(total_funds * 0.22))
        max_exposure = int(total_funds * max(0.28, min(0.46, 0.32 + (self.state.player.risk_appetite - 50) / 260)))
        if held > 0 and (preferred.day_change_pct >= 4.8 or preferred.change_pct <= -2.0):
            return (preferred.symbol, "sell", min(held, 2), "观察模式下先做一次止盈或止损。")
        if current_equity >= max_exposure:
            for symbol, shares in sorted(self.state.player.portfolio.items(), key=lambda item: item[1], reverse=True):
                if shares > 0:
                    return (symbol, "sell", min(shares, 2), "当前仓位已经偏重，先降一点风险。")
        if self.state.player.cash >= preferred.price and self.state.player.cash > reserve_cash:
            budget = min(max(0, self.state.player.cash - reserve_cash), 18 + self.state.player.risk_appetite // 3)
            shares = max(1, min(4, int(budget // preferred.price)))
            if shares > 0:
                return (preferred.symbol, "buy", shares, "观察模式下，玩家判断这条线值得先小仓位试试。")
        for symbol, shares in self.state.player.portfolio.items():
            if shares > 0:
                return (symbol, "sell", min(shares, 2), "手头现金偏紧，先卖一点。")
        return (preferred.symbol, "buy", 0, "现金不足")

    def _execute_trade_for_player(self, symbol: str, side: str, shares: int, manual: bool, reason: str = "") -> bool:
        quote = self._quote(symbol)
        if quote is None:
            if manual:
                raise ValueError(f"不存在股票代码 {symbol}。")
            return False
        if shares <= 0:
            if manual:
                raise ValueError("至少要买卖 1 股。")
            return False
        amount = int(round(quote.price * shares))
        if side == "buy":
            affordable = int(self.state.player.cash // quote.price)
            shares = min(shares, affordable)
            if shares <= 0:
                if manual:
                    raise ValueError("现金不够，买不了这么多。")
                return False
            amount = int(round(quote.price * shares))
            self.state.player.cash -= amount
            self.state.player.portfolio[symbol] = self.state.player.portfolio.get(symbol, 0) + shares
            self.state.player.last_trade_summary = f"买入 {quote.name} {shares} 股，花了 ${amount}。"
        else:
            held = self.state.player.portfolio.get(symbol, 0)
            shares = min(shares, held)
            if shares <= 0:
                if manual:
                    raise ValueError("你手里没有这么多可卖的仓位。")
                return False
            amount = int(round(quote.price * shares))
            self.state.player.portfolio[symbol] = held - shares
            if self.state.player.portfolio[symbol] <= 0:
                self.state.player.portfolio.pop(symbol, None)
            self.state.player.cash += amount
            self.state.player.last_trade_summary = f"卖出 {quote.name} {shares} 股，回收 ${amount}。"
        market_tax = self._collect_tax(
            payer_type="player",
            payer_id=self.state.player.id,
            payer_name=self.state.player.name,
            revenue_key="market",
            label="证券交易",
            base_amount=amount,
            rate_pct=self.state.government.securities_tax_rate_pct,
        )
        self.state.player.last_trade_summary = f"{self.state.player.last_trade_summary[:-1]}，另缴税 ${market_tax}。"
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"你{'买入' if side == 'buy' else '卖出'}了 {quote.name}",
                summary=f"你在白天盘中{'买入' if side == 'buy' else '卖出'} {shares} 股 {quote.name}，金额约 ${amount}。{reason}",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]
        self._log(
            "player_market_trade",
            trade={"symbol": symbol, "name": quote.name, "side": side, "shares": shares, "amount": amount, "manual": manual, "reason": reason},
        )
        self._append_finance_record(
            actor_id=self.state.player.id,
            actor_name=self.state.player.name,
            category="market",
            action="buy" if side == "buy" else "sell",
            summary=f"你{'买入' if side == 'buy' else '卖出'}了 {quote.name} {shares} 股，金额约 ${amount}，税费 ${market_tax}。",
            amount=amount + market_tax if side == 'buy' else max(0, amount - market_tax),
            asset_name=quote.name,
            counterparty="Pixel Exchange",
        )
        quote.volume = max(0, (quote.volume or 0) + shares)
        quote.turnover_pct = round((quote.volume / max(1, quote.shares_outstanding or BASE_SHARES_OUTSTANDING.get(symbol, 100000))) * 100, 2)
        quote.volatility_score = round(max(0.55, min(2.8, quote.volatility_score * 0.96 + shares * 0.02)), 2)
        self._refresh_market_microstructure()
        self._update_index_history(append=False)
        self._update_daily_index_history()
        self._refresh_tasks()
        return True

    def _find_loan_parties(self, loan: LoanRecord) -> tuple[Agent | None, Agent | None]:
        lender = next((agent for agent in self.state.agents if agent.id == loan.lender_id), None)
        borrower = next((agent for agent in self.state.agents if agent.id == loan.borrower_id), None)
        return lender, borrower

    def _loan_judgement_score(self, lender: Agent, borrower: Agent, amount_due: int) -> int:
        if borrower.credit_score <= 35:
            return -999
        score = lender.generosity
        score += lender.relations.get(borrower.id, 0) // 2
        score += borrower.relations.get(lender.id, 0) // 3
        score += (borrower.credit_score - 60) // 4
        score += 10 if borrower.id in lender.allies else 0
        score -= 14 if borrower.id in lender.rivals else 0
        score -= max(0, (amount_due - max(8, lender.cash // 3)) // 2)
        score -= borrower.state.stress // 18
        score += borrower.state.focus // 24
        outstanding = sum(1 for loan in self.state.loans if loan.borrower_id == borrower.id and loan.status in {"active", "overdue"})
        score -= outstanding * 10
        return score

    def _proposed_interest_rate(self, borrower: Agent) -> int:
        base = 4 + max(0, (borrower.money_urgency - 50) // 12) + max(0, (borrower.risk_appetite - 50) // 20)
        return max(2, min(18, base))

    def _create_loan(self, lender: Agent, borrower: Agent, principal: int, interest_rate: int, reason: str) -> LoanRecord:
        amount_due = principal + max(1, round(principal * interest_rate / 100))
        loan = LoanRecord(
            id=f"loan-{uuid4().hex[:8]}",
            lender_id=lender.id,
            borrower_id=borrower.id,
            principal=principal,
            interest_rate=interest_rate,
            amount_due=amount_due,
            start_day=self.state.day,
            due_day=self.state.day + 1,
            status="active",
            reason=reason,
        )
        self.state.loans.insert(0, loan)
        self.state.loans = self.state.loans[:20]
        self._append_finance_record(
            actor_id=borrower.id,
            actor_name=borrower.name,
            category="loan",
            action="borrow",
            summary=f"{borrower.name} 向 {lender.name} 借入 ${principal}，约定次日归还 ${amount_due}。",
            amount=principal,
            asset_name="人际借款",
            counterparty=lender.name,
            interest_rate=float(interest_rate),
        )
        return loan

    def _repay_loan(self, loan: LoanRecord, borrower: Agent, lender: Agent) -> None:
        payment = min(borrower.cash, loan.amount_due)
        if payment <= 0:
            loan.status = "overdue"
            borrower.credit_score = max(0, borrower.credit_score - 12)
            self._adjust_relation(borrower, lender, -4, "借款到期却没有还上。")
            self._append_dialogue_record(
                DialogueRecord(
                    id=f"dialogue-{uuid4().hex[:8]}",
                    kind="loan",
                    day=self.state.day,
                    time_slot=self.state.time_slot,
                    participants=[borrower.id, lender.id],
                    participant_names=[borrower.name, lender.name],
                    topic="借款清算",
                    summary=f"{borrower.name} 到了还款时点却一分钱也没还上，{lender.name} 这边直接记成逾期。",
                    key_point=f"{borrower.name} 信用受损，{lender.name} 对这笔钱的耐心明显下降。",
                    transcript=[f"{borrower.name}：我今天还不上。", f"{lender.name}：这笔先记逾期。"],
                    desire_labels={
                        borrower.name: DESIRE_LABELS.get(dominant_desire_for_agent(self.state, borrower)[0], "缓解钱压"),
                        lender.name: DESIRE_LABELS.get(dominant_desire_for_agent(self.state, lender)[0], "守住节奏"),
                    },
                    mood="tense",
                    financial_note=f"未归还，剩余应付 ${loan.amount_due}，约定利率 {loan.interest_rate}%",
                    interest_rate=loan.interest_rate,
                    gray_trade=False,
                )
            )
            self._log(
                "loan_repayment",
                loan={"id": loan.id, "status": loan.status, "remaining_due": loan.amount_due, "payment": 0},
                lender={"id": lender.id, "name": lender.name},
                borrower={"id": borrower.id, "name": borrower.name},
            )
            return
        borrower.cash -= payment
        lender.cash += payment
        loan.amount_due -= payment
        if loan.amount_due <= 0:
            loan.amount_due = 0
            loan.status = "repaid"
            borrower.credit_score = min(100, borrower.credit_score + 4)
            self.state.lab.reputation = self._bounded(self.state.lab.reputation + 2)
            borrower.last_interaction = f"刚把欠 {lender.name} 的钱还清了。"
            lender.last_interaction = f"{borrower.name} 刚把借款还清了。"
            self._adjust_relation(borrower, lender, 3, "借款按时还清。")
        else:
            loan.status = "overdue"
            borrower.credit_score = max(0, borrower.credit_score - 8)
            borrower.last_interaction = f"只先还了 {lender.name} 一部分钱，还差 ${loan.amount_due}。"
            lender.last_interaction = f"{borrower.name} 只还了一部分钱，还差 ${loan.amount_due}。"
            self._adjust_relation(borrower, lender, -3, "借款到期后没有全部还清。")
        self._remember(borrower, f"你今天向 {lender.name} 归还了借款 ${payment}。", 2)
        self._remember(lender, f"{borrower.name} 今天归还了你借款 ${payment}。", 2)
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="loan",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=[borrower.id, lender.id],
                participant_names=[borrower.name, lender.name],
                topic="借款清算",
                summary=(
                    f"{borrower.name} 早上归还了 {lender.name} ${payment}。"
                    if loan.status == "repaid"
                    else f"{borrower.name} 只先还了 {lender.name} ${payment}，这笔还没彻底结清。"
                ),
                key_point=(
                    f"这笔借款已经结清，信用略有修复。"
                    if loan.status == "repaid"
                    else f"还剩 ${loan.amount_due} 没还，关系和口碑都会继续受压。"
                ),
                transcript=[
                    f"{borrower.name}：今天先还你 ${payment}。",
                    f"{lender.name}：{'这笔清了。' if loan.status == 'repaid' else f'还差 ${loan.amount_due}。'}",
                ],
                desire_labels={
                    borrower.name: DESIRE_LABELS.get(dominant_desire_for_agent(self.state, borrower)[0], "缓解钱压"),
                    lender.name: DESIRE_LABELS.get(dominant_desire_for_agent(self.state, lender)[0], "守住节奏"),
                },
                mood="warm" if loan.status == "repaid" else "tense",
                financial_note=f"已归还 ${payment}，剩余 ${loan.amount_due}，约定利率 {loan.interest_rate}%",
                interest_rate=loan.interest_rate,
                gray_trade=False,
            )
        )
        self._log(
            "loan_repayment",
            loan={"id": loan.id, "status": loan.status, "remaining_due": loan.amount_due, "payment": payment},
            lender={"id": lender.id, "name": lender.name},
            borrower={"id": borrower.id, "name": borrower.name},
        )
        if payment > 0:
            self._append_finance_record(
                actor_id=borrower.id,
                actor_name=borrower.name,
                category="loan",
                action="repay",
                summary=f"{borrower.name} 向 {lender.name} 归还了 ${payment}，剩余 ${loan.amount_due}。",
                amount=payment,
                asset_name="人际借款",
                counterparty=lender.name,
                interest_rate=float(loan.interest_rate),
            )

    def _settle_due_loans(self) -> None:
        for loan in self.state.loans:
            if loan.status not in {"active", "overdue"} or loan.due_day > self.state.day or self.state.time_slot != "morning":
                continue
            lender, borrower = self._find_loan_parties(loan)
            if lender is None or borrower is None:
                continue
            previous_status = loan.status
            self._repay_loan(loan, borrower, lender)
            if previous_status != loan.status or loan.status == "repaid":
                summary = (
                    f"{borrower.name} 在早上归还了 {lender.name} 的借款。"
                    if loan.status == "repaid"
                    else f"{borrower.name} 只还了一部分给 {lender.name}，剩余 ${loan.amount_due}。"
                )
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=f"{borrower.name} 处理了一笔借款",
                        summary=summary,
                        slot=self.state.time_slot,
                        category="general",
                    ),
                )
                self.state.events = self.state.events[:8]

    def _bank_regime_adjustment(self) -> float:
        regime = self.state.market.regime or "bull"
        return {"bull": -0.25, "sideways": 0.35, "risk": 1.1}.get(regime, 0.2)

    def _refresh_bank_state(self) -> None:
        active_loans = [loan for loan in self.state.bank_loans if loan.status in {"active", "overdue"}]
        overdue_count = sum(1 for loan in active_loans if loan.status == "overdue")
        liquidity_pressure = 0.9 if self.state.bank.liquidity <= 420 else 0.45 if self.state.bank.liquidity <= 820 else 0.0
        default_pressure = min(2.6, overdue_count * 0.65 + self.state.bank.defaults_count * 0.08)
        reputation_tilt = 0.35 if self.state.lab.reputation <= 18 else -0.15 if self.state.lab.reputation >= 62 else 0.0
        self.state.bank.risk_spread_pct = round(max(0.0, min(4.5, 0.2 + liquidity_pressure + default_pressure + reputation_tilt)), 2)
        regime = self.state.market.regime or "bull"
        regime_boost = {"bull": -0.04, "sideways": 0.06, "risk": 0.14}.get(regime, 0.05)
        liquidity_boost = 0.18 if self.state.bank.liquidity <= 420 else 0.09 if self.state.bank.liquidity <= 820 else -0.02
        spread_boost = self.state.bank.risk_spread_pct * 0.08
        self.state.bank.deposit_daily_rate_pct = round(max(0.06, min(1.25, self.state.bank.base_deposit_daily_rate_pct + regime_boost + liquidity_boost + spread_boost)), 2)

    def _bank_offer_rate(self, credit_score: int, term_days: int) -> tuple[float, float]:
        base_daily = self.state.bank.base_daily_rate_pct + self.state.bank.risk_spread_pct + self._bank_regime_adjustment()
        term_premium = {1: 0.2, 2: 0.45, 3: 0.8}.get(term_days, 0.8)
        if credit_score >= 85:
            credit_premium = -0.55
        elif credit_score >= 70:
            credit_premium = 0.0
        elif credit_score >= 55:
            credit_premium = 0.9
        elif credit_score >= 40:
            credit_premium = 2.2
        else:
            credit_premium = 4.0
        reputation_premium = 0.45 if self.state.lab.reputation <= 22 else 0.0
        daily_rate = max(0.8, min(9.5, round(base_daily + term_premium + credit_premium + reputation_premium, 2)))
        total_rate = round(daily_rate * term_days, 2)
        return daily_rate, total_rate

    def _bank_holder_name(self, holder_type: str, holder_id: str) -> str:
        if holder_type == "player":
            return self.state.player.name
        return self._find_agent(holder_id).name

    def _bank_holder_deposit_balance(self, holder_type: str, holder_id: str) -> int:
        if holder_type == "player":
            return self.state.player.deposit_balance
        return self._find_agent(holder_id).deposit_balance

    def _adjust_bank_holder_deposit(self, holder_type: str, holder_id: str, delta: int) -> None:
        if holder_type == "player":
            self.state.player.deposit_balance = max(0, self.state.player.deposit_balance + delta)
            return
        holder = self._find_agent(holder_id)
        holder.deposit_balance = max(0, holder.deposit_balance + delta)

    def _bank_deposit(self, holder_type: str, holder_id: str, amount: int, *, manual: bool = False, reason: str = "") -> int:
        if amount <= 0:
            raise ValueError("存款金额必须大于 0。")
        holder_name, cash = self._bank_borrower_cash_ref(holder_type, holder_id)
        if cash < amount:
            raise ValueError("手头现金不够，存不了这么多。")
        self._adjust_bank_borrower_cash(holder_type, holder_id, -amount)
        self._adjust_bank_holder_deposit(holder_type, holder_id, amount)
        self.state.bank.liquidity += amount
        self.state.bank.total_deposits += amount
        self._append_finance_record(
            actor_id=holder_id,
            actor_name=holder_name,
            category="bank",
            action="deposit",
            summary=f"{holder_name} 向 {self.state.bank.name} 存入了 ${amount}。",
            amount=amount,
            asset_name="银行存款",
            counterparty=self.state.bank.name,
            interest_rate=self.state.bank.deposit_daily_rate_pct,
        )
        if holder_type == "player":
            self.state.player.last_trade_summary = f"你刚向{self.state.bank.name}存入了 ${amount}，当前日利率 {self.state.bank.deposit_daily_rate_pct:.2f}%。"
        else:
            holder = self._find_agent(holder_id)
            holder.last_trade_summary = f"刚往{self.state.bank.name}存入 ${amount}，先把现金放稳。"
        self._log("bank_deposit", holder={"type": holder_type, "id": holder_id, "name": holder_name}, amount=amount, manual=manual)
        self._refresh_bank_state()
        return amount

    def _bank_withdraw(self, holder_type: str, holder_id: str, amount: int, *, manual: bool = False, reason: str = "") -> int:
        if amount <= 0:
            raise ValueError("取款金额必须大于 0。")
        balance = self._bank_holder_deposit_balance(holder_type, holder_id)
        if balance < amount:
            raise ValueError("存款余额不够，取不了这么多。")
        if self.state.bank.liquidity < amount:
            raise ValueError("银行当前流动性不足，这笔取款暂时提不出来。")
        holder_name = self._bank_holder_name(holder_type, holder_id)
        self._adjust_bank_holder_deposit(holder_type, holder_id, -amount)
        self._adjust_bank_borrower_cash(holder_type, holder_id, amount)
        self.state.bank.liquidity = max(0, self.state.bank.liquidity - amount)
        self.state.bank.total_deposits = max(0, self.state.bank.total_deposits - amount)
        self._append_finance_record(
            actor_id=holder_id,
            actor_name=holder_name,
            category="bank",
            action="withdraw",
            summary=f"{holder_name} 从 {self.state.bank.name} 取出了 ${amount}。",
            amount=amount,
            asset_name="银行存款",
            counterparty=self.state.bank.name,
            interest_rate=self.state.bank.deposit_daily_rate_pct,
        )
        if holder_type == "player":
            self.state.player.last_trade_summary = f"你刚从{self.state.bank.name}取出 ${amount}，回到现金账户。"
        else:
            holder = self._find_agent(holder_id)
            holder.last_trade_summary = f"刚从{self.state.bank.name}取出 ${amount}，准备当现金用。"
        self._log("bank_withdraw", holder={"type": holder_type, "id": holder_id, "name": holder_name}, amount=amount, manual=manual)
        self._refresh_bank_state()
        return amount

    def _settle_bank_deposit_interest(self) -> None:
        if self.state.time_slot != "morning":
            return
        rate = self.state.bank.deposit_daily_rate_pct
        for holder_type, holder_id, holder_name, balance in [
            ("player", self.state.player.id, self.state.player.name, self.state.player.deposit_balance),
            *[( "agent", agent.id, agent.name, agent.deposit_balance) for agent in self.state.agents],
        ]:
            if balance <= 0:
                continue
            interest = max(1, round(balance * rate / 100))
            if self.state.bank.liquidity < interest:
                interest = max(0, min(interest, self.state.bank.liquidity))
            if interest <= 0:
                continue
            self._adjust_bank_holder_deposit(holder_type, holder_id, interest)
            self.state.bank.liquidity = max(0, self.state.bank.liquidity - interest)
            self.state.bank.total_interest_paid += interest
            self.state.bank.total_deposits += interest
            self._append_finance_record(
                actor_id=holder_id,
                actor_name=holder_name,
                category="bank",
                action="interest",
                summary=f"{holder_name} 从 {self.state.bank.name} 收到存款利息 ${interest}。",
                amount=interest,
                asset_name="银行存款",
                counterparty=self.state.bank.name,
                interest_rate=rate,
            )
        self._refresh_bank_state()

    def _bank_credit_line(self, borrower_type: str, borrower_id: str, credit_score: int) -> int:
        if borrower_type == "player":
            total_assets = self._player_total_assets()
            deposit_balance = self.state.player.deposit_balance
        else:
            borrower = self._find_agent(borrower_id)
            total_assets = self._agent_total_assets(borrower)
            deposit_balance = borrower.deposit_balance
        outstanding = self._bank_liability_for(borrower_type, borrower_id)
        if credit_score >= 85:
            base_limit = 10000
            asset_ratio = 0.18
        elif credit_score >= 70:
            base_limit = 7000
            asset_ratio = 0.14
        elif credit_score >= 55:
            base_limit = 4500
            asset_ratio = 0.10
        elif credit_score >= 40:
            base_limit = 2500
            asset_ratio = 0.07
        else:
            base_limit = 1200
            asset_ratio = 0.04
        asset_boost = int(max(0, total_assets) * asset_ratio)
        deposit_boost = int(max(0, deposit_balance) * 0.35)
        liquidity_cap = max(1800, min(24000, int(self.state.bank.liquidity * 0.16)))
        limit = max(600, base_limit + asset_boost + deposit_boost - outstanding)
        return max(600, min(24000, min(limit, liquidity_cap)))

    def _borrower_bank_loans(self, borrower_type: str, borrower_id: str) -> list[BankLoanRecord]:
        return [
            loan
            for loan in self.state.bank_loans
            if loan.borrower_type == borrower_type and loan.borrower_id == borrower_id and loan.status in {"active", "overdue"}
        ]

    def _bank_borrower_cash_ref(self, borrower_type: str, borrower_id: str) -> tuple[str, int]:
        if borrower_type == "player":
            return self.state.player.name, self.state.player.cash
        borrower = self._find_agent(borrower_id)
        return borrower.name, borrower.cash

    def _adjust_bank_borrower_cash(self, borrower_type: str, borrower_id: str, delta: int) -> None:
        if borrower_type == "player":
            self.state.player.cash = max(0, self.state.player.cash + delta)
            return
        borrower = self._find_agent(borrower_id)
        borrower.cash = max(0, borrower.cash + delta)

    def _adjust_bank_borrower_credit(self, borrower_type: str, borrower_id: str, delta: int) -> None:
        if borrower_type == "player":
            self.state.player.credit_score = self._bounded(self.state.player.credit_score + delta)
            return
        borrower = self._find_agent(borrower_id)
        borrower.credit_score = self._bounded(borrower.credit_score + delta)

    def _bank_borrower_display_name(self, borrower_type: str, borrower_id: str) -> str:
        if borrower_type == "player":
            return self.state.player.name
        return self._find_agent(borrower_id).name

    def _bank_can_lend(self, borrower_type: str, borrower_id: str, credit_score: int, amount: int) -> None:
        if amount <= 0:
            raise ValueError("借款金额至少要大于 0。")
        active = self._borrower_bank_loans(borrower_type, borrower_id)
        if any(loan.status == "overdue" for loan in active):
            raise ValueError("你当前有逾期银行贷款，银行不会继续放款。")
        if len(active) >= 2:
            raise ValueError("当前银行只允许你同时持有最多 2 笔未结清贷款。")
        limit = self._bank_credit_line(borrower_type, borrower_id, credit_score)
        if amount > limit:
            raise ValueError(f"按当前信用，这次最多只能向银行借 ${limit}。")
        if amount > self.state.bank.liquidity:
            raise ValueError("银行当前流动性不够，这笔暂时批不下来。")

    def _create_bank_loan(self, borrower_type: str, borrower_id: str, borrower_name: str, principal: int, term_days: int, reason: str, credit_score: int) -> BankLoanRecord:
        daily_rate, total_rate = self._bank_offer_rate(credit_score, term_days)
        amount_due = principal + max(1, round(principal * total_rate / 100))
        loan = BankLoanRecord(
            id=f"bank-{uuid4().hex[:8]}",
            borrower_type=borrower_type,
            borrower_id=borrower_id,
            borrower_name=borrower_name,
            principal=principal,
            daily_rate_pct=daily_rate,
            total_rate_pct=total_rate,
            amount_due=amount_due,
            start_day=self.state.day,
            due_day=self.state.day + term_days,
            term_days=term_days,
            status="active",
            reason=reason,
        )
        self.state.bank_loans.insert(0, loan)
        self.state.bank_loans = self.state.bank_loans[:40]
        self.state.bank.liquidity = max(0, self.state.bank.liquidity - principal)
        self.state.bank.total_issued += principal
        self._refresh_bank_state()
        return loan

    def _append_bank_dialogue_record(self, loan: BankLoanRecord, summary: str, key_point: str, mood: str, transcript: list[str], amount_paid: int = 0) -> None:
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="bank_loan",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=[loan.borrower_id],
                participant_names=[loan.borrower_name, self.state.bank.name],
                topic="银行借贷",
                summary=summary,
                key_point=key_point,
                transcript=transcript,
                desire_labels={
                    loan.borrower_name: "缓解钱压",
                    self.state.bank.name: "按信用定价",
                },
                mood=mood,
                financial_note=f"本金 ${loan.principal}，日利率 {loan.daily_rate_pct:.2f}%，总利率 {loan.total_rate_pct:.2f}%，剩余 ${loan.amount_due}，本次处理 ${amount_paid}",
                interest_rate=int(round(loan.total_rate_pct)),
                gray_trade=False,
            )
        )

    def _bank_borrow(self, borrower_type: str, borrower_id: str, amount: int, term_days: int, reason: str, manual: bool = False) -> BankLoanRecord:
        credit_score = self.state.player.credit_score if borrower_type == "player" else self._find_agent(borrower_id).credit_score
        borrower_name = self._bank_borrower_display_name(borrower_type, borrower_id)
        self._bank_can_lend(borrower_type, borrower_id, credit_score, amount)
        loan = self._create_bank_loan(borrower_type, borrower_id, borrower_name, amount, term_days, reason, credit_score)
        self._adjust_bank_borrower_cash(borrower_type, borrower_id, amount)
        self._adjust_bank_borrower_credit(borrower_type, borrower_id, 1 if credit_score >= 70 else 0)
        if borrower_type == "player":
            self.state.player.last_trade_summary = f"从{self.state.bank.name}借入 ${amount}，{term_days} 天后还 ${loan.amount_due}。"
        else:
            borrower = self._find_agent(borrower_id)
            borrower.last_trade_summary = f"向{self.state.bank.name}借入 ${amount}，{term_days} 天后应还 ${loan.amount_due}。"
            borrower.current_bubble = "我先去银行周转一下。"
            self._remember(borrower, f"你刚从{self.state.bank.name}借入 ${amount}，{term_days} 天后要还 ${loan.amount_due}。", 2)
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"{borrower_name} 向银行借了一笔钱",
                summary=f"{borrower_name} 刚从{self.state.bank.name}借到 ${amount}，期限 {term_days} 天，总利率 {loan.total_rate_pct:.2f}%。",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]
        self._append_bank_dialogue_record(
            loan,
            summary=self._natural_bank_borrow_summary(borrower_name, self.state.bank.name, amount, term_days, loan.amount_due),
            key_point=f"银行按当前信用给出 {loan.total_rate_pct:.2f}% 总利率，借款已经到账。",
            mood="warm" if credit_score >= 70 else "neutral",
            transcript=[f"{self.state.bank.name}：这笔可以批，按 {loan.total_rate_pct:.2f}% 总利率走。"] if borrower_type == "player" else [f"{borrower_name}：先借 ${amount} 周转。"],
        )
        self._append_finance_record(
            actor_id=borrower_id,
            actor_name=borrower_name,
            category="bank",
            action="borrow",
            summary=f"{borrower_name} 从 {self.state.bank.name} 借入 ${amount}，期限 {term_days} 天，应还 ${loan.amount_due}。",
            amount=amount,
            asset_name="银行贷款",
            counterparty=self.state.bank.name,
            interest_rate=loan.total_rate_pct,
            financed=True,
        )
        self._log(
            "bank_loan_created",
            loan={"id": loan.id, "borrower_type": borrower_type, "borrower_id": borrower_id, "principal": amount, "term_days": term_days, "amount_due": loan.amount_due},
            manual=manual,
        )
        self._refresh_bank_state()
        return loan

    def player_bank_borrow(self, amount: int, term_days: int) -> WorldState:
        self._bank_borrow("player", self.state.player.id, amount, term_days, "玩家主动申请银行贷款", manual=True)
        self._refresh_tasks()
        self._refresh_memory_streams()
        return self.state

    def player_bank_deposit(self, amount: int) -> WorldState:
        self._bank_deposit("player", self.state.player.id, amount, manual=True, reason="玩家主动存款")
        self._refresh_tasks()
        self._refresh_memory_streams()
        return self.state

    def player_bank_withdraw(self, amount: int) -> WorldState:
        self._bank_withdraw("player", self.state.player.id, amount, manual=True, reason="玩家主动取款")
        self._refresh_tasks()
        self._refresh_memory_streams()
        return self.state

    def _settle_bank_loan(self, loan: BankLoanRecord, payment_limit: int | None = None) -> int:
        borrower_name, borrower_cash = self._bank_borrower_cash_ref(loan.borrower_type, loan.borrower_id)
        target_payment = min(payment_limit if payment_limit is not None else loan.amount_due, loan.amount_due)
        deposit_balance = self._bank_holder_deposit_balance(loan.borrower_type, loan.borrower_id)
        if borrower_cash < target_payment and deposit_balance > 0:
            try:
                self._bank_withdraw(loan.borrower_type, loan.borrower_id, min(deposit_balance, target_payment - borrower_cash), reason="贷款到期前自动从存款补足还款现金。")
                borrower_name, borrower_cash = self._bank_borrower_cash_ref(loan.borrower_type, loan.borrower_id)
            except ValueError:
                pass
        payment = min(payment_limit if payment_limit is not None else borrower_cash, borrower_cash, loan.amount_due)
        if payment > 0:
            self._adjust_bank_borrower_cash(loan.borrower_type, loan.borrower_id, -payment)
            self.state.bank.liquidity += payment
            self.state.bank.total_repaid += payment
            loan.amount_due -= payment
        if loan.amount_due <= 0:
            loan.amount_due = 0
            loan.status = "repaid"
            self._adjust_bank_borrower_credit(loan.borrower_type, loan.borrower_id, 4)
            self.state.lab.reputation = self._bounded(self.state.lab.reputation + 1)
            summary = self._natural_bank_repay_summary(borrower_name, payment, 0)
            key_point = "按时还清后，信用略有回升。"
            mood = "warm"
        elif loan.status == "overdue":
            summary = self._natural_bank_repay_summary(borrower_name, payment, loan.amount_due)
            key_point = f"还剩 ${loan.amount_due}，逾期状态还没完全解除。"
            mood = "tense"
        elif self.state.day < loan.due_day:
            loan.status = "active"
            summary = self._natural_bank_repay_summary(borrower_name, payment, loan.amount_due)
            key_point = f"还剩 ${loan.amount_due}，这笔贷款还没到期。"
            mood = "neutral"
        else:
            penalty = max(1, round(loan.amount_due * 0.06))
            loan.amount_due += penalty
            loan.due_day = self.state.day + 1
            loan.status = "overdue"
            self._adjust_bank_borrower_credit(loan.borrower_type, loan.borrower_id, -10)
            self.state.bank.defaults_count += 1
            self.state.lab.reputation = self._bounded(self.state.lab.reputation - 1)
            summary = f"{borrower_name} 没能按时还清银行贷款，银行把剩余欠款滚到了明天。"
            key_point = f"还剩 ${loan.amount_due}，逾期后又加了一层罚息。"
            mood = "tense"
        self._append_bank_dialogue_record(
            loan,
            summary=summary,
            key_point=key_point,
            mood=mood,
            transcript=[f"{borrower_name}：这次先还 ${payment}。", f"{self.state.bank.name}：{'这笔已经结清。' if loan.status == 'repaid' else f'剩余 ${loan.amount_due}，已记逾期。'}"],
            amount_paid=payment,
        )
        if payment > 0:
            self._append_finance_record(
                actor_id=loan.borrower_id,
                actor_name=borrower_name,
                category="bank",
                action="repay",
                summary=f"{borrower_name} 向 {self.state.bank.name} 归还了 ${payment}，剩余 ${loan.amount_due}。",
                amount=payment,
                asset_name="银行贷款",
                counterparty=self.state.bank.name,
                interest_rate=loan.total_rate_pct,
                financed=True,
            )
        self._log(
            "bank_loan_repayment",
            loan={"id": loan.id, "status": loan.status, "remaining_due": loan.amount_due, "payment": payment},
        )
        self._refresh_bank_state()
        return payment

    def player_bank_repay(self, loan_id: str, amount: int | None = None) -> WorldState:
        loan = next((item for item in self.state.bank_loans if item.id == loan_id and item.borrower_type == "player"), None)
        if loan is None:
            raise KeyError(loan_id)
        if loan.status not in {"active", "overdue"}:
            raise ValueError("这笔银行贷款已经结清了。")
        if amount is not None and amount <= 0:
            raise ValueError("还款金额必须大于 0。")
        if self.state.player.cash <= 0 and self.state.player.deposit_balance <= 0:
            raise ValueError("你手头没有可用于归还银行贷款的现金或存款。")
        payment_limit = amount if amount is not None else None
        paid = self._settle_bank_loan(loan, payment_limit=payment_limit)
        if paid <= 0:
            raise ValueError("这次没有成功归还任何金额。")
        self.state.player.last_trade_summary = f"你刚向{self.state.bank.name}归还了 ${paid}。"
        self._refresh_tasks()
        self._refresh_memory_streams()
        return self.state

    def _settle_due_bank_loans(self) -> None:
        if self.state.time_slot != "morning":
            return
        for loan in self.state.bank_loans:
            if loan.status not in {"active", "overdue"} or loan.due_day > self.state.day:
                continue
            previous_status = loan.status
            self._settle_bank_loan(loan)
            if previous_status != loan.status or loan.status == "repaid":
                borrower_name = self._bank_borrower_display_name(loan.borrower_type, loan.borrower_id)
                summary = (
                    f"{borrower_name} 今早处理了一笔来自{self.state.bank.name}的贷款。"
                    if loan.status == "repaid"
                    else f"{borrower_name} 今早没能按时还清银行贷款，剩余 ${loan.amount_due}。"
                )
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=f"{borrower_name} 处理了一笔银行借款",
                        summary=summary,
                        slot=self.state.time_slot,
                        category="general",
                    ),
                )
                self.state.events = self.state.events[:8]

    def _trigger_bank_activity(self) -> None:
        if not self.state.market.is_open:
            return
        for agent in self.state.agents:
            baseline_need = (
                self.state.company.low_cash_threshold
                + agent.daily_cost_baseline * 5
                + max(0, agent.monthly_burden // 3)
            )
            severe_cash_stress = agent.cash < max(self.state.company.low_cash_threshold, baseline_need * 0.45)
            borrow_for_pressure = agent.cash < baseline_need or agent.money_urgency >= 62
            borrow_for_opportunity = (
                self.state.market.regime == "bull"
                and agent.risk_appetite >= 60
                and agent.credit_score >= 30
                and self._agent_total_assets(agent) >= 2500
                and agent.cash < 4800
            )
            leverage_borrow = (
                self.state.market.regime == "bull"
                and agent.risk_appetite >= 72
                and agent.credit_score >= 35
                and (agent.deposit_balance >= 1200 or self._agent_total_assets(agent) >= 8000)
                and agent.cash < max(4200, int(agent.deposit_balance * 0.08) if agent.deposit_balance else 4200)
            )
            if (
                agent.deposit_balance > 0
                and (severe_cash_stress or agent.money_urgency >= 86)
                and self.random.random() < 0.34
            ):
                try:
                    withdraw_target = min(
                        agent.deposit_balance,
                        max(8, min(max(18, baseline_need - agent.cash), max(18, agent.deposit_balance // 4))),
                    )
                    self._bank_withdraw("agent", agent.id, withdraw_target)
                    agent.current_bubble = "先把存款拿一点出来。"
                except ValueError:
                    pass
            active_loans = self._borrower_bank_loans("agent", agent.id)
            overdue = next((loan for loan in active_loans if loan.status == "overdue"), None)
            if overdue is not None and agent.cash >= max(8, overdue.amount_due // 3) and self.random.random() < 0.42:
                self._settle_bank_loan(overdue, payment_limit=min(agent.cash, overdue.amount_due))
                agent.current_bubble = "先把银行那边补一点。"
                agent.last_trade_summary = f"刚向{self.state.bank.name}补还了一笔贷款。"
                continue
            if active_loans:
                continue
            baseline_need = (
                self.state.company.low_cash_threshold
                + agent.daily_cost_baseline * 5
                + max(0, agent.monthly_burden // 3)
            )
            severe_cash_stress = agent.cash < max(self.state.company.low_cash_threshold, baseline_need * 0.45)
            borrow_for_pressure = (
                agent.cash < int(baseline_need * 1.15)
                or agent.money_urgency >= 55
                or agent.monthly_burden > max(120, agent.cash * 1.25)
            )
            borrow_for_opportunity = (
                self.state.market.regime == "bull"
                and agent.risk_appetite >= 60
                and agent.credit_score >= 30
                and self._agent_total_assets(agent) >= 2500
                and agent.cash < 4800
            )
            leverage_borrow = (
                self.state.market.regime == "bull"
                and agent.risk_appetite >= 72
                and agent.credit_score >= 35
                and (agent.deposit_balance >= 1200 or self._agent_total_assets(agent) >= 8000)
                and agent.cash < max(4200, int(agent.deposit_balance * 0.08) if agent.deposit_balance else 4200)
            )
            if not borrow_for_pressure and not borrow_for_opportunity and not leverage_borrow:
                continue
            borrow_chance = 0.58 if borrow_for_pressure else 0.26 if borrow_for_opportunity else 0.18
            if self.random.random() > borrow_chance:
                continue
            suggested_amount = max(
                320,
                min(
                    12000,
                    340
                    + max(0, baseline_need - agent.cash) * 18
                    + agent.money_urgency * 24
                    + max(0, agent.monthly_burden // 2)
                    + (800 if borrow_for_opportunity else 0)
                    + (1200 if leverage_borrow else 0),
                ),
            )
            amount = min(self._bank_credit_line("agent", agent.id, agent.credit_score), suggested_amount)
            term_days = 1 if agent.credit_score >= 70 else 2 if agent.credit_score >= 50 else 3
            try:
                self._bank_borrow(
                    "agent",
                    agent.id,
                    amount,
                    term_days,
                    "现金和体力都偏紧，先从银行周转。" if not leverage_borrow else "想留住手里的流动性，顺手借一点做周转和加仓。",
                )
            except ValueError:
                continue
            continue
        for agent in self.state.agents:
            reserve_floor = max(180, self.state.company.low_cash_threshold + agent.daily_cost_baseline * 9 + max(0, agent.monthly_burden // 2))
            if agent.cash <= reserve_floor or agent.money_urgency >= 56 or agent.is_resting:
                continue
            if self.random.random() > 0.1:
                continue
            amount = min(max(10, int(agent.cash * 0.1)), max(0, agent.cash - reserve_floor))
            if amount <= 0:
                continue
            try:
                self._bank_deposit("agent", agent.id, amount, reason="把暂时不用的现金先放进银行。")
                agent.current_bubble = "先存一笔，别全放手上。"
            except ValueError:
                continue

    def _run_tourism_activity(self) -> None:
        self._refresh_tourist_turnover()
        if self.state.time_slot != "night":
            self._maybe_spawn_tourist()
        self._rebalance_tourist_activity()
        self._move_tourists()
        self._trigger_tourist_spending()
        self._trigger_tourist_investment()
        self._trigger_tourist_market_exit()
        self._trigger_tourist_market_investment()
        self._trigger_tourist_conversations()
        self._trigger_tourist_signals()

    def _active_tourists(self) -> list[TouristAgent]:
        return [tourist for tourist in (self.state.tourists or []) if getattr(tourist, "active_in_scene", True)]

    def _active_tourist_count(self) -> int:
        return len(self._active_tourists())

    def _rebalance_tourist_activity(self) -> None:
        tourists = self.state.tourists or []
        if not tourists:
            return
        cap = max(1, min(getattr(self.state.tourism, "active_visitor_cap", 7), len(tourists)))
        prioritized = sorted(
            tourists,
            key=lambda tourist: (
                1 if tourist.visitor_tier == "vip" else 0,
                1 if tourist.visitor_tier == "buyer" else 0,
                1 if tourist.visitor_tier == "repeat" else 0,
                1 if tourist.property_interest else 0,
                1 if tourist.market_portfolio else 0,
                tourist.message_influence,
                min(4, len(tourist.short_term_memory or [])),
                tourist.cash + tourist.budget,
                tourist.mood,
            ),
            reverse=True,
        )
        active_ids = {tourist.id for tourist in prioritized[:cap]}
        for tourist in tourists:
            tourist.active_in_scene = tourist.id in active_ids

    def _trigger_tourist_market_investment(self) -> None:
        if not self.state.market.is_open or not self.state.market.stocks:
            return
        hot_market_buzz = any(
            post.category in {"market", "tourism", "property"} and (post.heat or 0) >= 18
            for post in (self.state.feed_timeline or [])[:18]
        )
        for tourist in self._active_tourists():
            if tourist.visitor_tier not in {"vip", "buyer", "repeat", "regular"}:
                continue
            if tourist.market_last_action.startswith("刚把"):
                continue
            minimum_cash = {
                "vip": 70,
                "buyer": 65,
                "repeat": 55,
                "regular": 45,
            }.get(tourist.visitor_tier, 70)
            if tourist.cash < minimum_cash:
                continue
            if tourist.current_location not in {"market", "meeting", "data_wall", "lounge", "foyer"}:
                continue
            base_chance = {
                "vip": 0.16,
                "buyer": 0.11,
                "repeat": 0.05,
                "regular": 0.04,
            }.get(tourist.visitor_tier, 0.04)
            chance = base_chance + max(0.0, self.state.market.sentiment / 420)
            if self.state.market.regime == "bull":
                chance += 0.05
            if hot_market_buzz:
                chance += 0.06
            if tourist.favorite_topic in {"股票", "房价", "GeoAI"}:
                chance += 0.04
            if tourist.property_interest:
                chance += 0.02
            if tourist.mood >= 72:
                chance += 0.025
            if self.random.random() > chance:
                continue
            preferred_symbol, preference_note = self._tourist_preferred_market_symbol(tourist)
            quote = max(
                self.state.market.stocks,
                key=lambda item: (
                    item.change_pct
                    + item.turnover_pct * 0.22
                    + max(0.0, (item.fair_value - item.price) / max(0.01, item.price) * 100) * 0.18
                    + (0.75 if item.symbol == preferred_symbol else 0.0)
                ),
            )
            budget_floor = {
                "vip": 120,
                "buyer": 90,
                "repeat": 60,
                "regular": 28,
            }.get(tourist.visitor_tier, 80)
            budget_ceiling = {
                "vip": 320,
                "buyer": 240,
                "repeat": 140,
                "regular": 72,
            }.get(tourist.visitor_tier, 180)
            budget = min(tourist.cash, self.random.randint(budget_floor, budget_ceiling))
            shares = max(1, int(budget // max(1.0, quote.price)))
            cost = int(round(shares * quote.price))
            if cost <= 0 or cost > tourist.cash:
                continue
            tourist.cash -= cost
            tourist.market_portfolio[quote.symbol] = tourist.market_portfolio.get(quote.symbol, 0) + shares
            tourist.market_cost_basis[quote.symbol] = tourist.market_cost_basis.get(quote.symbol, 0) + cost
            tourist.market_invested_total = sum(tourist.market_cost_basis.values())
            tourist.market_preference = preferred_symbol or quote.symbol
            tourist.market_preference_note = preference_note
            tourist.market_last_action = f"刚拿 ${cost} 买了 {quote.symbol} {shares} 股。"
            tourist.mood = self._bounded(tourist.mood + 3)
            tourist.current_activity = f"刚通过外部券商小仓位买了 {quote.symbol}，想看看这波热度还能不能再冲一段。"
            tourist.brief_note = (
                f"{'这位高消费客户' if tourist.visitor_tier == 'vip' else '这位看房游客'}刚拿出 ${cost} 买了点 {quote.symbol}，"
                "已经开始把这里当成能顺手下注的小市场。"
            )
            self._apply_quote_move(quote.symbol, min(2.4, max(0.4, cost / 420)), f"受 {tourist.name} 的场外追单影响")
            quote.volume = max(quote.volume or 0, (quote.volume or 0) + shares)
            quote.turnover_pct = round((quote.volume / max(1, quote.shares_outstanding or BASE_SHARES_OUTSTANDING.get(quote.symbol, 100000))) * 100, 2)
            self._refresh_market_microstructure()
            self._update_index_history()
            self._update_daily_index_history()
            self._append_finance_record(
                actor_id=tourist.id,
                actor_name=tourist.name,
                category="market",
                action="invest",
                summary=f"{tourist.name} 通过外部券商买入 {quote.name} {shares} 股，投入 ${cost}，准备继续盯着这里的市场风向。",
                amount=cost,
                asset_name=quote.name,
                counterparty="外部券商",
            )
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{tourist.name} 小仓位买入了 {quote.symbol}",
                    summary=f"{tourist.name} 刚花 ${cost} 小仓位买入 {quote.name}，游客里开始有人把这里当成可以顺手追单的小市场。",
                    slot=self.state.time_slot,
                    category="market",
                ),
            )
            self.state.events = self.state.events[:8]
            post = FeedPost(
                id=f"feed-{uuid4().hex[:8]}",
                author_type="tourist",
                author_id=tourist.id,
                author_name=tourist.name,
                day=self.state.day,
                time_slot=self.state.time_slot,
                category="market",
                mood="spark",
                content=self._clean_feed_text(
                    f"我刚拿了 ${cost} 去试 {quote.symbol}。如果这里接下来还热，我可能会继续加一点；要是气氛一冷，我也会跑得很快。"
                ),
                topic_tags=[quote.symbol, "游客投机", "市场风向", "场外小仓位"],
                desire_tags=["想试水", "追风向"],
                likes=6 + self.random.randint(0, 5),
                views=54 + self.random.randint(0, 36),
                summary="有游客开始把这里当成可以试水投机的小市场。",
                impacts=["影响市场", "影响游客讨论"],
            )
            post.credibility = self._feed_credibility_for_post(post)
            post.heat = self._compute_feed_heat(post)
            self._append_feed_post(post, remember=True, apply_impacts=True)
            self._log(
                "tourist_market_invest",
                tourist={"id": tourist.id, "name": tourist.name, "tier": tourist.visitor_tier},
                quote={"symbol": quote.symbol, "name": quote.name, "shares": shares, "cost": cost},
            )

    def _trigger_tourist_market_exit(self) -> None:
        if not self.state.market.is_open or not self.state.market.stocks:
            return
        for tourist in self._active_tourists():
            positions = [(symbol, shares) for symbol, shares in (tourist.market_portfolio or {}).items() if shares > 0]
            if not positions:
                continue
            negative_buzz = any(post.category in {"market", "policy", "gossip"} and post.mood == "tense" and post.heat >= 18 for post in (self.state.feed_timeline or [])[:18])
            tight_cash = tourist.cash <= 28
            leaving_soon = tourist.stay_until_day - self.state.day <= 1
            chance = 0.0
            if tight_cash:
                chance += 0.18
            if leaving_soon:
                chance += 0.14
            if self.state.market.regime == "risk":
                chance += 0.08
            if negative_buzz:
                chance += 0.08
            if tourist.mood <= 45:
                chance += 0.05
            chance += 0.04
            if self.random.random() > chance:
                continue
            preferred_symbol, preference_note = self._tourist_preferred_market_symbol(tourist)
            symbol, shares = max(
                positions,
                key=lambda item: (
                    1 if item[0] != preferred_symbol else 0,
                    item[1],
                ),
            )
            quote = next((stock for stock in self.state.market.stocks if stock.symbol == symbol), None)
            if quote is None:
                continue
            sell_shares = max(1, shares if (tight_cash or leaving_soon) else max(1, shares // 2))
            proceeds = int(round(sell_shares * quote.price))
            cost_basis = tourist.market_cost_basis.get(symbol, 0)
            avg_cost = cost_basis / max(1, shares)
            realized_cost = int(round(avg_cost * sell_shares))
            tourist.cash += proceeds
            remaining = max(0, shares - sell_shares)
            if remaining <= 0:
                tourist.market_portfolio.pop(symbol, None)
                tourist.market_cost_basis.pop(symbol, None)
            else:
                tourist.market_portfolio[symbol] = remaining
                tourist.market_cost_basis[symbol] = max(0, cost_basis - realized_cost)
            tourist.market_invested_total = sum(tourist.market_cost_basis.values())
            tourist.market_last_action = f"刚把 {symbol} 卖出 {sell_shares} 股，回收 ${proceeds}。"
            tourist.market_preference = preferred_symbol or symbol
            tourist.market_preference_note = preference_note
            realized_delta = proceeds - realized_cost
            tourist.mood = self._bounded(tourist.mood + (2 if realized_delta >= 0 else -1))
            tourist.current_activity = f"刚把 {symbol} 卖出一部分，准备看看接下来还值不值得继续跟。"
            tourist.brief_note = f"刚把 {symbol} 卖出 {sell_shares} 股，回收 ${proceeds}，这趟投资开始更像一次短线试水。"
            self._apply_quote_move(symbol, max(-2.0, min(-0.35, -proceeds / 520)), f"受 {tourist.name} 的场外减仓影响")
            quote.volume = max(quote.volume or 0, (quote.volume or 0) + sell_shares)
            quote.turnover_pct = round((quote.volume / max(1, quote.shares_outstanding or BASE_SHARES_OUTSTANDING.get(quote.symbol, 100000))) * 100, 2)
            self._refresh_market_microstructure()
            self._update_index_history()
            self._update_daily_index_history()
            self._append_finance_record(
                actor_id=tourist.id,
                actor_name=tourist.name,
                category="market",
                action="exit",
                summary=f"{tourist.name} 通过外部券商卖出 {quote.name} {sell_shares} 股，回收 ${proceeds}，实现盈亏 ${realized_delta}。",
                amount=proceeds,
                asset_name=quote.name,
                counterparty="外部券商",
            )
            if self.random.random() < 0.35:
                post = FeedPost(
                    id=f"feed-{uuid4().hex[:8]}",
                    author_type="tourist",
                    author_id=tourist.id,
                    author_name=tourist.name,
                    day=self.state.day,
                    time_slot=self.state.time_slot,
                    category="market",
                    mood="cool" if realized_delta >= 0 else "tense",
                    content=self._clean_feed_text(
                        f"我先把 {symbol} 收回来一点，落袋为安总比把情绪全压在一条线上强。"
                        if realized_delta >= 0
                        else f"{symbol} 这波我先撤一点，不然心态会先被它拖坏。"
                    ),
                    topic_tags=[symbol, "游客减仓", "短线试水"],
                    desire_tags=["先收手", "控制风险"],
                    likes=4 + self.random.randint(0, 4),
                    views=28 + self.random.randint(0, 18),
                    summary="有游客开始把这里的市场当成可进可出的短线试水盘。",
                    impacts=["影响市场", "影响游客讨论"],
                )
                post.credibility = self._feed_credibility_for_post(post)
                post.heat = self._compute_feed_heat(post)
                self._append_feed_post(post, remember=True, apply_impacts=True)
            self._log(
                "tourist_market_exit",
                tourist={"id": tourist.id, "name": tourist.name, "tier": tourist.visitor_tier},
                quote={"symbol": quote.symbol, "name": quote.name, "shares": sell_shares, "proceeds": proceeds, "realized_delta": realized_delta},
            )

    def _tourist_preferred_market_symbol(self, tourist: TouristAgent) -> tuple[str, str]:
        scores = {"GEO": 0.0, "AGR": 0.0, "SIG": 0.0}
        reasons: dict[str, list[str]] = {symbol: [] for symbol in scores}
        topic = tourist.favorite_topic or ""
        if any(keyword in topic for keyword in ["GeoAI", "空间", "故事", "懂这里"]):
            scores["GEO"] += 1.1
            reasons["GEO"].append("你更关注 GeoAI 和小镇故事")
        if any(keyword in topic for keyword in ["集市", "价格", "带回去", "消费", "小吃"]):
            scores["AGR"] += 1.0
            reasons["AGR"].append("你更在意消费、集市和价格")
        if any(keyword in topic for keyword in ["天气", "住宿", "信号", "风向"]):
            scores["SIG"] += 0.9
            reasons["SIG"].append("你更留意住宿、风向和信号")
        if tourist.property_interest:
            scores["AGR"] += 0.35
            reasons["AGR"].append("你本来就在看房和资产")
        if tourist.visitor_tier == "vip":
            scores["SIG"] += 0.25
            reasons["SIG"].append("高消费游客更容易追逐风向")
        if tourist.visitor_tier == "buyer":
            scores["AGR"] += 0.3
            scores["GEO"] += 0.2
            reasons["AGR"].append("看房游客偏向资产和消费线")
            reasons["GEO"].append("看房游客也会顺带注意 GeoAI 主线")
        rotation_leader = self.state.market.rotation_leader or "GEO"
        scores[rotation_leader] += 0.55
        reasons[rotation_leader].append("当前市场主线正在轮到这只票")
        if self.state.market.regime == "bull":
            scores["GEO"] += 0.18
            scores["AGR"] += 0.12
            reasons["GEO"].append("牛市里更愿意追增长")
        elif self.state.market.regime == "risk":
            scores["SIG"] += 0.22
            reasons["SIG"].append("风险市里更偏保守信号资产")
        sentiment = self.state.market.sentiment or 0
        if sentiment >= 18:
            scores["GEO"] += 0.2
            scores["AGR"] += 0.14
            reasons["GEO"].append("市场情绪偏热，增长题材更受欢迎")
        elif sentiment <= -12:
            scores["SIG"] += 0.18
            reasons["SIG"].append("市场偏冷，防守型标的更稳")
        for post in (self.state.feed_timeline or [])[:24]:
            if post.category not in {"market", "tourism", "property"} or (post.heat or 0) < 10:
                continue
            tags = " ".join(post.topic_tags or []) + " " + (post.content or "")
            for symbol in scores:
                if symbol in tags:
                    delta = min(0.45, (post.heat or 0) / 120)
                    if post.mood == "tense":
                        delta *= -0.5
                        reasons[symbol].append(f"微博上有人在紧张讨论 {symbol}")
                    elif post.mood in {"warm", "spark"}:
                        reasons[symbol].append(f"微博上对 {symbol} 的情绪偏热")
                    scores[symbol] += delta
        symbol, _ = max(scores.items(), key=lambda item: item[1])
        note = "；".join(reasons[symbol][:3]) if reasons[symbol] else "更多是顺着当前市场和小镇舆论试水。"
        return symbol, note

    def _trigger_tourist_investment(self) -> None:
        listed_assets = [
            asset
            for asset in self.state.properties
            if asset.status == "listed"
            and asset.owner_type in {"market", "government"}
            and asset.property_type in {"rental_house", "shop", "greenhouse"}
        ]
        if not listed_assets:
            return
        for tourist in self.state.tourists:
            if tourist.visitor_tier not in {"buyer", "vip"}:
                continue
            if tourist.cash < 60:
                continue
            if tourist.current_location not in {"market", "meeting", "data_wall"}:
                continue
            trigger_bias = 0.06
            if tourist.property_interest:
                trigger_bias += 0.04
            if tourist.visitor_tier == "vip":
                trigger_bias += 0.03
            if self.random.random() > trigger_bias:
                continue
            target = self.random.choice(listed_assets)
            deposit = min(tourist.cash, max(24, min(180, int(round(target.purchase_price * 0.08)))))
            if deposit <= 0:
                continue
            tourist.cash = max(0, tourist.cash - deposit)
            tourist.property_interest = True
            tourist.current_activity = f"刚给 {target.name} 放了意向金，想再多看两眼。"
            tourist.brief_note = f"对 {target.name} 动了心，今天先拿了 ${deposit} 试水。"
            self.state.tourism.buyer_leads_total += 1
            if target.owner_type == "government":
                self.state.government.reserve_balance += deposit
                self.state.government.revenues["government_asset"] = self.state.government.revenues.get("government_asset", 0) + deposit
            self._append_finance_record(
                actor_id=tourist.id,
                actor_name=tourist.name,
                category="property",
                action="invest",
                summary=f"{tourist.name} 给 {target.name} 放了 ${deposit} 意向金，想继续观察后续价格和氛围。",
                amount=deposit,
                asset_name=target.name,
                counterparty="财政资产" if target.owner_type == "government" else "地产市场",
            )
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{tourist.name} 看中了 {target.name}",
                    summary=f"{tourist.name} 先给 {target.name} 放了 ${deposit} 的意向金，准备继续看看这里到底值不值得长留。",
                    slot=self.state.time_slot,
                    category="market",
                ),
            )
            self.state.events = self.state.events[:8]
            self._log(
                "tourist_property_invest",
                tourist={"id": tourist.id, "name": tourist.name, "tier": tourist.visitor_tier},
                property={"id": target.id, "name": target.name},
                deposit=deposit,
            )
            post = FeedPost(
                id=f"feed-{uuid4().hex[:8]}",
                author_type="tourist",
                author_id=tourist.id,
                author_name=tourist.name,
                day=self.state.day,
                time_slot=self.state.time_slot,
                category="property",
                mood="spark",
                content=self._clean_feed_text(f"{target.name} 我真有点心动。今天先放了 ${deposit} 当意向金，想看看这里到底值不值得长留。"),
                topic_tags=["看房", target.name, "意向金"],
                desire_tags=["想留更久", "先试水"],
                likes=5 + self.random.randint(0, 4),
                views=42 + self.random.randint(0, 24),
                summary="游客公开表达了对小镇房产的兴趣。",
                impacts=["提升购房线索", "带动地产讨论"],
            )
            post.credibility = self._feed_credibility_for_post(post)
            post.heat = self._compute_feed_heat(post)
            self._append_feed_post(post, remember=True, apply_impacts=True)

    def _refresh_tourist_turnover(self) -> None:
        remaining: list[TouristAgent] = []
        for tourist in self.state.tourists:
            should_leave = tourist.stay_until_day < self.state.day or tourist.cash <= 3
            if should_leave:
                self.state.tourism.total_departures += 1
                self.state.tourism.daily_departures += 1
                self.state.tourism.last_note = f"{tourist.name} 结束停留离开了，手里还剩 ${tourist.cash}。"
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=f"{tourist.name} 离开小镇",
                        summary=f"{tourist.name} 结束了这次短住，带着“{tourist.favorite_topic or '这里挺有意思'}”的印象离开了。",
                        slot=self.state.time_slot,
                        category="general",
                    ),
                )
                self.state.events = self.state.events[:8]
                continue
            remaining.append(tourist)
        self.state.tourists = remaining

    def _maybe_spawn_tourist(self) -> None:
        tourism = self.state.tourism
        if len(self.state.tourists) >= getattr(tourism, "max_visitor_cap", 10):
            return
        weather_bonus = {"sunny": 0.09, "breezy": 0.06, "cloudy": 0.02, "drizzle": -0.01}[self.state.weather]
        reputation_bonus = max(0.0, (self.state.lab.reputation - 18) / 260)
        market_bonus = max(0.0, self.state.market.sentiment / 320)
        season_bonus = {"off": -0.06, "normal": 0.0, "peak": 0.08, "festival": 0.14}.get(tourism.season_mode, 0.0)
        public_support_bonus = max(0.0, self.state.government.tourism_support_level / 500)
        chance = min(0.58, 0.07 + weather_bonus + reputation_bonus + market_bonus + season_bonus + public_support_bonus)
        if not self.state.tourists:
            chance = max(chance, 0.24)
        if self.random.random() > chance:
            return
        template = self.random.choice(TOURIST_ARCHETYPES)
        arrival_index = tourism.total_arrivals + 1
        base_name = TOURIST_NAME_POOL[(arrival_index - 1) % len(TOURIST_NAME_POOL)]
        name = base_name if not any(item.name == base_name for item in self.state.tourists) else f"{base_name}{arrival_index}"
        has_property_inventory = any(asset.status == "listed" for asset in self.state.properties if asset.owner_type == "market")
        tier_roll = self.random.random()
        visitor_tier = "regular"
        if has_property_inventory and tier_roll < 0.1:
            visitor_tier = "buyer"
        elif tier_roll < 0.22:
            visitor_tier = "vip"
        elif tier_roll < 0.4:
            visitor_tier = "repeat"
        tier_cash_bonus = {"regular": (26, 86), "repeat": (42, 112), "vip": (74, 168), "buyer": (96, 220)}[visitor_tier]
        cash = self.random.randint(*tier_cash_bonus)
        budget = min(cash - 6, int(template["budget"]) + self.random.randint(0, 8))
        spending_desire = max(30, min(95, int(template["spending_desire"]) + self.random.randint(-10, 12)))
        if visitor_tier == "vip":
            budget += 12
            spending_desire += 10
        elif visitor_tier == "repeat":
            budget += 5
            spending_desire += 4
        elif visitor_tier == "buyer":
            budget += 18
            spending_desire += 6
        initial_topic = self.random.choice(list(template["topic_pool"]))
        tourist = TouristAgent(
            id=f"tourist-{uuid4().hex[:8]}",
            name=name,
            archetype=str(template["archetype"]),
            visitor_tier=visitor_tier,
            is_returning=visitor_tier == "repeat",
            property_interest=visitor_tier == "buyer",
            message_influence=3 if visitor_tier == "vip" else 2 if visitor_tier in {"repeat", "buyer"} else 1,
            favorite_topic=initial_topic,
            position=tourism.inn_position.model_copy(),
            current_location=tourism.inn_location,
            cash=cash,
            budget=max(10, budget),
            mood=58 + self.random.randint(-8, 10),
            spending_desire=spending_desire,
            stay_until_day=self.state.day + self.random.randint(1, 3),
            current_activity=f"刚在{tourism.inn_name}放下行李，准备先看看集市和湖边。",
            current_bubble="这地方比想象中舒服。",
            brief_note=self._tourist_brief_note(visitor_tier, initial_topic),
            short_term_memory=[
                MemoryEntry(
                    text=f"刚住进{tourism.inn_name}，第一反应是这里比想象中更舒服。",
                    day=self.state.day,
                    time_slot=self.state.time_slot,
                    importance=2,
                )
            ],
        )
        self.state.tourists.append(tourist)
        tourism.total_arrivals += 1
        tourism.daily_arrivals += 1
        if tourist.is_returning:
            tourism.repeat_customers_total += 1
        if tourist.visitor_tier == "vip":
            tourism.vip_customers_total += 1
        if tourist.property_interest:
            tourism.buyer_leads_total += 1
        tourism.last_note = f"{tourist.name} 刚到 {tourism.inn_name}，准备逛逛 {tourism.market_name}。"
        self._route_tourism_income(tourist, amount=min(12, max(6, tourist.budget // 2)), spend_type="stay", note="入住旅馆")
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"{tourist.name} 搬进了 {tourism.inn_name}",
                summary=f"{tourist.name} 作为 {tourist.archetype} 来到小镇短住，身份偏向{self._tourist_tier_label(tourist.visitor_tier)}，可能会去 {tourism.market_name} 消费、和人聊天，并给本地经济带来一点热度。",
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._rebalance_tourist_activity()

    def _move_tourists(self) -> None:
        for tourist in self._active_tourists():
            if tourist.linger_ticks > 0 and tourist.target_position is not None and tourist.position == tourist.target_position:
                tourist.linger_ticks = max(0, tourist.linger_ticks - 1)
                tourist.current_location = self._room_for(tourist.position.x, tourist.position.y)
                tourist.current_activity = f"正在 {ROOM_LABELS.get(tourist.current_location, tourist.current_location)} 附近慢慢停留。"
                continue
            if tourist.target_position is None or tourist.position == tourist.target_position:
                destination = self._tourist_destination(tourist)
                tourist.target_position = destination.model_copy()
                tourist.target_location = self._room_for(destination.x, destination.y)
                tourist.linger_ticks = self.random.randint(1, 3)
            else:
                destination = tourist.target_position.model_copy()
            previous = tourist.position.model_copy()
            tourist.position = self._step_toward_point(tourist.position, destination)
            tourist.current_location = self._room_for(tourist.position.x, tourist.position.y)
            if tourist.position == destination:
                if not tourist.last_locations or tourist.last_locations[-1] != tourist.current_location:
                    tourist.last_locations.append(tourist.current_location)
                    tourist.last_locations = tourist.last_locations[-4:]
                if self.random.random() < 0.18:
                    self._refresh_tourist_topic(tourist)
                if destination == self.state.tourism.market_position:
                    tourist.current_activity = f"正在 {self.state.tourism.market_name} 东看西看，顺手打听这里的价钱和故事。"
                    tourist.current_bubble = self.random.choice(["这边摊子还挺密。", "这里买东西好像不贵。", "有人愿意给我讲讲这里吗？"])
                elif destination == self.state.tourism.inn_position:
                    tourist.current_activity = f"正在 {self.state.tourism.inn_name} 歇脚，准备下一轮出门。"
                    tourist.current_bubble = self.random.choice(["先回旅馆缓一缓。", "我晚点再出去。"])
                else:
                    tourist.current_activity = "正在湖边和广场之间慢慢闲逛。"
                    tourist.current_bubble = self.random.choice(["湖边真适合发呆。", "这里比我想的热闹。"])
            elif tourist.position != previous:
                tourist.current_activity = "正在往下一个想逛的地方慢慢走。"

    def _tourist_destination(self, tourist: TouristAgent) -> Point:
        tourism = self.state.tourism
        if self.state.time_slot == "night":
            return tourism.inn_position.model_copy()
        if tourist.cash <= 8:
            return tourism.inn_position.model_copy()
        candidate_keys = ["market_chat", "market_watch", "lakeside_pause", "workshop_huddle", "foyer_gossip", "noon_social"]
        candidates = [point for key in candidate_keys for point in self._activity_anchor_points(key)]
        room_loads: dict[str, int] = {}
        for other in self._active_tourists():
            room = other.target_location or other.current_location
            room_loads[room] = room_loads.get(room, 0) + 1
        recent_rooms = set((tourist.last_locations or [])[-2:])

        def score(point: Point) -> float:
            room = self._room_for(point.x, point.y)
            if room == tourist.current_location:
                return -999.0
            score = 1.0
            if room in recent_rooms:
                score -= 1.15
            score -= room_loads.get(room, 0) * 0.9
            if tourist.property_interest and room in {"meeting", "data_wall"}:
                score += 1.6
            if tourist.visitor_tier == "vip" and room in {"lounge", "data_wall"}:
                score += 1.25
            if room == tourism.market_location:
                score += 0.75 if tourist.cash >= 14 else 0.25
            if room == tourism.inn_location:
                score -= 0.45
            return score + self.random.uniform(-0.18, 0.18)

        ranked = sorted(candidates, key=score, reverse=True)
        if tourist.current_location == tourism.inn_location:
            return ranked[0].model_copy()
        if tourist.property_interest:
            buyer_targets = self._activity_anchor_points("buyer_tour")
            ranked_buyers = sorted(buyer_targets, key=score, reverse=True)
            return ranked_buyers[0].model_copy()
        if tourist.visitor_tier == "vip":
            vip_targets = self._activity_anchor_points("vip_stroll") + [tourism.market_position.model_copy()]
            ranked_vip = sorted(vip_targets, key=score, reverse=True)
            return ranked_vip[0].model_copy()
        return ranked[0].model_copy()

    def _rebalance_tourists_if_clustered(self) -> None:
        tourists = self._active_tourists()
        if len(tourists) < 4:
            return
        counts: dict[str, int] = {}
        for tourist in tourists:
            counts[tourist.current_location] = counts.get(tourist.current_location, 0) + 1
        crowded_room, crowded_count = max(counts.items(), key=lambda item: item[1])
        if crowded_count < len(tourists) - 1:
            return
        scatter_points = [
            self._pick_activity_anchor("market_chat"),
            self._pick_activity_anchor("buyer_tour"),
            self._pick_activity_anchor("workshop_huddle"),
            self._pick_activity_anchor("foyer_gossip"),
            self._pick_activity_anchor("lakeside_pause"),
        ]
        for tourist, point in zip(tourists, scatter_points):
            destination = self._nearest_walkable(point, self._room(self._room_for(point.x, point.y)))
            tourist.position = destination
            tourist.current_location = self._room_for(destination.x, destination.y)
            tourist.target_position = destination.model_copy()
            tourist.target_location = tourist.current_location
            tourist.linger_ticks = self.random.randint(1, 2)
            tourist.last_locations = [crowded_room, tourist.current_location]
            tourist.current_activity = f"刚从拥挤的{ROOM_LABELS.get(crowded_room, crowded_room)}散开，准备在{ROOM_LABELS.get(tourist.current_location, tourist.current_location)}看看。"

    def _step_toward_point(self, point: Point, target: Point) -> Point:
        dx = 0 if target.x == point.x else (1 if target.x > point.x else -1)
        dy = 0 if target.y == point.y else (1 if target.y > point.y else -1)
        options: list[tuple[int, int]] = []
        if abs(target.x - point.x) >= abs(target.y - point.y):
            options.extend([(dx, 0), (0, dy), (dx, dy)])
        else:
            options.extend([(0, dy), (dx, 0), (dx, dy)])
        options.extend([(0, 0)])
        for step_x, step_y in options:
            moved = self._move_with_collision(point, step_x, step_y)
            if moved != point or (step_x == 0 and step_y == 0):
                return moved
        return point

    def _trigger_tourist_spending(self) -> None:
        active_tourists = self._active_tourists()
        if not active_tourists:
            return
        for tourist in active_tourists:
            if tourist.cash <= 5 or self.random.random() > 0.34:
                continue
            multiplier = {"regular": 1.0, "repeat": 1.15, "vip": 1.42, "buyer": 1.18}.get(tourist.visitor_tier, 1.0)
            if tourist.current_location == self.state.tourism.market_location:
                amount = int(round(max(4, min(22, tourist.spending_desire // 6 + self.random.randint(0, 5))) * multiplier))
                amount = min(tourist.cash, amount)
                self._route_tourism_income(tourist, amount=amount, spend_type="market", note="在集市消费")
                tourist.current_bubble = self.random.choice(["这笔买得值。", "这里真容易花钱。", "我想把这个也带走。"])
                tourist.mood = self._bounded(tourist.mood + 2)
            elif tourist.current_location == self.state.tourism.inn_location and self.random.random() < 0.24:
                amount = int(round(max(3, min(14, tourist.budget // 3)) * multiplier))
                amount = min(tourist.cash, amount)
                self._route_tourism_income(tourist, amount=amount, spend_type="stay", note="在旅馆加购服务")
                tourist.current_bubble = "旅馆这边倒是挺省心。"
                tourist.mood = self._bounded(tourist.mood + 1)
            if tourist.property_interest and tourist.current_location == self.state.tourism.market_location and self.random.random() < 0.18:
                self._append_finance_record(
                    actor_id=tourist.id,
                    actor_name=tourist.name,
                    category="tourism",
                    action="visit",
                    summary=f"{tourist.name} 顺手打听了几处挂牌资产，已经算一个潜在购房线索。",
                    amount=0,
                    asset_name="看房咨询",
                    counterparty=self.state.tourism.market_name,
                )
                self.state.tourism.last_note = f"{tourist.name} 在 {self.state.tourism.market_name} 问了看房和买卖行情。"

    def _route_tourism_income(self, tourist: TouristAgent, amount: int, spend_type: str, note: str) -> None:
        if amount <= 0 or tourist.cash <= 0:
            return
        actual_amount = min(amount, tourist.cash)
        tourist.cash -= actual_amount
        tourism = self.state.tourism
        if spend_type == "stay":
            candidates = [asset for asset in self.state.properties if asset.status == "owned" and asset.property_type == "rental_house" and asset.owner_type != "market"]
            facility_name = tourism.inn_name
        else:
            candidates = [
                asset
                for asset in self.state.properties
                if asset.status == "owned" and asset.property_type in {"shop", "farm_plot", "greenhouse"} and asset.owner_type != "market"
            ]
            facility_name = tourism.market_name
        owner_name = facility_name
        owner_type = "market"
        owner_id = facility_name
        if candidates:
            asset = self.random.choice(candidates)
            facility_name = asset.name
            owner_type = asset.owner_type
            owner_id = asset.owner_id
            owner_name = self._property_owner_name(asset)
            if owner_type == "player":
                self.state.player.cash += actual_amount
                self.state.player.last_trade_summary = f"{tourist.name} 刚在 {asset.name} 花了 ${actual_amount}。"
            elif owner_type == "agent":
                owner = self._find_agent(owner_id)
                owner.cash += actual_amount
                owner.last_trade_summary = f"{tourist.name} 刚在 {asset.name} 留下 ${actual_amount} 的收入。"
                owner.current_bubble = "今天游客倒是挺愿意花钱。"
            elif owner_type == "government":
                self.state.government.reserve_balance += actual_amount
                self.state.government.revenues["government_asset"] = self.state.government.revenues.get("government_asset", 0) + actual_amount
                self.state.government.last_distribution_note = f"政府持有资产 {asset.name} 刚收到游客收入 ${actual_amount}。"
        else:
            owner_type = "public_tourism"
            owner_id = "tourism_public"
            owner_name = "小镇文旅运营"
            self.state.government.reserve_balance += actual_amount
            self.state.government.revenues["tourism_public"] = self.state.government.revenues.get("tourism_public", 0) + actual_amount
        tourism.daily_revenue += actual_amount
        tourism.total_revenue += actual_amount
        if owner_type in {"player", "agent"}:
            tourism.daily_private_income += actual_amount
            tourism.total_private_income += actual_amount
        elif owner_type == "government":
            tourism.daily_government_income += actual_amount
            tourism.total_government_income += actual_amount
        elif owner_type == "public_tourism":
            tourism.daily_public_operator_income += actual_amount
            tourism.total_public_operator_income += actual_amount
        tourism.last_note = f"{tourist.name} 刚在 {facility_name} 花了 ${actual_amount}。"
        self._remember_tourist(tourist, f"你刚在 {facility_name} 花了 ${actual_amount}，对这里的消费体验多留意了一层。", 1)
        tax = self._collect_tax(
            payer_type="tourist",
            payer_id=tourist.id,
            payer_name=tourist.name,
            revenue_key="consumption",
            label=f"{note}",
            base_amount=actual_amount,
            rate_pct=self.state.government.consumption_tax_rate_pct,
        )
        self._append_finance_record(
            actor_id=tourist.id,
            actor_name=tourist.name,
            category="tourism",
            action="spend",
            summary=f"{tourist.name} {note}，在 {facility_name} 留下了 ${actual_amount}。",
            amount=-actual_amount,
            asset_name=facility_name,
            counterparty=owner_name,
        )
        if owner_type in {"player", "agent", "government", "public_tourism"}:
            self._append_finance_record(
                actor_id=owner_id,
                actor_name=owner_name,
                category="government" if owner_type in {"government", "public_tourism"} else "tourism",
                action="receive",
                summary=f"{owner_name} 因游客消费从 {facility_name} 收到 ${actual_amount} 的收入。",
                amount=actual_amount,
                asset_name=facility_name,
                counterparty=tourist.name,
            )
        if tax > 0:
            self.state.tourism.last_note = f"{tourist.name} 在 {facility_name} 消费 ${actual_amount}，其中缴税 ${tax}。"

    def _trigger_tourist_conversations(self) -> None:
        active_tourists = self._active_tourists()
        if not active_tourists or self.random.random() > 0.46:
            return
        tourist = self.random.choice(active_tourists)
        nearby_agents = [
            agent
            for agent in self.state.agents
            if not agent.is_resting and agent.current_location == tourist.current_location and abs(agent.position.x - tourist.position.x) + abs(agent.position.y - tourist.position.y) <= 4
        ]
        if not nearby_agents:
            return
        agent = self.random.choice(nearby_agents)
        tourist_line, agent_line = self._tourist_ambient_lines(tourist, agent)
        tourist.current_bubble = tourist_line
        agent.current_bubble = agent_line
        tourist.current_activity = f"刚和 {agent.name} 聊起了“{tourist.favorite_topic or '这里的生活'}”。"
        agent.current_activity = f"刚和游客 {tourist.name} 接了一轮短对话。"
        self._remember_tourist(tourist, f"你刚和 {agent.name} 聊了“{tourist.favorite_topic or '这里的生活'}”，对这座小镇的印象更具体了。", 2)
        self._remember(agent, f"刚和游客 {tourist.name} 聊了“{tourist.favorite_topic or '这里的生活'}”。", 1)
        agent.state.mood = self._bounded(agent.state.mood + 1)
        self.state.lab.team_atmosphere = self._bounded(self.state.lab.team_atmosphere + 1)
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="ambient_dialogue",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=[tourist.id, agent.id],
                participant_names=[tourist.name, agent.name],
                topic=tourist.favorite_topic or "旅途见闻",
                summary=self._natural_tourist_dialogue_summary(
                    tourist.name,
                    agent.name,
                    ROOM_LABELS.get(tourist.current_location, tourist.current_location),
                    tourist.favorite_topic or "旅途见闻",
                ),
                key_point=self._natural_tourist_agent_key_point(tourist.name, agent.name, tourist.favorite_topic or "这里值得看什么"),
                transcript=[f"{tourist.name}：{tourist_line}", f"{agent.name}：{agent_line}"],
                desire_labels={tourist.name: "想把旅途过得有意思一点", agent.name: DESIRE_LABELS.get(dominant_desire_for_agent(self.state, agent)[0], "想先观察局势")},
                mood="warm",
            )
        )
        self._append_finance_record(
            actor_id=tourist.id,
            actor_name=tourist.name,
            category="tourism",
            action="chat",
            summary=f"{tourist.name} 刚和 {agent.name} 聊了一轮，后续更可能继续消费或留宿。",
            amount=0,
            asset_name=self.state.tourism.market_name,
            counterparty=agent.name,
        )
        self._log(
            "tourist_ambient_dialogue",
            tourist={"id": tourist.id, "name": tourist.name},
            agent={"id": agent.id, "name": agent.name},
            topic=tourist.favorite_topic,
        )

    def _trigger_tourist_signals(self) -> None:
        tourism = self.state.tourism
        active_tourists = self._active_tourists()
        if not active_tourists or tourism.daily_messages_count >= 2:
            return
        chance = 0.09 + (0.06 if tourism.season_mode in {"peak", "festival"} else 0.0) + min(0.08, len(active_tourists) * 0.015)
        if self.random.random() > chance:
            return
        tourist = self.random.choice(active_tourists)
        signal = self.random.choice(TOURIST_SIGNAL_BANK)
        event = LabEvent(
            id=f"tourist-signal-{uuid4().hex[:8]}",
            category=signal["category"],
            title=f"游客消息：{signal['title']}",
            summary=f"{tourist.name} 带来的外部说法：{signal['summary']}",
            source=tourist.name,
            time_slot=self.state.time_slot,
            impacts={"collective_reasoning": 1, "research_progress": 1 if signal["category"] in {"geoai", "tech"} else 0},
            participants=[tourist.id],
            tone_hint=int(signal["tone"]) * tourist.message_influence,
            market_target=str(signal["target"]),
            market_strength=min(5, int(signal["strength"]) + tourist.message_influence - 1),
        )
        tourism.daily_messages_count += 1
        tourism.latest_signal = event.title
        tourism.last_note = f"{tourist.name} 带来一条外部消息：{signal['title']}。"
        tourist.current_bubble = self.random.choice([
            "我刚听到一条外面的风声。",
            "这消息不一定准，但外面已经在传了。",
            "我在旅馆里听到一个值得提一下的说法。",
        ])
        tourist.brief_note = f"刚把一条外部消息带进小镇：{signal['title']}。"
        self._remember_tourist(tourist, f"你刚把一条外部消息“{signal['title']}”带进小镇，觉得自己像个临时情报源。", 2)
        self._ingest_event(event, player_injected=False)

    def _tourist_ambient_lines(self, tourist: TouristAgent, agent: Agent) -> tuple[str, str]:
        tourist_openers = [
            f"这里最值得逛的是哪一块？我主要想看看{tourist.favorite_topic or '好玩的地方'}。",
            f"我刚从{self.state.tourism.inn_name}那边过来，这里比我想的热闹。",
            "你们这边平时也会这么多人吗？",
        ]
        agent_replies = {
            "rational": f"如果你想看得更值一点，可以先去{ROOM_LABELS.get(agent.current_location, agent.current_location)}附近转一圈。",
            "creative": "你可以别按路线走，绕一下湖边和集市中间，会更有意思。",
            "engineering": "先去集市，再回旅馆，会比较顺路。",
            "empathetic": "你别赶，慢慢逛就行。累了就回旅馆坐会儿。",
            "opportunist": "如果你想听新鲜事，先去集市，消息都在那里。",
        }
        return self.random.choice(tourist_openers), agent_replies.get(agent.persona, "先随便逛逛，哪里有感觉就停一下。")

    def _tourist_reply_line(self, tourist: TouristAgent, player_text: str) -> str:
        if any(token in player_text for token in ["住", "旅馆", "休息"]):
            return f"{self.state.tourism.inn_name} 倒挺安静的，我可能今晚就住那边。"
        if any(token in player_text for token in ["买", "集市", "逛", "吃"]):
            return f"{self.state.tourism.market_name} 挺有意思，我刚刚已经在那里花掉一笔了。"
        if any(token in player_text for token in ["GeoAI", "实验", "研究", "空间智能"]):
            return "原来这里不只是田园，我还真想听听你们在研究什么。"
        return self.random.choice(
            [
                "我主要是来住两天、逛逛集市，再听听这里的人都在聊什么。",
                "这边节奏挺舒服的，我本来只想路过，结果想多待一会儿。",
                "我现在最想知道，哪里最值得逛，哪里最值得花钱。",
            ]
        )

    def _tourist_tier_label(self, visitor_tier: str) -> str:
        return {
            "regular": "普通游客",
            "repeat": "回头客",
            "vip": "高消费客户",
            "buyer": "潜在购房者",
        }.get(visitor_tier, visitor_tier)

    def _tourist_brief_note(self, visitor_tier: str, topic: str) -> str:
        tier_note = {
            "regular": "更容易被轻松氛围和集市吸引，会带来稳定的小额消费。",
            "repeat": "这是回头客，熟悉小镇节奏，更容易再次消费和传播消息。",
            "vip": "这是高消费客户，出手更大方，也更容易影响周边人的判断。",
            "buyer": "这是潜在购房者，会顺手打听旅馆、集市和挂牌房产。",
        }.get(visitor_tier, "会在停留期间带来额外消费。")
        return f"{tier_note} 这趟尤其在意“{topic}”。"

    def _refresh_tourism_cycle(self) -> None:
        cycle = self.state.day % 12
        tourism = self.state.tourism
        if cycle in {0, 6}:
            tourism.season_mode = "festival"
            tourism.event_day_title = TOURISM_EVENT_TITLES[(self.state.day // 3) % len(TOURISM_EVENT_TITLES)]
        elif cycle in {4, 5, 7}:
            tourism.season_mode = "peak"
            tourism.event_day_title = ""
        elif cycle in {1, 2}:
            tourism.season_mode = "off"
            tourism.event_day_title = ""
        else:
            tourism.season_mode = "normal"
            tourism.event_day_title = ""
        tourism.last_note = (
            f"今天是{self._tourism_season_label(tourism.season_mode)}，主题是“{tourism.event_day_title}”。"
            if tourism.event_day_title
            else f"今天游客流量处在{self._tourism_season_label(tourism.season_mode)}。"
        )

    def _tourism_season_label(self, season_mode: str) -> str:
        return {
            "off": "淡季",
            "normal": "平季",
            "peak": "旺季",
            "festival": "活动日",
        }.get(season_mode, season_mode)

    def _trigger_work_activity(self) -> None:
        if not self.state.market.is_open:
            return
        if self._player_should_work():
            self._run_player_work_shift(forced=self._player_total_funds() < self.state.company.low_cash_threshold)
        for agent in self.state.agents:
            if agent.is_resting:
                continue
            if self._agent_should_work(agent):
                self._run_agent_work_shift(agent, forced=self._agent_total_funds(agent) < self.state.company.low_cash_threshold)

    def _trigger_gray_market_activity(self) -> None:
        active_cases = sum(1 for case in self.state.gray_cases if case.status == "active")
        pressure = 0.08 + max(0, 2 - active_cases) * 0.04
        if self.state.market.regime == "risk":
            pressure += 0.08
        elif self.state.market.regime == "sideways":
            pressure += 0.03
        if self.state.lab.reputation <= 24:
            pressure += 0.05
        if self.random.random() > min(0.32, pressure):
            return
        candidates = [
            agent
            for agent in self.state.agents
            if not agent.is_resting and (agent.cash <= 120 or agent.money_urgency >= 50 or agent.materialism >= 56 or agent.credit_score <= 60)
        ]
        if len(candidates) < 2:
            return
        requester = max(
            candidates,
            key=lambda agent: agent.money_urgency + max(0, 60 - agent.cash) + agent.materialism + max(0, 68 - agent.credit_score),
        )
        donors = [
            agent
            for agent in candidates
            if agent.id != requester.id and agent.cash >= 10 and requester.current_location == agent.current_location
        ]
        if not donors:
            donors = [agent for agent in candidates if agent.id != requester.id and agent.cash >= 10]
        if not donors:
            return
        donor = max(donors, key=lambda agent: agent.cash + agent.generosity + max(0, agent.relations.get(requester.id, 0)))
        topic = self.random.choice(["灰市盘子", "账外回扣", "不想摆到台面的钱", "临时过手的私货", "灰色套利机会"])
        first_desire, _ = dominant_desire_for_agent(self.state, requester)
        second_desire, _ = dominant_desire_for_agent(self.state, donor)
        mood = self._thread_mood(
            requester,
            donor,
            topic,
            existing=self._social_thread_for(requester.id, donor.id),
            first_desire=first_desire,
            second_desire=second_desire,
        )
        gray_options = self._gray_trade_catalog(requester, donor, topic, mood, first_desire, second_desire)
        if not gray_options:
            return
        plan = self.random.choice(gray_options)
        result = self._execute_gray_trade_plan(requester, donor, topic, mood, plan)
        if result is None:
            return
        line_a = str(plan.get("line_a") or f"这笔别摆到台面上，{donor.name}，钱先过来。")
        line_b = str(plan.get("line_b") or "行，这笔就按灰市的规矩走。")
        requester.current_bubble = line_a
        donor.current_bubble = line_b
        requester.current_activity = f"刚和 {donor.name} 过完一笔{self._gray_case_label(str(plan.get('type') or 'under_table_exchange'))}。"
        donor.current_activity = f"刚和 {requester.name} 走完一笔不想公开的钱。"
        left_desire_label = DESIRE_LABELS.get(first_desire, first_desire)
        right_desire_label = DESIRE_LABELS.get(second_desire, second_desire)
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="gray_trade",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=[requester.id, donor.id],
                participant_names=[requester.name, donor.name],
                topic=topic,
                summary=self._natural_gray_trade_summary(requester.name, donor.name, topic),
                key_point=self._ambient_dialogue_key_point(
                    requester.name,
                    donor.name,
                    topic,
                    mood,
                    left_desire_label,
                    right_desire_label,
                    str(result.get("note") or ""),
                ),
                transcript=[f"{requester.name}：{line_a}", f"{donor.name}：{line_b}"],
                desire_labels={requester.name: left_desire_label, donor.name: right_desire_label},
                mood=str(plan.get("mood_override") or mood),
                financial_note=str(result.get("note") or ""),
                gray_trade=True,
                gray_trade_type=str(result.get("gray_trade_type") or plan.get("type") or "under_table_exchange"),
                gray_trade_severity=int(result.get("gray_trade_severity") or plan.get("severity") or 2),
            )
        )
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"灰市里又起了一笔{self._gray_case_label(str(plan.get('type') or 'under_table_exchange'))}",
                summary=f"{requester.name} 和 {donor.name} 在{ROOM_LABELS.get(requester.current_location, requester.current_location)}悄悄做了一笔不想公开的买卖。",
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._log(
            "gray_market_activity",
            requester={"id": requester.id, "name": requester.name},
            donor={"id": donor.id, "name": donor.name},
            gray_type=str(plan.get("type") or "under_table_exchange"),
            amount=int(plan.get("amount", 0) or 0),
            topic=topic,
        )

    def _player_should_work(self) -> bool:
        threshold = self.state.company.low_cash_threshold
        total_funds = self._player_total_funds()
        if total_funds < threshold:
            return True
        urge = max(0, threshold + 18 - total_funds)
        work_score = self.state.player.work_drive + urge + self.state.player.monthly_burden // 2
        return self.random.random() < min(0.32, 0.05 + work_score / 320)

    def _agent_should_work(self, agent: Agent) -> bool:
        threshold = self.state.company.low_cash_threshold
        total_funds = self._agent_total_funds(agent)
        if total_funds < threshold:
            return True
        if agent.state.energy <= 18:
            return False
        work_score = agent.work_drive + max(0, threshold + 18 - total_funds) + agent.money_urgency // 2 + agent.monthly_burden // 3
        return self.random.random() < min(0.36, 0.04 + work_score / 300)

    def _work_effort_from_drive(self, work_drive: int, cash: int, threshold: int) -> int:
        pressure = max(0, threshold + 24 - cash)
        return max(4, min(12, 4 + work_drive // 18 + pressure // 12))

    def _run_player_work_shift(self, forced: bool = False) -> None:
        threshold = self.state.company.low_cash_threshold
        effort = self._work_effort_from_drive(self.state.player.work_drive, self.state.player.cash, threshold)
        pay = self.state.company.base_pay_per_shift + effort * self.state.company.pay_per_energy + int(round(effort * self.state.company.pay_skill_multiplier * (1 + self.state.player.risk_appetite / 20)))
        self.state.player.cash += pay
        wage_tax = self._collect_tax(
            payer_type="player",
            payer_id=self.state.player.id,
            payer_name=self.state.player.name,
            revenue_key="wage",
            label="工资收入",
            base_amount=pay,
            rate_pct=self.state.government.wage_tax_rate_pct,
        )
        self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + (1 if forced else 0) - max(1, effort // 5))
        self.state.player.consumption_desire = self._bounded(self.state.player.consumption_desire + 4)
        self.state.player.daily_actions.append(f"work:{self.state.company.name}:${pay}")
        self.state.player.last_trade_summary = f"刚去{self.state.company.name}干了一轮，税后到手 ${max(0, pay - wage_tax)}。"
        self.state.company.total_wages_paid += pay
        self.state.company.total_work_sessions += 1
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"你去 {self.state.company.name} 上了一轮班",
                summary=f"你投入了约 {effort} 点精力，在 {self.state.company.location_label} 那边干完一轮活，赚到 ${pay}。",
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._append_finance_record(
            actor_id=self.state.player.id,
            actor_name=self.state.player.name,
            category="work",
            action="work",
            summary=f"你在 {self.state.company.name} 工作一轮，税前 ${pay}，税后 ${max(0, pay - wage_tax)}。",
            amount=max(0, pay - wage_tax),
            asset_name=self.state.company.name,
            counterparty="工资结算",
        )

    def _run_agent_work_shift(self, agent: Agent, forced: bool = False) -> None:
        threshold = self.state.company.low_cash_threshold
        effort = min(max(4, agent.state.energy // 6), self._work_effort_from_drive(agent.work_drive, agent.cash, threshold))
        if effort <= 0:
            return
        skill_mix = (agent.state.research_skill + agent.state.geo_reasoning_skill) / 20
        pay = self.state.company.base_pay_per_shift + effort * self.state.company.pay_per_energy + int(round(effort * self.state.company.pay_skill_multiplier * skill_mix * 10))
        agent.cash += pay
        wage_tax = self._collect_tax(
            payer_type="agent",
            payer_id=agent.id,
            payer_name=agent.name,
            revenue_key="wage",
            label="工资收入",
            base_amount=pay,
            rate_pct=self.state.government.wage_tax_rate_pct,
        )
        agent.state.energy = max(0, agent.state.energy - effort * 2)
        agent.state.stress = self._bounded(agent.state.stress + (3 if forced else 1))
        agent.state.mood = self._bounded(agent.state.mood - (1 if forced else 0))
        self._adjust_agent_satisfaction(agent, -max(1, effort // 5) + (1 if forced else 0))
        agent.consumption_desire = self._bounded(agent.consumption_desire + 5)
        agent.current_location = "compute"
        agent.position = Point(x=self.state.company.position.x, y=self.state.company.position.y)
        agent.current_activity = f"正在 {self.state.company.name} 打工换现金。"
        agent.current_bubble = "我先去公司把现金补一补。"
        agent.last_trade_summary = f"刚在{self.state.company.name}干了一轮，税后到手 ${max(0, pay - wage_tax)}。"
        agent.last_interaction = f"刚去 {self.state.company.name} 打工一轮，优先把现金补上。"
        self.state.company.total_wages_paid += pay
        self.state.company.total_work_sessions += 1
        self._remember(agent, f"你刚在 {self.state.company.name} 工作一轮，赚到 ${pay}。", 2)
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"{agent.name} 去 {self.state.company.name} 打工",
                summary=f"{agent.name} 投入了约 {effort} 点精力，换回 ${pay} 的现金，准备继续应付接下来的消费、借贷或交易。",
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._append_finance_record(
            actor_id=agent.id,
            actor_name=agent.name,
            category="work",
            action="work",
            summary=f"{agent.name} 在 {self.state.company.name} 工作一轮，税前 ${pay}，税后 ${max(0, pay - wage_tax)}。",
            amount=max(0, pay - wage_tax),
            asset_name=self.state.company.name,
            counterparty="工资结算",
        )

    def _settle_daily_living_costs(self) -> None:
        player_activity_load = min(5, len(self.state.player.daily_actions) // 4)
        self._apply_daily_living_cost(
            actor_type="player",
            actor_id=self.state.player.id,
            actor_name=self.state.player.name,
            base_cost=self.state.player.daily_cost_baseline + player_activity_load + max(0, self.state.player.monthly_burden // 10),
            current_cash=self.state.player.cash,
        )
        for agent in self.state.agents:
            behavior_cost = max(0, agent.monthly_burden // 10) + (2 if agent.current_activity and ("买" in agent.current_activity or "卖" in agent.current_activity or "打工" in agent.current_activity) else 0)
            self._apply_daily_living_cost(
                actor_type="agent",
                actor_id=agent.id,
                actor_name=agent.name,
                base_cost=agent.daily_cost_baseline + behavior_cost,
                current_cash=agent.cash,
                agent=agent,
            )

    def _update_inflation_state(self) -> None:
        property_count = sum(1 for asset in self.state.properties if asset.owner_type != "market" and asset.status == "owned")
        total_cash = self._team_cash_total() + self.state.player.cash
        total_daily_burden = self.state.player.daily_cost_baseline + sum(agent.daily_cost_baseline for agent in self.state.agents)
        service_relief = (self.state.government.public_service_level + self.state.government.housing_support_level) / 34
        regime_bias = {"bull": 2.8, "sideways": 1.2, "risk": -1.4}.get(self.state.market.regime or "bull", 1.0)
        sentiment_bias = (self.state.market.sentiment or 0) / 18
        wealth_bias = min(14.0, total_cash / 5200)
        property_bias = property_count * 0.8
        wage_bias = min(4.5, self.state.company.total_work_sessions / 60)
        day_bias = min(7.0, max(0.0, (self.state.day - 1) * 0.22))
        burden_bias = min(6.0, total_daily_burden / 110)
        reputation_bias = max(0.0, (self.state.lab.reputation - 45) / 18)
        weather_bias = {"sunny": 0.3, "breezy": 0.6, "cloudy": 0.8, "drizzle": 1.2}.get(self.state.weather, 0.4)
        target = max(96.0, min(172.0, 100.0 + regime_bias + sentiment_bias + wealth_bias + property_bias + wage_bias + day_bias + burden_bias + reputation_bias + weather_bias - service_relief))
        previous = self.state.market.inflation_index or 100.0
        next_value = max(96.0, min(170.0, previous + ((target - previous) * 0.32)))
        next_value = round(next_value, 2)
        if previous <= 0:
            daily_pct = 0.0
        else:
            daily_pct = round(((next_value - previous) / previous) * 100, 2)
        self.state.market.inflation_index = next_value
        self.state.market.daily_inflation_pct = daily_pct
        pressure = ((next_value - 100.0) * 1.35) + property_count + (total_daily_burden / 36) + max(0, total_cash - 6000) / 3000 - ((self.state.government.public_service_level + self.state.government.housing_support_level) / 18)
        if self.state.market.regime == "risk":
            pressure += 3
        self.state.market.living_cost_pressure = self._bounded(round(pressure))

    def _update_daily_cost_baselines(self) -> None:
        inflation_index = self.state.market.inflation_index or 100.0
        living_pressure = self.state.market.living_cost_pressure or 0
        service_relief = round((self.state.government.public_service_level + self.state.government.housing_support_level) / 32)
        inflation_lift = max(0, round((inflation_index - 100.0) / 16))
        pressure_lift = max(0, round(living_pressure / 24))
        wealth_lift = min(4, round(max(0, self._team_cash_total() + self.state.player.cash - 18000) / 32000))
        tourism_lift = 1 if (self.state.tourism and ((self.state.tourism.daily_arrivals or 0) >= 4 or len(self.state.tourists or []) >= 4)) else 0

        def step_toward(current: int, target: int, floor: int, cap: int) -> int:
            current = current or floor
            target = max(floor, min(cap, target))
            if current < target:
                current += min(2, target - current)
            elif current > target:
                current -= min(1, current - target)
            return max(floor, min(cap, current))

        player_target = (
            8
            + inflation_lift
            + pressure_lift
            + wealth_lift
            + tourism_lift
            + max(0, self.state.player.monthly_burden // 14)
            - service_relief
        )
        self.state.player.daily_cost_baseline = step_toward(
            self.state.player.daily_cost_baseline,
            player_target,
            8,
            36,
        )

        persona_base_cost = {
            "engineering": 6,
            "rational": 7,
            "creative": 8,
            "empathetic": 7,
            "opportunist": 9,
        }
        for agent in self.state.agents:
            asset_lift = 1 if self._agent_total_assets(agent) >= 12000 else 0
            housing_lift = max(0, len(agent.owned_property_ids or []) - 1)
            target = (
                persona_base_cost.get(agent.persona, 7)
                + inflation_lift
                + pressure_lift
                + wealth_lift
                + tourism_lift
                + asset_lift
                + housing_lift
                + max(0, agent.monthly_burden // 14)
                - service_relief
            )
            agent.daily_cost_baseline = step_toward(agent.daily_cost_baseline, target, 6, 34)

    def _apply_daily_living_cost(
        self,
        *,
        actor_type: str,
        actor_id: str,
        actor_name: str,
        base_cost: int,
        current_cash: int,
        agent: Agent | None = None,
    ) -> None:
        inflation_multiplier = max(1.0, (self.state.market.inflation_index or 100.0) / 100)
        pressure_surcharge = max(0, round((self.state.market.living_cost_pressure or 0) / 18))
        service_discount = max(0, round((self.state.government.public_service_level + self.state.government.housing_support_level) / 22))
        cost = max(4, min(48, round(base_cost * inflation_multiplier) + pressure_surcharge - service_discount))
        payment = min(current_cash, cost)
        consumption_tax = max(1, int(round(payment * self.state.government.consumption_tax_rate_pct / 100))) if payment > 0 else 0
        actual_tax = 0
        if actor_type == "player":
            self.state.player.cash = max(0, self.state.player.cash - payment)
            if consumption_tax:
                actual_tax = min(consumption_tax, self.state.player.cash)
                self.state.player.cash = max(0, self.state.player.cash - actual_tax)
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction - (2 if payment < cost else 1))
            self.state.player.last_trade_summary = f"昨天的日常开销结算了 ${payment}，当前物价指数 {self.state.market.inflation_index:.1f}。"
        elif agent is not None:
            agent.cash = max(0, agent.cash - payment)
            if consumption_tax:
                actual_tax = min(consumption_tax, agent.cash)
                agent.cash = max(0, agent.cash - actual_tax)
            self._adjust_agent_satisfaction(agent, -2 if payment < cost else -1)
            agent.last_trade_summary = f"昨天的日常开销结算了 ${payment}，物价有点在往上走。"
        if actual_tax:
            self.state.government.total_revenue += actual_tax
            self.state.government.reserve_balance += actual_tax
            self.state.government.revenues["consumption"] = self.state.government.revenues.get("consumption", 0) + actual_tax
            self._append_finance_record(
                actor_id=actor_id,
                actor_name=actor_name,
                category="tax",
                action="tax",
                summary=f"{actor_name} 因日常开销缴了 ${actual_tax} 消费税。",
                amount=-actual_tax,
                asset_name="日常开销税",
                counterparty=self.state.government.name,
            )
        post_cash = self.state.player.cash if actor_type == "player" else agent.cash if agent is not None else 0
        post_funds = post_cash + (self.state.player.deposit_balance if actor_type == "player" else agent.deposit_balance if agent is not None else 0)
        total_assets = self._player_total_assets() if actor_type == "player" else self._agent_total_assets(agent) if agent is not None else post_funds
        if post_funds <= self.state.government.welfare_low_cash_threshold:
            payout = self._disburse_welfare(
                recipient_type=actor_type,
                recipient_id=actor_id,
                recipient_name=actor_name,
                current_cash=post_cash,
                total_assets=total_assets,
                bankruptcy=post_funds <= 0,
                agent=agent,
            )
            if payout > 0:
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=f"{actor_name} 获得财政保障",
                        summary=f"{self.state.government.name} 向 {actor_name} 发放了 ${payout} 的{'破产' if post_funds <= 0 else '低收入'}保障金，防止现金链立刻断掉。",
                        slot=self.state.time_slot,
                        category="general",
                    ),
                )
                self.state.events = self.state.events[:8]
        self._append_finance_record(
            actor_id=actor_id,
            actor_name=actor_name,
            category="consume",
            action="expense",
            summary=f"{actor_name} 完成了一次日常开销结算，支出 ${payment}。当前物价指数 {self.state.market.inflation_index:.1f}{'，但手头已经有点吃紧。' if payment < cost else '。'}",
            amount=-payment,
            asset_name="日常开销",
            counterparty="生活结算",
        )

    def _item_by_id(self, item_id: str) -> ConsumableItem:
        for item in self.state.lifestyle_catalog:
            if item.id == item_id:
                return item
        raise KeyError(item_id)

    def _property_by_id(self, property_id: str) -> PropertyAsset:
        for asset in self.state.properties:
            if asset.id == property_id:
                return asset
        raise KeyError(property_id)

    def _casino_asset(self) -> PropertyAsset | None:
        return next((asset for asset in self.state.properties if asset.id == "property-underground-casino"), None)

    def _casino_staging_points(self) -> list[Point]:
        casino = self._casino_asset()
        if casino is None:
            return []
        candidates = [
            Point(x=casino.position.x - 1, y=casino.position.y + 1),
            Point(x=casino.position.x + casino.width, y=casino.position.y + 1),
            Point(x=casino.position.x, y=casino.position.y + casino.height),
            Point(x=casino.position.x + casino.width - 1, y=casino.position.y + casino.height),
        ]
        points: list[Point] = []
        for candidate in candidates:
            safe = self._nearest_walkable(candidate, self._room(self._room_for(candidate.x, candidate.y)))
            if (safe.x, safe.y) not in {(point.x, point.y) for point in points}:
                points.append(safe)
        return points

    def _is_player_near_property(self, asset: PropertyAsset, radius: int = 2) -> bool:
        left = asset.position.x
        top = asset.position.y
        right = asset.position.x + max(0, asset.width - 1)
        bottom = asset.position.y + max(0, asset.height - 1)
        px = self.state.player.position.x
        py = self.state.player.position.y
        dx = 0 if left <= px <= right else min(abs(px - left), abs(px - right))
        dy = 0 if top <= py <= bottom else min(abs(py - top), abs(py - bottom))
        return dx + dy <= radius

    def _trigger_casino_activity(self) -> None:
        casino = self._casino_asset()
        if casino is None or casino.status not in {"owned", "operating"}:
            return
        self.state.casino.current_heat = max(8, int(self.state.casino.current_heat * 0.96))
        staging_points = self._casino_staging_points()
        if not staging_points:
            return
        actor_slots = iter(staging_points)
        triggered = 0
        tourist_triggered = 0
        for agent in self.state.agents:
            if triggered >= 2:
                break
            if agent.is_resting:
                continue
            total_funds = self._agent_total_funds(agent)
            high_cash = total_funds >= 2500
            tight_cash = total_funds <= 90
            high_mood = agent.state.mood >= 76 or agent.life_satisfaction >= 82
            if not (high_cash or tight_cash or high_mood):
                continue
            chance = 0.022 + (0.032 if tight_cash else 0.0) + (0.022 if high_cash else 0.0) + (0.016 if high_mood else 0.0)
            if self.random.random() >= min(0.1, chance):
                continue
            stake = self._suggest_agent_casino_stake(agent, tight_cash=tight_cash, high_cash=high_cash)
            if stake <= 0 or agent.cash < stake:
                continue
            point = next(actor_slots, staging_points[triggered % len(staging_points)]).model_copy()
            result = self._resolve_casino_round(
                payer_type="agent",
                payer_id=agent.id,
                payer_name=agent.name,
                available_cash=agent.cash,
                stake=stake,
                trigger="desperation" if tight_cash else "thrill",
            )
            agent.cash = max(0, agent.cash - int(result["stake"]))
            if int(result["payout"]) > 0:
                agent.cash += int(result["payout"])
            agent.position = point
            agent.current_location = self._room_for(point.x, point.y)
            agent.current_activity = f"刚从后巷地下赌场牌桌边退下来，手心还在冒汗。"
            agent.current_bubble = "再压一手，还是现在就走？"
            agent.last_trade_summary = f"刚在后巷地下赌场下注 ${stake}，{result['outcome']}，净变化 ${result['net']}。"
            self._shift_agent_state(agent, mood=3 if int(result["net"]) > 0 else -2, stress=int(result["stress"]), curiosity=1)
            self._adjust_agent_satisfaction(agent, int(result["satisfaction"]))
            if int(result["net"]) > 0:
                agent.consumption_desire = self._bounded(agent.consumption_desire + min(8, max(2, int(result["net"]) // 70)))
            else:
                agent.money_urgency = self._bounded(agent.money_urgency + min(10, max(2, abs(int(result["net"])) // 60)))
            self._remember(agent, f"你刚在后巷地下赌场下注 ${stake}，{result['outcome']}。", 2, long_term=stake >= 120)
            self._append_finance_record(
                actor_id=agent.id,
                actor_name=agent.name,
                category="casino",
                action="gamble",
                summary=f"{agent.name} 在 {casino.name} 下注 ${stake}，{result['outcome']}，净变化 ${result['net']}，赌税 ${result['tax']}。",
                amount=int(result["net"]),
                asset_name=casino.name,
                counterparty="灰市牌桌",
            )
            self._append_casino_dialogue_record(
                actor_id=agent.id,
                actor_name=agent.name,
                actor_role="智能体",
                stake=stake,
                outcome_text=str(result["outcome"]),
                net_delta=int(result["net"]),
                payout=int(result["payout"]),
                tax=int(result["tax"]),
            )
            self._record_casino_stats(stake=stake, payout=int(result["payout"]), tax=int(result["tax"]), actor_name=agent.name, actor_type="agent")
            self._maybe_register_casino_case(actor_id=agent.id, actor_name=agent.name, actor_type="agent", stake=stake, net_delta=int(result["net"]), trigger="desperation" if tight_cash else "thrill")
            self._maybe_publish_casino_buzz(actor_name=agent.name, actor_type="agent", stake=stake, outcome_text=str(result["outcome"]), net_delta=int(result["net"]), tourist=False)
            self._apply_casino_social_effects(agent, stake=stake, net_delta=int(result["net"]))
            self._append_casino_event(agent.name, stake, str(result["outcome"]), int(result["net"]), tourist=False)
            self._log("agent_gamble", agent={"id": agent.id, "name": agent.name}, wager={"stake": stake, "tax": result["tax"], "payout": result["payout"], "net": result["net"]})
            triggered += 1
        for tourist in self._active_tourists():
            if tourist_triggered >= 2:
                break
            high_cash = tourist.cash >= 90
            tight_cash = tourist.cash <= 24
            high_mood = tourist.mood >= 68 or tourist.spending_desire >= 74
            thrill_tier = tourist.visitor_tier in {"repeat", "vip"}
            hot_table = self.state.casino.current_heat >= 24
            prime_time = self.state.time_slot in {"evening", "night"}
            if not (high_cash or tight_cash or high_mood or thrill_tier or hot_table):
                continue
            chance = 0.02
            chance += 0.022 if tight_cash else 0.0
            chance += 0.018 if high_cash else 0.0
            chance += 0.02 if high_mood else 0.0
            chance += 0.012 if thrill_tier else 0.0
            chance += 0.01 if hot_table else 0.0
            chance += 0.01 if prime_time else 0.0
            if tourist.visitor_tier == "buyer":
                chance *= 0.9
            if self.random.random() >= min(0.14, chance):
                continue
            stake = self._suggest_tourist_casino_stake(tourist, tight_cash=tight_cash, high_cash=high_cash)
            if stake <= 0 or tourist.cash < stake:
                continue
            point = staging_points[triggered % len(staging_points)].model_copy()
            result = self._resolve_casino_round(
                payer_type="tourist",
                payer_id=tourist.id,
                payer_name=tourist.name,
                available_cash=tourist.cash,
                stake=stake,
                trigger="tourist",
            )
            tourist.cash = max(0, tourist.cash - int(result["stake"]))
            if int(result["payout"]) > 0:
                tourist.cash += int(result["payout"])
            tourist.position = point
            tourist.current_location = self._room_for(point.x, point.y)
            tourist.current_activity = "刚在后巷地下赌场围着牌桌试了试手气，还在回味输赢。"
            tourist.current_bubble = "这地方真敢玩。"
            tourist.mood = self._bounded(tourist.mood + (4 if int(result["net"]) > 0 else -2))
            tourist.spending_desire = self._bounded(tourist.spending_desire + (4 if int(result["net"]) > 0 else -1))
            self._remember_tourist(tourist, f"你刚在后巷地下赌场下注 ${stake}，{result['outcome']}。", 2)
            self._append_finance_record(
                actor_id=tourist.id,
                actor_name=tourist.name,
                category="casino",
                action="gamble",
                summary=f"{tourist.name} 在 {casino.name} 下注 ${stake}，{result['outcome']}，净变化 ${result['net']}，赌税 ${result['tax']}。",
                amount=int(result["net"]),
                asset_name=casino.name,
                counterparty="灰市牌桌",
            )
            self._append_casino_dialogue_record(
                actor_id=tourist.id,
                actor_name=tourist.name,
                actor_role="游客",
                stake=stake,
                outcome_text=str(result["outcome"]),
                net_delta=int(result["net"]),
                payout=int(result["payout"]),
                tax=int(result["tax"]),
            )
            self._record_casino_stats(stake=stake, payout=int(result["payout"]), tax=int(result["tax"]), actor_name=tourist.name, actor_type="tourist")
            self._maybe_register_casino_case(actor_id=tourist.id, actor_name=tourist.name, actor_type="tourist", stake=stake, net_delta=int(result["net"]), trigger="tourist")
            self._maybe_publish_casino_buzz(actor_name=tourist.name, actor_type="tourist", stake=stake, outcome_text=str(result["outcome"]), net_delta=int(result["net"]), tourist=True)
            self._publish_tourist_casino_post(tourist, stake=stake, net_delta=int(result["net"]), outcome_text=str(result["outcome"]))
            self._append_casino_event(tourist.name, stake, str(result["outcome"]), int(result["net"]), tourist=True)
            self._log("tourist_gamble", tourist={"id": tourist.id, "name": tourist.name}, wager={"stake": stake, "tax": result["tax"], "payout": result["payout"], "net": result["net"]})
            tourist_triggered += 1

    def _suggest_agent_casino_stake(self, agent: Agent, *, tight_cash: bool, high_cash: bool) -> int:
        if tight_cash:
            return max(8, min(agent.cash, 20 + agent.money_urgency // 7))
        if high_cash:
            return max(60, min(agent.cash // 5, 220 + agent.risk_appetite * 2 + agent.money_urgency))
        return max(15, min(agent.cash // 6, 96 + agent.state.mood // 2 + agent.risk_appetite // 3))

    def _suggest_tourist_casino_stake(self, tourist: TouristAgent, *, tight_cash: bool, high_cash: bool) -> int:
        if tight_cash:
            return max(6, min(tourist.cash, 14))
        if high_cash:
            bonus = 80 if tourist.visitor_tier == "vip" else 40 if tourist.visitor_tier == "buyer" else 0
            return max(16, min(tourist.cash // 5, 96 + bonus))
        return max(8, min(tourist.cash // 6, 42))

    def _property_owner_name(self, asset: PropertyAsset) -> str:
        if asset.owner_type == "player":
            return self.state.player.name
        if asset.owner_type == "agent":
            return self._find_agent(asset.owner_id).name
        if asset.owner_type == "government":
            return self.state.government.name
        return "市场"

    def _active_property_assets(self, owner_type: str, owner_id: str) -> list[PropertyAsset]:
        return [asset for asset in self.state.properties if asset.owner_type == owner_type and asset.owner_id == owner_id and asset.status == "owned"]

    def _player_lifestyle_burden(self) -> int:
        loan_burden = sum(max(1, loan.amount_due // max(1, loan.term_days)) for loan in self._borrower_bank_loans("player", self.state.player.id))
        property_burden = sum(asset.daily_maintenance for asset in self._active_property_assets("player", self.state.player.id))
        return loan_burden + property_burden

    def _agent_lifestyle_burden(self, agent: Agent) -> int:
        loan_burden = sum(max(1, loan.amount_due // max(1, loan.term_days)) for loan in self._borrower_bank_loans("agent", agent.id))
        property_burden = sum(asset.daily_maintenance for asset in self._active_property_assets("agent", agent.id))
        return loan_burden + property_burden

    def _maybe_player_finance_gap(self, cost: int, reason: str, financed: bool, term_days: int) -> None:
        if self.state.player.cash >= cost:
            return
        if not financed:
            raise ValueError(f"当前现金只有 ${self.state.player.cash}，不够支付 ${cost}。可以勾选贷款购买。")
        gap = cost - self.state.player.cash
        self._bank_borrow("player", self.state.player.id, gap, term_days, reason, manual=True)

    def _adjust_player_satisfaction(self, delta: int) -> None:
        self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + delta)

    def _adjust_agent_satisfaction(self, agent: Agent, delta: int) -> None:
        agent.life_satisfaction = self._bounded(agent.life_satisfaction + delta)

    def _consume_coupon(self, *, holder_type: str, holder_id: str, amount: int) -> int:
        if amount <= 0:
            return 0
        if holder_type == "player":
            applied = min(amount, self.state.player.consumption_coupon_balance)
            self.state.player.consumption_coupon_balance = max(0, self.state.player.consumption_coupon_balance - applied)
            return applied
        agent = self._find_agent(holder_id)
        applied = min(amount, agent.consumption_coupon_balance)
        agent.consumption_coupon_balance = max(0, agent.consumption_coupon_balance - applied)
        return applied

    def _player_consume_item(self, item_id: str, recipient_id: str, financed: bool = False) -> None:
        item = self._item_by_id(item_id)
        recipient_name = self.state.player.name
        relation_delta = 0
        recipient_agent: Agent | None = None
        if recipient_id != "player":
            recipient_agent = self._find_agent(recipient_id)
            if not item.giftable:
                raise ValueError("这件物品不适合送给别人。")
            recipient_name = recipient_agent.name
        coupon_used = self._consume_coupon(holder_type="player", holder_id=self.state.player.id, amount=item.price)
        net_payment = max(0, item.price - coupon_used)
        self._maybe_player_finance_gap(net_payment, f"购买{item.name}", financed=financed and item.debt_eligible, term_days=1)
        self.state.player.cash = max(0, self.state.player.cash - net_payment)
        consume_tax = self._collect_tax(
            payer_type="player",
            payer_id=self.state.player.id,
            payer_name=self.state.player.name,
            revenue_key="consumption",
            label="消费支出",
            base_amount=net_payment,
            rate_pct=self.state.government.consumption_tax_rate_pct + (self.state.government.luxury_tax_rate_pct if item.price >= 18 else 0.0),
        )
        self._adjust_player_satisfaction(item.satisfaction_gain + (1 if recipient_agent else 0))
        self.state.player.monthly_burden = self._player_lifestyle_burden()
        if recipient_agent is None:
            self.state.player.housing_quality = self._bounded(self.state.player.housing_quality + item.comfort_gain)
            self.state.player.last_trade_summary = f"刚买了{item.name}，现金支出 ${net_payment}，消费券抵扣 ${coupon_used}，另缴税 ${consume_tax}。"
            summary = f"你刚买了{item.name}，生活满意度有些回升。"
        else:
            recipient_agent.state.mood = self._bounded(recipient_agent.state.mood + item.mood_gain)
            recipient_agent.state.energy = self._bounded(recipient_agent.state.energy + item.energy_gain)
            recipient_agent.housing_quality = self._bounded(recipient_agent.housing_quality + item.comfort_gain)
            self._adjust_agent_satisfaction(recipient_agent, item.satisfaction_gain)
            relation_delta = item.relation_bonus or 1
            self._adjust_player_relation(recipient_agent, relation_delta, f"你送了 {recipient_agent.name} 一份{item.name}。")
            self.state.player.last_trade_summary = f"刚给 {recipient_agent.name} 买了{item.name}，现金支出 ${net_payment}，消费券抵扣 ${coupon_used}，另缴税 ${consume_tax}。"
            recipient_agent.current_bubble = f"{item.name} 还挺让人开心。"
            recipient_agent.last_interaction = f"你刚送了他一份{item.name}。"
            self._remember(recipient_agent, f"玩家刚送了你一份{item.name}。", 2)
            summary = f"你给 {recipient_agent.name} 买了{item.name}，这轮关系和满意度都往上走了一点。"
        self.state.player.daily_actions.append(f"consume:{item.name}->{recipient_name}")
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"发生了一笔生活消费：{item.name}",
                summary=summary,
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="player_dialogue",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=["player"] + ([recipient_agent.id] if recipient_agent else []),
                participant_names=[self.state.player.name] + ([recipient_agent.name] if recipient_agent else []),
                topic=f"消费：{item.name}",
                summary=summary,
                key_point=f"你支付 ${net_payment}，消费券抵扣 ${coupon_used}，购买{item.name}，另缴税 ${consume_tax}，生活满意度 {item.satisfaction_gain:+d}。",
                transcript=[f"你：先买个{item.name}。", f"{recipient_name}：这笔消费让这会儿舒服多了。"],
                desire_labels={self.state.player.name: "把日子过舒服一点", recipient_name: "获得一点现实回报"},
                mood="warm",
                financial_note=f"现金消费 ${net_payment}，消费券 ${coupon_used}，满意度 +{item.satisfaction_gain}，关系变化 {relation_delta:+d}",
            )
        )
        self._append_finance_record(
            actor_id=self.state.player.id,
            actor_name=self.state.player.name,
            category="consume",
            action="buy",
            summary=f"你购买了 {item.name}，现金支出 ${net_payment}，消费券抵扣 ${coupon_used}，税费 ${consume_tax}。{f' 送给了 {recipient_name}。' if recipient_agent else ''}",
            amount=net_payment + consume_tax,
            asset_name=item.name,
            counterparty=recipient_name if recipient_agent else "生活消费",
            financed=financed and item.debt_eligible,
        )
        self._log("player_consumption", item=item.model_dump(), recipient=recipient_id, financed=financed)
        self._refresh_presence()

    def _player_buy_property(self, property_id: str, financed: bool = False) -> None:
        asset = self._property_by_id(property_id)
        if asset.owner_type not in {"market", "government"} or asset.status != "listed":
            raise ValueError("这处地产当前不在出售。")
        seller_type = asset.owner_type
        self._maybe_player_finance_gap(asset.purchase_price, f"购买地产 {asset.name}", financed=financed and asset.debt_eligible, term_days=3)
        self.state.player.cash = max(0, self.state.player.cash - asset.purchase_price)
        transfer_tax = self._collect_tax(
            payer_type="player",
            payer_id=self.state.player.id,
            payer_name=self.state.player.name,
            revenue_key="property",
            label="地产过户",
            base_amount=asset.purchase_price,
            rate_pct=self.state.government.property_transfer_tax_rate_pct,
        )
        asset.owner_type = "player"
        asset.owner_id = self.state.player.id
        asset.status = "owned"
        asset.listed = False
        asset.built = True
        if asset.id not in self.state.player.owned_property_ids:
            self.state.player.owned_property_ids.append(asset.id)
        self.state.player.housing_quality = self._bounded(self.state.player.housing_quality + asset.comfort_bonus)
        self._adjust_player_satisfaction(6 + asset.social_bonus)
        self.state.player.monthly_burden = self._player_lifestyle_burden()
        self.state.player.last_trade_summary = f"刚买下{asset.name}，成交 ${asset.purchase_price}，税费 ${transfer_tax}。"
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"你买下了{asset.name}",
                summary=f"这笔地产交易花了 ${asset.purchase_price}，后续每天会带来收益和维护成本。",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]
        self._append_finance_record(
            actor_id=self.state.player.id,
            actor_name=self.state.player.name,
            category="property",
            action="buy",
            summary=f"你买下了 {asset.name}，成交价 ${asset.purchase_price}，过户税 ${transfer_tax}。",
            amount=asset.purchase_price + transfer_tax,
            asset_name=asset.name,
            counterparty="财政资产" if seller_type == "government" else "地产市场",
            financed=financed and asset.debt_eligible,
        )
        self._log("player_property_purchase", property=asset.model_dump(), financed=financed)
        self._refresh_presence()

    def _player_sell_property(self, property_id: str) -> None:
        asset = self._property_by_id(property_id)
        if asset.owner_type != "player" or asset.owner_id != self.state.player.id:
            raise ValueError("这处地产不属于你。")
        if asset.id == "property-player-cottage":
            raise ValueError("你当前的小屋不能直接卖掉。")
        payout = max(12, int(round(asset.estimated_value * 0.82)))
        self.state.player.cash += payout
        transfer_tax = self._collect_tax(
            payer_type="player",
            payer_id=self.state.player.id,
            payer_name=self.state.player.name,
            revenue_key="property",
            label="地产转让",
            base_amount=payout,
            rate_pct=max(1.5, self.state.government.property_transfer_tax_rate_pct * 0.7),
        )
        asset.owner_type = "market"
        asset.owner_id = "market"
        asset.status = "listed"
        asset.listed = True
        if asset.id in self.state.player.owned_property_ids:
            self.state.player.owned_property_ids.remove(asset.id)
        self.state.player.housing_quality = self._bounded(self.state.player.housing_quality - max(0, asset.comfort_bonus // 2))
        self._adjust_player_satisfaction(-2 + max(0, asset.daily_income // 6))
        self.state.player.monthly_burden = self._player_lifestyle_burden()
        self.state.player.last_trade_summary = f"刚卖出{asset.name}，回笼 ${max(0, payout - transfer_tax)}。"
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"你卖出了{asset.name}",
                summary=f"卖出后回笼 ${payout}，相应的日收益和维护责任也一起移除了。",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]
        self._append_finance_record(
            actor_id=self.state.player.id,
            actor_name=self.state.player.name,
            category="property",
            action="sell",
            summary=f"你卖出了 {asset.name}，回笼 ${payout}，转让税 ${transfer_tax}。",
            amount=max(0, payout - transfer_tax),
            asset_name=asset.name,
            counterparty="地产市场",
        )
        self._log("player_property_sale", property=asset.id, payout=payout)
        self._refresh_presence()

    def _refresh_lifestyle_state(self) -> None:
        self.state.player.monthly_burden = self._player_lifestyle_burden()
        player_relation_avg = int(sum(self.state.player.social_links.values()) / max(1, len(self.state.player.social_links))) if self.state.player.social_links else 0
        self.state.player.consumption_desire = self._bounded(
            28
            + self.state.player.materialism // 2
            + max(0, 55 - self.state.player.life_satisfaction) // 2
            + max(0, self.state.company.low_cash_threshold + 8 - self.state.player.cash) // 3
            + max(0, 55 - self.state.player.housing_quality) // 3
            + (self.state.market.living_cost_pressure // 9)
            + (4 if self.state.weather in {"drizzle", "breezy"} else 0)
            + max(0, player_relation_avg // 10)
            - self.state.player.monthly_burden // 4
        )
        for agent in self.state.agents:
            agent.monthly_burden = self._agent_lifestyle_burden(agent)
            relation_avg = int(sum(agent.relations.values()) / max(1, len(agent.relations))) if agent.relations else 0
            agent.consumption_desire = self._bounded(
                25
                + agent.materialism // 2
                + max(0, 55 - agent.life_satisfaction) // 2
                + max(0, self.state.company.low_cash_threshold + 6 - agent.cash) // 3
                + max(0, 50 - agent.housing_quality) // 3
                + max(0, agent.state.stress - 55) // 5
                + (self.state.market.living_cost_pressure // 10)
                + max(0, relation_avg // 12)
                - agent.monthly_burden // 4
            )

    def _trigger_property_market_activity(self) -> None:
        listed_assets = [asset for asset in self.state.properties if asset.status == "listed" and asset.owner_type in {"market", "government"}]
        if not listed_assets:
            return
        for agent in self.state.agents:
            if agent.is_resting or agent.cash < 90 or len(agent.owned_property_ids or []) >= 3:
                continue
            buy_bias = (
                0.06
                + max(0, 62 - agent.housing_quality) / 220
                + max(0, agent.cash - 110) / 850
                + (0.08 if agent.persona in {"opportunist", "empathetic"} else 0.0)
            )
            if self.random.random() > min(0.24, buy_bias):
                continue
            affordable = [asset for asset in listed_assets if asset.purchase_price <= max(agent.cash, agent.cash + min(30, agent.credit_score // 2))]
            if not affordable:
                continue
            asset = sorted(
                affordable,
                key=lambda item: (
                    item.property_type not in {"rental_house", "shop"},
                    abs(item.comfort_bonus - max(4, 12 - agent.housing_quality // 12)),
                    item.purchase_price,
                ),
            )[0]
            financed = asset.purchase_price > agent.cash and asset.debt_eligible and agent.credit_score >= 55
            if financed:
                gap = asset.purchase_price - agent.cash
                try:
                    self._bank_borrow("agent", agent.id, gap, 3, f"想买下 {asset.name} 做长期资产。")
                except ValueError:
                    continue
            if agent.cash < asset.purchase_price:
                continue
            seller_type = asset.owner_type
            agent.cash -= asset.purchase_price
            transfer_tax = self._collect_tax(
                payer_type="agent",
                payer_id=agent.id,
                payer_name=agent.name,
                revenue_key="property",
                label="地产过户",
                base_amount=asset.purchase_price,
                rate_pct=self.state.government.property_transfer_tax_rate_pct,
            )
            if seller_type == "government":
                if asset.id in self.state.government.government_asset_ids:
                    self.state.government.government_asset_ids.remove(asset.id)
                self.state.government.reserve_balance += asset.purchase_price
                self.state.government.revenues["government_asset"] = self.state.government.revenues.get("government_asset", 0) + asset.purchase_price
            asset.owner_type = "agent"
            asset.owner_id = agent.id
            asset.status = "owned"
            asset.listed = False
            asset.built = True
            if asset.id not in agent.owned_property_ids:
                agent.owned_property_ids.append(asset.id)
            agent.housing_quality = self._bounded(agent.housing_quality + asset.comfort_bonus)
            self._adjust_agent_satisfaction(agent, 5 + asset.social_bonus)
            agent.last_trade_summary = f"刚买下 {asset.name}，成交 ${asset.purchase_price}，税费 ${transfer_tax}。"
            self._remember(agent, f"你刚买下 {asset.name}，想用它改善住处和现金流。", 3, long_term=True)
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{agent.name} 买下了 {asset.name}",
                    summary=f"{agent.name} 花 ${asset.purchase_price} 买下 {asset.name}，准备把它当成长期资产来运营。",
                    slot=self.state.time_slot,
                    category="market",
                ),
            )
            self._append_finance_record(
                actor_id=agent.id,
                actor_name=agent.name,
                category="property",
                action="buy",
                summary=f"{agent.name} 买下了 {asset.name}，成交价 ${asset.purchase_price}，过户税 ${transfer_tax}。",
                amount=asset.purchase_price + transfer_tax,
                asset_name=asset.name,
                counterparty="财政资产" if seller_type == "government" else "地产市场",
                financed=financed,
            )
            listed_assets = [candidate for candidate in listed_assets if candidate.id != asset.id]
            if not listed_assets:
                break
        self.state.events = self.state.events[:8]

    def _settle_property_income(self) -> None:
        for asset in self.state.properties:
            if asset.status != "owned":
                continue
            owner_name = self._property_owner_name(asset)
            net_income = asset.daily_income - asset.daily_maintenance
            holding_tax = 0
            if asset.estimated_value > 0:
                base_holding = max(0, net_income) + max(2, round(asset.estimated_value / 180))
                holding_tax = max(1, round(base_holding * self.state.government.property_holding_tax_rate_pct / 100))
            if asset.owner_type == "player":
                self.state.player.cash = max(0, self.state.player.cash + net_income)
                if holding_tax:
                    self._collect_tax(
                        payer_type="player",
                        payer_id=self.state.player.id,
                        payer_name=self.state.player.name,
                        revenue_key="property",
                        label="房产持有",
                        base_amount=holding_tax,
                        rate_pct=100.0,
                    )
                self.state.player.housing_quality = self._bounded(self.state.player.housing_quality + max(0, asset.comfort_bonus // 4))
                self._adjust_player_satisfaction(max(-2, asset.comfort_bonus // 3))
                if asset.daily_income or asset.daily_maintenance:
                    self.state.player.last_trade_summary = f"{asset.name} 昨天税后净额 ${max(0, net_income - holding_tax)}。"
            elif asset.owner_type == "agent":
                owner = self._find_agent(asset.owner_id)
                owner.cash = max(0, owner.cash + net_income)
                if holding_tax:
                    self._collect_tax(
                        payer_type="agent",
                        payer_id=owner.id,
                        payer_name=owner.name,
                        revenue_key="property",
                        label="房产持有",
                        base_amount=holding_tax,
                        rate_pct=100.0,
                    )
                owner.housing_quality = self._bounded(owner.housing_quality + max(0, asset.comfort_bonus // 4))
                self._adjust_agent_satisfaction(owner, max(-2, asset.comfort_bonus // 3))
                if asset.daily_income or asset.daily_maintenance:
                    owner.last_trade_summary = f"{asset.name} 昨天税后净额 ${max(0, net_income - holding_tax)}。"
            elif asset.owner_type == "government":
                self.state.government.reserve_balance = max(0, self.state.government.reserve_balance + net_income)
                self.state.government.revenues["government_asset"] = self.state.government.revenues.get("government_asset", 0) + max(0, net_income)
                if holding_tax:
                    self.state.government.revenues["property"] = self.state.government.revenues.get("property", 0) + holding_tax
                    self.state.government.total_revenue += holding_tax
                self.state.government.last_distribution_note = f"政府资产 {asset.name} 昨天结算净额 ${max(0, net_income - holding_tax)}。"
            if asset.daily_income or asset.daily_maintenance:
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=f"{asset.name} 完成了一次日结",
                        summary=f"{owner_name} 的 {asset.name} 昨天结算净额 ${net_income}，持有税 ${holding_tax}。",
                        slot=self.state.time_slot,
                        category="market",
                    ),
                )
                owner_id = self.state.player.id if asset.owner_type == "player" else asset.owner_id
                self._append_finance_record(
                    actor_id=owner_id,
                    actor_name=owner_name,
                    category="government" if asset.owner_type == "government" else "property",
                    action="settle",
                    summary=f"{owner_name} 的 {asset.name} 完成日结，净额 ${net_income}，持有税 ${holding_tax}。",
                    amount=net_income - holding_tax,
                    asset_name=asset.name,
                    counterparty="地产结算",
                )
        self.state.events = self.state.events[:8]

    def _trigger_lifestyle_activity(self) -> None:
        if not self.state.market.is_open:
            return
        for agent in self.state.agents:
            desire_bias = 0.12 + agent.consumption_desire / 320 + agent.materialism / 500
            if agent.is_resting or self.random.random() > min(0.34, desire_bias):
                continue
            candidate_items = []
            for item in self.state.lifestyle_catalog:
                effective_cash = agent.cash + agent.consumption_coupon_balance
                if item.price <= effective_cash:
                    candidate_items.append(item)
                elif item.debt_eligible and agent.credit_score >= 55 and effective_cash >= max(4, item.price // 3):
                    candidate_items.append(item)
            if not candidate_items:
                continue
            if agent.consumption_desire < 40 and agent.life_satisfaction > 62:
                continue
            if agent.cash < 8 and agent.credit_score < 45:
                continue
            item = self.random.choice(candidate_items)
            gifted = item.giftable and self.random.random() < 0.36
            target = None
            if gifted:
                nearby = [other for other in self.state.agents if other.id != agent.id and abs(other.position.x - agent.position.x) + abs(other.position.y - agent.position.y) <= 6]
                if nearby:
                    target = sorted(nearby, key=lambda other: other.relations.get(agent.id, 0), reverse=True)[0]
            if agent.cash < item.price and item.debt_eligible:
                gap = item.price - agent.cash
                try:
                    self._bank_borrow("agent", agent.id, gap, 1, f"想买{item.name}，先周转一下。")
                except ValueError:
                    continue
            coupon_used = self._consume_coupon(holder_type="agent", holder_id=agent.id, amount=item.price)
            net_payment = max(0, item.price - coupon_used)
            if agent.cash < net_payment:
                continue
            agent.cash -= net_payment
            consume_tax = self._collect_tax(
                payer_type="agent",
                payer_id=agent.id,
                payer_name=agent.name,
                revenue_key="consumption",
                label="消费支出",
                base_amount=net_payment,
                rate_pct=self.state.government.consumption_tax_rate_pct + (self.state.government.luxury_tax_rate_pct if item.price >= 18 else 0.0),
            )
            agent.state.mood = self._bounded(agent.state.mood + item.mood_gain)
            agent.state.energy = self._bounded(agent.state.energy + item.energy_gain)
            agent.housing_quality = self._bounded(agent.housing_quality + item.comfort_gain)
            self._adjust_agent_satisfaction(agent, item.satisfaction_gain)
            agent.current_bubble = f"先花点钱把这会儿过舒服。"
            agent.last_trade_summary = f"刚买了{item.name}，现金支出 ${net_payment}，消费券抵扣 ${coupon_used}，另缴税 ${consume_tax}。"
            self._remember(agent, f"你刚花 ${net_payment} 现金并用 ${coupon_used} 消费券买了{item.name}。", 2)
            summary = f"{agent.name} 刚买了{item.name}，生活满意度和状态往上提了一点。"
            if target is not None:
                target.state.mood = self._bounded(target.state.mood + item.mood_gain)
                self._adjust_agent_satisfaction(target, max(1, item.satisfaction_gain - 1))
                self._adjust_relation(agent, target, item.relation_bonus, f"一起围绕 {item.name} 发生了一笔生活消费")
                target.current_bubble = f"{agent.name} 刚给我带了{item.name}。"
                summary = f"{agent.name} 刚给 {target.name} 买了{item.name}，两个人的生活满意度和关系都有点上升。"
            self.state.events.insert(0, build_internal_event(title=f"{agent.name} 发生了一笔生活消费", summary=summary, slot=self.state.time_slot, category="general"))
            self._append_finance_record(
                actor_id=agent.id,
                actor_name=agent.name,
                category="consume",
                action="buy",
                summary=f"{agent.name} 购买了 {item.name}，现金支出 ${net_payment}，消费券抵扣 ${coupon_used}，税费 ${consume_tax}。{f' 目标是 {target.name}。' if target else ''}",
                amount=net_payment + consume_tax,
                asset_name=item.name,
                counterparty=target.name if target else "生活消费",
                financed=False,
            )
        self.state.events = self.state.events[:8]

    def _refresh_agent_plans(self) -> None:
        latest_event = self.state.events[0].title if self.state.events else "今天的研究安排"
        for agent in self.state.agents:
            money_pressure = self._money_pressure(agent)
            agent.money_urgency = money_pressure
            if agent.is_resting:
                agent.social_stance = "observe"
                agent.current_plan = f"先在{agent.home_label or '小屋'}补觉，等明早再出来。"
                agent.immediate_intent = "想安静休息，不想被打断。"
                continue
            partner_name = self._agent_name(agent.allies[0]) if agent.allies else "别人"
            rival_name = self._agent_name(agent.rivals[0]) if agent.rivals else "阻力"
            resource_name = RESOURCE_LABELS.get(agent.desired_resource, agent.desired_resource)
            if agent.cash < self.state.company.low_cash_threshold:
                agent.social_stance = "compete"
                agent.current_plan = f"现金只剩 ${agent.cash}，得先去{self.state.company.name}打一轮工，再谈股票、借贷或消费。"
                agent.immediate_intent = f"想先在{self.state.company.location_label}干一轮活，把现金补到安全线以上。"
                continue
            if money_pressure >= 92:
                agent.social_stance = "compete"
                agent.current_plan = f"手头只剩 ${agent.cash}，得明确借钱、接活或先卖点持仓。"
                agent.immediate_intent = "想把话说明白，尽快弄到钱或者腾出现金。"
                continue
            if agent.cash <= 72 and money_pressure >= 68:
                agent.social_stance = "compete"
                agent.current_plan = f"手头只剩 ${agent.cash}，想找明确的借款、帮忙或市场机会。"
                agent.immediate_intent = "想把话题往预算、合作回报或股票上带。"
                continue
            if agent.state.stress >= 68:
                agent.social_stance = "defensive"
                agent.current_plan = f"先守住{resource_name}，不想被 {rival_name} 再打乱节奏。"
                agent.immediate_intent = f"想先把自己的节奏护住，不想再被{rival_name}扰乱。"
            elif agent.persona == "empathetic":
                agent.social_stance = "mediate"
                agent.current_plan = f"准备观察谁快顶不住了，必要时去替 {partner_name} 缓一口气。"
                agent.immediate_intent = f"想先看看谁状态在掉，再决定去接哪句话。"
            elif agent.persona in {"rational", "engineering"} and ("GeoAI" in latest_event or "复盘" in latest_event):
                agent.social_stance = "cooperate"
                agent.current_plan = f"想拉 {partner_name} 一起围绕“{latest_event}”把{resource_name}做扎实。"
                agent.immediate_intent = f"想把“{latest_event}”说得更实一点，最好顺手拉上{partner_name}。"
            elif agent.persona in {"creative", "opportunist"} and self.state.lab.external_sensitivity >= 24:
                agent.social_stance = "compete"
                agent.current_plan = f"想抢在 {rival_name} 前把新的{resource_name}推进到台面上。"
                agent.immediate_intent = f"想先把新动静说出来，免得又被{rival_name}压下去。"
            else:
                agent.social_stance = "observe"
                agent.current_plan = f"继续盯着{resource_name}，看谁值得合作、谁可能挡路。"
                agent.immediate_intent = "想先随口聊聊，再判断这轮该靠近谁。"

    def _refresh_memory_streams(self) -> None:
        latest_event = self.state.events[0].title if self.state.events else "今天暂时没出大事"
        latest_brief = self.state.daily_briefings[0] if self.state.daily_briefings else None
        for agent in self.state.agents:
            items: list[str] = []
            if agent.immediate_intent:
                items.append(f"眼下最在意：{agent.immediate_intent}")
            items.append(f"当前状态：心情{agent.state.mood}，压力{agent.state.stress}，体力{agent.state.energy}，现金${agent.cash}")
            items.append(f"金钱倾向：渴望{agent.money_desire}，当前压力{agent.money_urgency}，信用{agent.credit_score}，慷慨{agent.generosity}")
            if agent.portfolio:
                holdings = "，".join(f"{symbol}×{shares}" for symbol, shares in sorted(agent.portfolio.items()))
                items.append(f"持仓：{holdings}")
            debt = next((loan for loan in self.state.loans if loan.status in {"active", "overdue"} and (loan.borrower_id == agent.id or loan.lender_id == agent.id)), None)
            if debt is not None:
                if debt.borrower_id == agent.id:
                    items.append(f"借款：明天前要还 ${debt.amount_due}")
                else:
                    items.append(f"借款：明天等着收回 ${debt.amount_due}")
            bank_debt = next((loan for loan in self.state.bank_loans if loan.borrower_type == "agent" and loan.borrower_id == agent.id and loan.status in {"active", "overdue"}), None)
            if bank_debt is not None:
                items.append(f"银行贷款：剩余 ${bank_debt.amount_due}，第 {bank_debt.due_day} 天前处理")
            if agent.short_term_memory:
                items.append(f"刚记住：{agent.short_term_memory[0].text}")
            if agent.long_term_memory:
                long_term = agent.long_term_memory[0]
                if long_term.importance >= 4 or long_term.day < self.state.day:
                    items.append(f"长线挂念：{long_term.text}")
            thread = next((thread for thread in self.state.social_threads if agent.id in thread.participants), None)
            if thread:
                items.append(f"最近对话线：{thread.latest_summary}")
            else:
                items.append(f"外部场景：{latest_event}")
            if latest_brief is not None:
                items.append(f"Lab Daily：{latest_brief.items[0] if latest_brief.items else latest_brief.lead}")
            if agent.current_plan:
                items.append(f"当前打算：{agent.current_plan}")
            agent.memory_stream = items[:6]

    def _trigger_strategy_event(self) -> None:
        if self.random.random() > 0.58:
            return
        if self._maybe_trigger_reconciliation_chain():
            return
        pairs = [
            (first, second)
            for index, first in enumerate(self.state.agents)
            for second in self.state.agents[index + 1 :]
            if not first.is_resting and not second.is_resting
        ]
        if not pairs:
            return
        scored_pairs = []
        for first, second in pairs:
            coop_score = self._cooperation_score(first, second)
            conflict_score = self._conflict_score(first, second)
            score = max(coop_score, conflict_score)
            if score > 0:
                scored_pairs.append((score, coop_score, conflict_score, first, second))
        if not scored_pairs:
            return
        _, coop_score, conflict_score, first, second = max(scored_pairs, key=lambda item: item[0])
        if coop_score >= conflict_score and coop_score >= 3:
            self._run_cooperation_event(first, second)
        elif conflict_score >= 3:
            self._run_conflict_event(first, second)

    def _maybe_trigger_reconciliation_chain(self) -> bool:
        candidates: list[tuple[int, Agent, Agent]] = []
        for index, first in enumerate(self.state.agents):
            for second in self.state.agents[index + 1 :]:
                if first.is_resting or second.is_resting:
                    continue
                relation = (first.relations.get(second.id, 0) + second.relations.get(first.id, 0)) // 2
                if relation > -18:
                    continue
                if max(self._cooldown_for(first, second.id), self._cooldown_for(second, first.id)) > 0:
                    continue
                score = abs(relation) + max(0, 100 - (first.state.stress + second.state.stress))
                if -62 <= relation <= -18:
                    score += 18
                candidates.append((score, first, second))
        if not candidates or self.random.random() > 0.28:
            return False
        _, first, second = max(candidates, key=lambda item: item[0])
        self._run_reconciliation_event(first, second)
        return True

    def _run_reconciliation_event(self, first: Agent, second: Agent) -> None:
        topic = "把之前那点心结讲开"
        existing = next(
            (
                beat
                for beat in self.state.story_beats
                if beat.kind == "reconciliation" and set(beat.participants) == {first.id, second.id}
            ),
            None,
        )
        stage = (existing.stage + 1) if existing is not None else 1
        delta = 3 if stage == 1 else 5 if stage == 2 else 6
        first.current_bubble = "先把那口气放下来吧。"
        second.current_bubble = "行，今天先不继续顶。"
        self._adjust_relation(first, second, delta, "在一段冷却之后，尝试把旧摩擦讲开。")
        self._shift_agent_state(first, mood=2, stress=-4, focus=1)
        self._shift_agent_state(second, mood=2, stress=-4, focus=1)
        first.current_activity = f"正和 {second.name} 试着把旧摩擦讲开。"
        second.current_activity = f"正和 {first.name} 试着把旧摩擦讲开。"
        first.last_interaction = f"刚和 {second.name} 试着和解，至少没再继续往下顶。"
        second.last_interaction = f"刚和 {first.name} 试着和解，气氛稍微缓了一层。"
        title = f"{first.name} 和 {second.name} 开始进入和解链"
        summary = f"{first.name} 和 {second.name} 在冷却一段时间后，试着围绕“{topic}”把旧冲突讲开。第 {stage} 段和解正在形成。"
        self._upsert_story_beat("reconciliation", title, summary, [first.id, second.id], first.current_location)
        self._emit_strategy_event(title, summary, first.current_location)
        self._log("strategy_reconciliation", participants=[first.id, second.id], stage=stage, topic=topic, location=first.current_location)

    def _cooperation_score(self, first: Agent, second: Agent) -> int:
        score = 0
        first_desire, _ = dominant_desire_for_agent(self.state, first)
        second_desire, _ = dominant_desire_for_agent(self.state, second)
        if second.id in first.allies or first.id in second.allies:
            score += 3
        relation = (first.relations.get(second.id, 0) + second.relations.get(first.id, 0)) // 2
        if relation >= 30:
            score += 2
        if first.desired_resource == second.desired_resource:
            score += 1
        if "GeoAI" in first.current_plan and "GeoAI" in second.current_plan:
            score += 2
        if "cooperate" in {first.social_stance, second.social_stance}:
            score += 1
        if "mediate" in {first.social_stance, second.social_stance}:
            score += 1
        if first_desire == second_desire:
            score += 2
        if {first_desire, second_desire} in [{"bond", "care"}, {"clarity", "validation"}, {"money", "opportunity"}]:
            score += 1
        score += min(first.credit_score, second.credit_score) // 25
        if first.credit_score <= 35 or second.credit_score <= 35:
            score -= 4
        return score

    def _conflict_score(self, first: Agent, second: Agent) -> int:
        score = 0
        first_desire, _ = dominant_desire_for_agent(self.state, first)
        second_desire, _ = dominant_desire_for_agent(self.state, second)
        if second.id in first.rivals or first.id in second.rivals:
            score += 3
        relation = (first.relations.get(second.id, 0) + second.relations.get(first.id, 0)) // 2
        if relation <= 10:
            score += 2
        if first.desired_resource == second.desired_resource:
            score += 3
        if {"compete", "defensive"} & {first.social_stance, second.social_stance}:
            score += 1
        if first.state.stress + second.state.stress >= 105:
            score += 1
        if self._desires_collide(first_desire, second_desire):
            score += 3
        if first.credit_score <= 35 or second.credit_score <= 35:
            score += 1
        return score

    def _run_cooperation_event(self, first: Agent, second: Agent) -> None:
        location = first.current_location if self.random.random() < 0.6 else second.current_location
        topic = self._strategy_topic(first, second, cooperative=True)
        first_desire = desire_label_for_agent(self.state, first)
        second_desire = desire_label_for_agent(self.state, second)
        summary = f"{first.name} 主动拉上 {second.name}，想一起围绕“{topic}”推进 {RESOURCE_LABELS.get(first.desired_resource, first.desired_resource)}。"
        title = f"{first.name} 和 {second.name} 形成临时联盟"
        first.current_bubble = f"{second.name}，这轮一起上。"
        second.current_bubble = "行，我接着你往下做。"
        self._remember(first, f"你决定和 {second.name} 联手推进“{topic}”。", 3, long_term=True)
        self._remember(second, f"{first.name} 主动找你合作，想一起追“{topic}”。", 3, long_term=True)
        self._remember(first, f"这次联盟背后，你更在意的是“{first_desire}”。", 2)
        self._remember(second, f"这次联盟背后，你更在意的是“{second_desire}”。", 2)
        self._adjust_relation(first, second, 5, f"围绕“{topic}”站到了一边。")
        self._shift_agent_state(first, mood=3, stress=-2, focus=2, curiosity=2, geo_reasoning_skill=1 if self._is_geoai_topic(topic) else 0)
        self._shift_agent_state(second, mood=3, stress=-2, focus=2, curiosity=2, geo_reasoning_skill=1 if self._is_geoai_topic(topic) else 0)
        first.current_activity = f"正和 {second.name} 联手推进“{topic}”。"
        second.current_activity = f"正和 {first.name} 一起把“{topic}”往前顶。"
        first.status_summary = self._build_status_summary(first, first.relations.get(second.id, 0), topic, counterpart=second.name)
        second.status_summary = self._build_status_summary(second, second.relations.get(first.id, 0), topic, counterpart=first.name)
        first.last_interaction = f"刚和 {second.name} 约好一起推进“{topic}”。"
        second.last_interaction = f"刚接下 {first.name} 的合作邀请，要一起追“{topic}”。"
        self.state.lab.collective_reasoning = min(100, self.state.lab.collective_reasoning + 2)
        self.state.lab.research_progress = min(100, self.state.lab.research_progress + 2)
        self._upsert_story_beat("alliance", title, summary, [first.id, second.id], location)
        self._emit_strategy_event(title, summary, location)
        self._log("strategy_alliance", participants=[first.id, second.id], topic=topic, location=location)

    def _run_conflict_event(self, first: Agent, second: Agent) -> None:
        if "mediate" in {first.social_stance, second.social_stance}:
            mediator = first if first.social_stance == "mediate" else second
            other = second if mediator is first else first
            topic = self._strategy_topic(mediator, other, cooperative=False)
            title = f"{mediator.name} 出面压住一场争执"
            summary = f"{other.name} 的节奏已经有点冲，{mediator.name} 主动站出来，把“{topic}”从情绪边缘拉回可谈状态。"
            mediator.current_bubble = "先别顶着冲。"
            other.current_bubble = "行，我先把话说清楚。"
            self._shift_agent_state(mediator, mood=2, stress=-1, focus=1)
            self._shift_agent_state(other, mood=1, stress=-2, focus=1)
            mediator.current_activity = f"正在调停围绕“{topic}”的拉扯。"
            other.current_activity = f"被 {mediator.name} 拉住后，重新整理“{topic}”。"
            mediator.last_interaction = f"刚把 {other.name} 从一场快升级的争执里拉了回来。"
            other.last_interaction = f"刚被 {mediator.name} 按住节奏，没让争执失控。"
            self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + 2)
            self._upsert_story_beat("mediation", title, summary, [mediator.id, other.id], mediator.current_location)
            self._emit_strategy_event(title, summary, mediator.current_location)
            self._log("strategy_mediation", participants=[mediator.id, other.id], topic=topic, location=mediator.current_location)
            return
        topic = self._strategy_topic(first, second, cooperative=False)
        first_desire = desire_label_for_agent(self.state, first)
        second_desire = desire_label_for_agent(self.state, second)
        conflict_resource = RESOURCE_LABELS.get(first.desired_resource, first.desired_resource)
        title = f"{first.name} 和 {second.name} 为 {conflict_resource} 顶上了"
        summary = f"{first.name} 和 {second.name} 都想主导“{topic}”，在 {conflict_resource} 的使用上谁也不肯先让。一个更想守住“{first_desire}”，另一个更想要“{second_desire}”。"
        first.current_bubble = "这轮不能再让了。"
        second.current_bubble = "你先别抢我的节奏。"
        self._adjust_relation(first, second, -5, f"为了 {conflict_resource} 的主导权围绕“{topic}”起了正面冲突。")
        self._shift_agent_state(first, mood=-3, stress=3, focus=2, energy=-1)
        self._shift_agent_state(second, mood=-3, stress=3, focus=2, energy=-1)
        first.current_activity = f"正在和 {second.name} 为“{topic}”争主导。"
        second.current_activity = f"正和 {first.name} 围绕“{topic}”僵持不下。"
        first.status_summary = self._build_status_summary(first, first.relations.get(second.id, 0), topic, counterpart=second.name)
        second.status_summary = self._build_status_summary(second, second.relations.get(first.id, 0), topic, counterpart=first.name)
        first.last_interaction = f"刚因为“{topic}”和 {second.name} 起了冲突。"
        second.last_interaction = f"刚在“{topic}”上和 {first.name} 顶了起来。"
        self.state.lab.team_atmosphere = max(0, self.state.lab.team_atmosphere - 2)
        self.state.lab.research_progress = max(0, self.state.lab.research_progress - 1)
        self._upsert_story_beat("conflict", title, summary, [first.id, second.id], first.current_location)
        self._emit_strategy_event(title, summary, first.current_location)
        self._log("strategy_conflict", participants=[first.id, second.id], topic=topic, location=first.current_location)

    def _desires_collide(self, first_desire: str, second_desire: str) -> bool:
        colliding = {
            frozenset({"money", "care"}),
            frozenset({"money", "bond"}),
            frozenset({"rest", "opportunity"}),
            frozenset({"rest", "validation"}),
            frozenset({"control", "bond"}),
            frozenset({"control", "care"}),
            frozenset({"clarity", "opportunity"}),
            frozenset({"validation", "clarity"}),
        }
        return frozenset({first_desire, second_desire}) in colliding

    def _desire_topic_between(self, first: Agent, second: Agent, first_desire: str, second_desire: str) -> str:
        if first_desire == second_desire:
            shared = {
                "money": "最近谁手头更紧",
                "rest": "今晚到底要不要回屋",
                "bond": "今天谁最需要被接住",
                "care": "谁现在快撑不住了",
                "clarity": "这件事到底怎么讲清楚",
                "validation": "这条想法到底值不值",
                "opportunity": "眼前这波机会要不要追",
                "control": "这轮谁该先把节奏收住",
            }
            return shared.get(first_desire, "这会儿最在意的事")
        if self._desires_collide(first_desire, second_desire):
            return f"{DESIRE_LABELS.get(first_desire, first_desire)}和{DESIRE_LABELS.get(second_desire, second_desire)}之间的拉扯"
        return self._pick_social_topic(first, second)

    def _strategy_topic(self, first: Agent, second: Agent, cooperative: bool) -> str:
        if cooperative and self._is_geoai_topic(f"{first.current_plan} {second.current_plan}"):
            return "GeoAI 主线推进"
        if first.desired_resource == second.desired_resource:
            return f"{RESOURCE_LABELS.get(first.desired_resource, first.desired_resource)}分配"
        return "今天的优先级安排" if not cooperative else "下一轮共同推进"

    def _upsert_story_beat(self, kind: str, title: str, summary: str, participants: list[str], location: str) -> None:
        pair = set(participants)
        existing = None
        for beat in self.state.story_beats:
            if set(beat.participants) == pair and beat.kind == kind:
                existing = beat
                break
        if existing:
            existing.title = title
            existing.summary = summary
            existing.stage = min(5, existing.stage + 1)
            existing.momentum = min(5, existing.momentum + 1)
            existing.location = location
        else:
            self.state.story_beats.insert(
                0,
                StoryBeat(
                    id=f"beat-{uuid4().hex[:8]}",
                    title=title,
                    summary=summary,
                    kind=kind,
                    participants=participants,
                    stage=1,
                    momentum=3,
                    location=location,
                ),
            )
        self.state.story_beats = self.state.story_beats[:8]

    def _age_story_beats(self) -> None:
        kept: list[StoryBeat] = []
        for beat in self.state.story_beats:
            beat.momentum -= 1
            if beat.momentum > 0:
                kept.append(beat)
        self.state.story_beats = kept[:8]

    def _emit_strategy_event(self, title: str, summary: str, location: str) -> None:
        self.state.events.insert(
            0,
            build_internal_event(
                title=title,
                summary=f"{summary} 地点在{ROOM_LABELS.get(location, location)}。",
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]

    def _agent_name(self, agent_id: str) -> str:
        try:
            return self._find_agent(agent_id).name
        except KeyError:
            return agent_id

    def _advance_world(self) -> None:
        previous_day = self.state.day
        day, slot = advance_time(self.state.day, self.state.time_slot)
        self.state.day = day
        self.state.time_slot = slot
        self.state.weather = self._roll_weather()
        self._sync_market_clock()
        self.trigger_scheduled_news()
        if slot == "morning":
            self._evaluate_business_lifecycle()
            self._sync_business_locations()
            self._record_daily_economy_point(
                previous_day,
                tourism_private_income=self.state.tourism.daily_private_income,
                tourism_government_income=self.state.tourism.daily_government_income,
                tourism_public_income=self.state.tourism.daily_public_operator_income,
            )
            self._record_daily_bank_point(previous_day)
            self._record_daily_casino_point(previous_day)
            self._record_daily_business_point(previous_day)
            self._apply_daily_market_and_consumption_feedback(previous_day)
            self._refresh_tourism_cycle()
            self.state.tourism.daily_revenue = 0
            self.state.tourism.daily_private_income = 0
            self.state.tourism.daily_government_income = 0
            self.state.tourism.daily_public_operator_income = 0
            self.state.tourism.daily_arrivals = 0
            self.state.tourism.daily_departures = 0
            self.state.tourism.daily_messages_count = 0
            self.state.tourism.latest_signal = ""
            self.state.casino.daily_visits = 0
            self.state.casino.daily_wagers = 0
            self.state.casino.daily_payouts = 0
            self.state.casino.daily_tax = 0
            self.state.casino.daily_big_wins = 0
            self.state.casino.current_heat = max(12, int(self.state.casino.current_heat * 0.7))
            self._reset_daily_business_metrics()

    def _apply_daily_market_and_consumption_feedback(self, day: int) -> None:
        slot = self.state.time_slot
        point = next((item for item in reversed(self.state.daily_economy_history or []) if item.day == day), None)
        if point is None:
            return
        total_consumption = point.resident_consumption + point.tourist_consumption
        if total_consumption <= 0:
            return
        consumption_score = min(5, total_consumption // 220)
        if point.tourist_consumption >= 80:
            self.state.market.sentiment = self._bounded(self.state.market.sentiment + 1 + consumption_score // 2)
        if total_consumption >= 180:
            self.state.player.consumption_desire = self._bounded(self.state.player.consumption_desire + 1 + consumption_score // 2)
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + 1)
            for agent in self.state.agents:
                agent.consumption_desire = self._bounded(agent.consumption_desire + 1 + consumption_score // 2)
                if point.tourist_consumption >= 60:
                    agent.life_satisfaction = self._bounded(agent.life_satisfaction + 1)
            if not self.state.casino.last_note:
                self.state.casino.last_note = "昨晚牌桌已经收声，今晚看谁还会摸进后巷。"
            self.state.market.sentiment = int(self.state.market.sentiment * 0.6)
            self._apply_opening_gap()
            for quote in self.state.market.stocks:
                quote.open_price = quote.price
                quote.day_change_pct = 0.0
                quote.change_pct = 0.0
                quote.last_reason = "新一天开盘"
            self.state.market.index_history = []
            self._refresh_market_regime(force_roll=True)
            self._refresh_sector_rotation(force_roll=True)
            self._update_index_history(append=True)
            self._update_daily_index_history()
            self._advance_gray_cases(daily_roll=True)
            self.lifestyle_engine.run_new_day()
            self._tick_relation_cooldowns()
            self._apply_relation_rebound()
            self._apply_property_cycle()
            self._settle_bank_deposit_interest()
            self._run_fiscal_distribution_cycle()
            self._advance_government_projects()
            self._run_government_agent()
        for agent in self.state.agents:
            if agent.is_resting:
                if slot == "morning" and day >= (agent.rest_until_day or day):
                    self._wake_agent_for_day(agent)
                else:
                    self._keep_agent_resting(agent, recovery_full=True)
                continue
            if slot == "night":
                if self._night_returns_home(agent):
                    self._send_agent_home(agent, "夜里差不多该回小屋休息了。")
                    agent.state.energy = min(100, agent.state.energy + 10)
                    agent.state.stress = max(0, agent.state.stress - 6)
                else:
                    x, y = HUBS[agent.id][slot]
                    agent.position = Point(x=x, y=y)
                    agent.current_location = self._room_for(x, y)
                    agent.state.energy = max(0, agent.state.energy - 12)
                    agent.state.focus = max(30, min(95, agent.state.focus - 3))
                    agent.state.stress = min(100, agent.state.stress + 4)
                    agent.current_activity = f"夜里还没回{agent.home_label or '小屋'}，继续在外面晃。"
                    agent.current_bubble = "今晚我先不回去。"
                    agent.status_summary = f"夜里还在外面，体力掉得更快；现在更需要休息，不太想被打断。"
                    agent.last_interaction = f"今晚还没回{agent.home_label or '小屋'}，想再拖一会儿。"
                    if agent.state.energy <= FORCED_REST_THRESHOLD:
                        self._send_agent_home(agent, "体力已经见底，得先回去睡一觉。", forced=True)
                continue
            x, y = HUBS[agent.id][slot]
            agent.position = Point(x=x, y=y)
            agent.current_location = self._room_for(x, y)
            energy_cost = 8 if slot in {"afternoon", "evening"} else 5
            agent.state.energy = max(0, agent.state.energy - energy_cost)
            agent.state.focus = max(30, min(95, agent.state.focus + (4 if agent.persona == "engineering" and slot == "morning" else -2)))
            agent.state.stress = min(100, agent.state.stress + 1)
            if agent.state.energy <= FORCED_REST_THRESHOLD:
                self._send_agent_home(agent, "体力已经见底，得先回去睡一觉。", forced=True)
        self._settle_due_loans()
        self._settle_due_bank_loans()
        self._refresh_presence()
        if slot == "morning" and day > 1:
            self.state.player.daily_actions = []
            self.social_engine.run_new_day_briefing(day - 1)
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"第 {day} 天开始",
                    summary="热咖啡、更新后的基准表，以及又一次磨练 GeoAI 推理的机会。",
                    slot=slot,
                    category="geoai",
                ),
            )
            self.state.events = self.state.events[:8]
        self._refresh_memory_streams()
        self._refresh_tasks()

    def _find_agent(self, agent_id: str) -> Agent:
        for agent in self.state.agents:
            if agent.id == agent_id:
                return agent
        raise KeyError(f"未知角色：{agent_id}")

    def _find_tourist(self, tourist_id: str) -> TouristAgent:
        for tourist in self.state.tourists:
            if tourist.id == tourist_id:
                return tourist
        raise KeyError(f"未知游客：{tourist_id}")

    def _night_returns_home(self, agent: Agent) -> bool:
        preference = 0.7
        if agent.persona in {"empathetic", "engineering"}:
            preference += 0.1
        if agent.persona in {"creative", "opportunist"}:
            preference -= 0.08
        if agent.state.energy <= 36:
            preference += 0.12
        if agent.state.stress >= 60:
            preference += 0.08
        return self.random.random() < max(0.15, min(0.95, preference))

    def _at_home(self, agent: Agent) -> bool:
        return agent.home_position is not None and agent.position == agent.home_position

    def _keep_agent_resting(self, agent: Agent, recovery_full: bool = False) -> None:
        if agent.home_position is not None:
            agent.position = agent.home_position.model_copy()
            agent.current_location = self._room_for(agent.position.x, agent.position.y)
        if recovery_full:
            agent.state.energy = 100
            agent.state.stress = max(0, agent.state.stress - 6)
            agent.state.mood = min(100, agent.state.mood + 3)
        agent.current_activity = f"正在{agent.home_label or '小屋'}里休息。"
        agent.current_bubble = "先回屋歇一会。"
        agent.status_summary = f"这会儿不在外面活动，正在{agent.home_label or '小屋'}休息；只要完整待过一个时段，体力就会回满。"
        agent.last_interaction = f"已经回到{agent.home_label or '小屋'}休息，等明早再出来。"
        agent.current_plan = f"先把体力补回来，明早再出门。"
        agent.social_stance = "observe"
        agent.immediate_intent = "想先休息，不太想接长对话。"

    def _send_agent_home(self, agent: Agent, reason: str, forced: bool = False) -> None:
        if agent.is_resting:
            self._keep_agent_resting(agent)
            return
        agent.is_resting = True
        agent.rest_until_day = self.state.day + 1
        if forced:
            agent.state.mood = max(0, agent.state.mood - 2)
            agent.state.stress = min(100, agent.state.stress + 2)
        self._keep_agent_resting(agent)
        self._remember(agent, reason, 3, long_term=forced)
        if forced:
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{agent.name} 体力见底回屋休息",
                    summary=f"{agent.name} 今天已经撑不住了，先回到{agent.home_label or '小屋'}睡一觉，准备明早再出来。",
                    slot=self.state.time_slot,
                    category="general",
                ),
            )
            self.state.events = self.state.events[:8]

    def _wake_agent_for_day(self, agent: Agent) -> None:
        agent.is_resting = False
        agent.rest_until_day = None
        x, y = HUBS[agent.id]["morning"]
        agent.position = Point(x=x, y=y)
        agent.current_location = self._room_for(x, y)
        agent.state.energy = 100
        agent.state.stress = max(0, agent.state.stress - 8)
        agent.state.mood = min(100, agent.state.mood + 3)
        agent.current_activity = f"一早从{agent.home_label or '小屋'}出来，准备开始今天的活动。"
        agent.current_bubble = "先出来走走。"
        agent.status_summary = f"昨晚在{agent.home_label or '小屋'}里补过觉了，现在体力回来了，准备重新加入大家。"
        agent.last_interaction = f"今早从{agent.home_label or '小屋'}出来了，状态比昨晚稳。"
        agent.immediate_intent = "刚出门，想先看看今天谁状态最值得接近。"

    def _apply_event_to_agent(self, agent: Agent, event: LabEvent) -> None:
        category_bias = {
            "rational": {"geoai": 5, "tech": 3},
            "creative": {"gaming": 3, "geoai": 4, "general": 2},
            "engineering": {"tech": 4, "geoai": 3},
            "empathetic": {"general": 3, "gaming": 2},
            "opportunist": {"market": 6, "general": 2, "tech": 2},
        }
        curiosity_gain = category_bias.get(agent.persona, {}).get(event.category, 1)
        agent.state.curiosity = min(100, agent.state.curiosity + curiosity_gain)
        agent.state.mood = min(100, agent.state.mood + max(1, curiosity_gain - 1))
        self._remember(agent, f"刚收到外部事件：“{event.title}”。", importance=2)
        if event.category in {"geoai", "tech", "market"}:
            self._remember(agent, f"“{event.title}”这件事，接下来多半会影响小镇里的看法。", importance=3, long_term=True)
        event_bubble = {
            "geoai": "这条信息值得继续推演。",
            "tech": "也许要调整实验方案。",
            "market": "这条外部波动会影响大家情绪。",
            "gaming": "休息区今晚肯定会聊这个。",
            "general": "这消息能带来一点新鲜空气。",
        }
        agent.current_bubble = event_bubble.get(event.category, "这条消息值得留意。")

    def _commit_dialogue(self, agent: Agent, dialogue: DialogueOutcome, reason: str, mode: str = "manual") -> DialogueOutcome:
        self.state.latest_dialogue = dialogue
        self.state.ambient_dialogues.insert(0, dialogue)
        self.state.ambient_dialogues = self.state.ambient_dialogues[:6]
        relation_delta, changes = self._apply_player_dialogue_impact(agent, dialogue, intensity=self._observer_dialogue_intensity(agent) if mode == "observer" else 1.0)
        relation_delta = self._adjust_player_relation(agent, relation_delta, reason, observer=mode == "observer")
        money_effects = self._resolve_player_money_exchange(agent, dialogue, relation_delta)
        self._adjust_player_satisfaction(2 if relation_delta >= 0 else -1)
        agent.life_satisfaction = self._bounded(agent.life_satisfaction + (2 if relation_delta >= 0 else 0))
        agent.current_bubble = dialogue.bubble_text
        self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + (1 if mode == "observer" else 2))
        if mode != "observer":
            self._advance_geoai_progress(3, reason=dialogue.topic or "玩家对话")
            self.state.lab.knowledge_base = min(100, self.state.lab.knowledge_base + 2)
        topic = dialogue.topic or "今天的聊天"
        self._remember(agent, f"你在{self._slot_name(self.state.time_slot)}和玩家聊了“{topic}”。", importance=2)
        if dialogue.player_text:
            self._remember(agent, f"玩家刚刚说：“{dialogue.player_text}”", importance=2)
        self._remember(agent, f"你刚刚回复玩家：“{dialogue.line[:72]}”", importance=2)
        if mode != "observer" and agent.persona in {"rational", "creative"}:
            self._remember(agent, f"“{topic}”这件事还值得过后再想一想。", importance=3, long_term=True)
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"{agent.name} 和你聊了起来",
                summary=dialogue.line,
                slot=self.state.time_slot,
                category="geoai" if agent.persona in {"rational", "creative"} else "general",
            ),
        )
        self.state.events = self.state.events[:8]
        apply_task_progress(self.state.tasks, "dialogue")
        intervention_cost = 0
        if mode != "observer":
            manual_pressure = sum(1 for action in self.state.player.daily_actions if action.startswith("intervene:dialogue:"))
            if relation_delta > 0 and (agent.relations.get("player", 0) >= 42 or manual_pressure >= 2):
                intervention_cost = -self._apply_player_intervention_cost("dialogue", amount=1)
        dialogue.effects = self._player_dialogue_effects(agent, relation_delta, changes) + money_effects
        if intervention_cost > 0:
            dialogue.effects.append(f"玩家信誉 -{intervention_cost}")
        player_desire = self._player_desire_label(dialogue.player_text)
        agent_desire = desire_label_for_agent(self.state, agent, dialogue.player_text)
        financial_note = "；".join(money_effects)
        key_point = self._player_dialogue_key_point(dialogue, agent.name, player_desire, agent_desire, financial_note, relation_delta)
        self._append_dialogue_record(
            DialogueRecord(
                id=f"dialogue-{uuid4().hex[:8]}",
                kind="player_dialogue",
                day=self.state.day,
                time_slot=self.state.time_slot,
                participants=["player", agent.id],
                participant_names=["你", agent.name],
                topic=dialogue.topic or "临时闲聊",
                summary=f"{'观察模式下你先随口抛出' if mode == 'observer' else '你先抛出'}“{dialogue.player_text or '一段试探'}”，{agent.name} 的回应是：“{dialogue.line}”",
                key_point=key_point,
                transcript=[f"你：{dialogue.player_text}", f"{agent.name}：{dialogue.line}"] if dialogue.player_text else [f"{agent.name}：{dialogue.line}"],
                desire_labels={"你": player_desire, agent.name: agent_desire},
                mood="warm" if relation_delta >= 3 else "tense" if relation_delta <= -2 else "neutral",
                financial_note=financial_note,
                gray_trade=False,
            )
        )
        self._log(
            "player_dialogue",
            agent={"id": agent.id, "name": agent.name, "x": agent.position.x, "y": agent.position.y},
            topic=dialogue.topic,
            reason=reason,
            mode=mode,
            dialogue={
                "player_text": dialogue.player_text,
                "agent_reply": dialogue.line,
                "bubble_text": dialogue.bubble_text,
                "effects": dialogue.effects,
            },
            money={"player_cash": self.state.player.cash, "agent_cash": agent.cash},
        )
        return dialogue

    def _append_dialogue_record(self, record: DialogueRecord) -> None:
        if self.state.dialogue_history is None:
            self.state.dialogue_history = []
        self.state.dialogue_history.insert(0, record)
        self.state.dialogue_history = self.state.dialogue_history[:1000]

    def _append_finance_record(
        self,
        *,
        actor_id: str,
        actor_name: str,
        category: str,
        action: str,
        summary: str,
        amount: int = 0,
        asset_name: str = "",
        counterparty: str = "",
        interest_rate: float | None = None,
        financed: bool = False,
    ) -> None:
        if self.state.finance_history is None:
            self.state.finance_history = []
        self.state.finance_history.insert(
            0,
            FinanceRecord(
                id=f"finance-{uuid4().hex[:8]}",
                day=self.state.day,
                time_slot=self.state.time_slot,
                actor_id=actor_id,
                actor_name=actor_name,
                category=category,
                action=action,
                summary=summary,
                amount=amount,
                asset_name=asset_name,
                counterparty=counterparty,
                interest_rate=interest_rate,
                financed=financed,
            ),
        )
        self.state.finance_history = self.state.finance_history[:200]

    def _disburse_welfare(
        self,
        *,
        recipient_type: str,
        recipient_id: str,
        recipient_name: str,
        current_cash: int,
        total_assets: int = 0,
        bankruptcy: bool = False,
        agent: Agent | None = None,
    ) -> int:
        government = self.state.government
        if government.reserve_balance <= 0:
            return 0
        threshold = government.welfare_low_cash_threshold
        asset_ceiling = threshold * (2 if bankruptcy else 4)
        if total_assets > asset_ceiling:
            return 0
        if current_cash > threshold and not bankruptcy:
            return 0
        support_floor = government.welfare_bankruptcy_support if bankruptcy else government.welfare_base_support
        target_cash = threshold + (8 if bankruptcy else 0)
        payout = max(support_floor, max(0, target_cash - current_cash))
        payout = max(0, min(government.reserve_balance, payout))
        if payout <= 0:
            return 0
        government.reserve_balance -= payout
        government.total_welfare_paid += payout
        government.expenditures["welfare"] = government.expenditures.get("welfare", 0) + payout
        if recipient_type == "player":
            self.state.player.cash += payout
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + (4 if bankruptcy else 2))
            self.state.player.last_trade_summary = f"小镇财政发来 ${payout} 的{'破产' if bankruptcy else '低收入'}保障金，先把现金线托住。"
        elif agent is not None:
            agent.cash += payout
            self._adjust_agent_satisfaction(agent, 4 if bankruptcy else 2)
            agent.state.stress = self._bounded(agent.state.stress - (8 if bankruptcy else 4))
            agent.last_trade_summary = f"小镇财政发来 ${payout} 的{'破产' if bankruptcy else '低收入'}保障金，让你先稳一口气。"
        self._append_finance_record(
            actor_id=recipient_id,
            actor_name=recipient_name,
            category="welfare",
            action="support",
            summary=f"{recipient_name} 领取了 ${payout} 的{'破产' if bankruptcy else '低收入'}财政保障金。",
            amount=payout,
            asset_name="财政保障",
            counterparty=government.name,
        )
        return payout

    def _issue_consumption_coupon(self, *, recipient_type: str, recipient_id: str, recipient_name: str, amount: int, note: str) -> int:
        if amount <= 0 or self.state.government.reserve_balance <= 0:
            return 0
        issued = min(max(0, amount), self.state.government.reserve_balance)
        self.state.government.reserve_balance -= issued
        if recipient_type == "player":
            self.state.player.consumption_coupon_balance += issued
            self.state.player.consumption_desire = self._bounded(self.state.player.consumption_desire + max(1, issued // 6))
        else:
            agent = self._find_agent(recipient_id)
            agent.consumption_coupon_balance += issued
            agent.consumption_desire = self._bounded(agent.consumption_desire + max(1, issued // 6))
            agent.last_trade_summary = f"财政发来 ${issued} 的消费券，理由是：{note}"
        self.state.government.total_coupons_issued += issued
        self.state.government.expenditures["coupon"] = self.state.government.expenditures.get("coupon", 0) + issued
        self._append_finance_record(
            actor_id=recipient_id,
            actor_name=recipient_name,
            category="government",
            action="coupon",
            summary=f"{recipient_name} 领到 ${issued} 的消费券。{note}",
            amount=issued,
            asset_name="消费券",
            counterparty=self.state.government.name,
        )
        return issued

    def _recent_finance_records(self, days: int) -> list[FinanceRecord]:
        floor = max(1, self.state.day - days + 1)
        return [record for record in self.state.finance_history if record.day >= floor]

    def _recent_nonfine_consumption(self, actor_id: str, actor_name: str, days: int) -> int:
        total = 0
        for record in self._recent_finance_records(days):
            if record.actor_id != actor_id or record.actor_name != actor_name:
                continue
            if record.category != "consume" or record.action not in {"buy", "expense"}:
                continue
            total += abs(int(record.amount or 0))
        return total

    def _government_investment_targets(self) -> list[PropertyAsset]:
        return [
            asset
            for asset in self.state.properties
            if asset.owner_type in {"market", "player", "agent"}
            and asset.status == "listed"
            and asset.property_type in {"rental_house", "shop", "greenhouse"}
        ]

    def _government_owned_assets(self) -> list[PropertyAsset]:
        return [
            asset
            for asset in self.state.properties
            if asset.owner_type == "government" and asset.status == "owned"
        ]

    def _government_facility_candidates(self, property_type: str, facility_kind: str = "") -> list[tuple[int, int]]:
        facility_map: dict[str, list[tuple[int, int]]] = {
            "public_housing": [
                (26, 12), (29, 12), (41, 12),
            ],
            "night_market_stall": [
                (9, 14), (12, 14), (15, 14), (18, 14), (21, 14),
                (8, 17), (11, 17), (14, 17), (17, 17),
            ],
            "visitor_service_station": [
                (23, 6), (27, 6), (31, 6), (35, 6),
                (23, 9), (27, 9), (31, 9),
            ],
        }
        if facility_kind and facility_kind in facility_map:
            return facility_map[facility_kind]
        type_map = {
            "shop": facility_map["night_market_stall"],
            "rental_house": facility_map["public_housing"],
            "greenhouse": facility_map["visitor_service_station"],
        }
        return type_map.get(property_type, [(10, 10)])

    def _government_facility_anchor(self, property_type: str, facility_kind: str = "", preferred_slot: str = "") -> tuple[Point, str]:
        candidates = self._government_facility_candidates(property_type, facility_kind)
        probe = PropertyAsset(
            id="government-anchor-probe",
            owner_type="government",
            owner_id="government",
            property_type=property_type,
            name="政府设施",
            position=Point(x=1, y=1),
            purchase_price=0,
            estimated_value=0,
            facility_kind=facility_kind,
        )
        occupied = [
            (asset.position.x, asset.position.y, asset.width, asset.height, asset.id)
            for asset in self.state.properties
            if asset.status in {"owned", "listed", "construction", "demolishing"}
        ]

        if preferred_slot:
            try:
                _, raw_index = preferred_slot.rsplit(":", 1)
                preferred_index = int(raw_index)
            except ValueError:
                preferred_index = -1
            if 0 <= preferred_index < len(candidates):
                x, y = candidates[preferred_index]
                if self._can_place_property_anchor(probe, x, y, occupied):
                    return Point(x=x, y=y), preferred_slot

        for idx, (x, y) in enumerate(candidates):
            if self._can_place_property_anchor(probe, x, y, occupied):
                return Point(x=x, y=y), f"{facility_kind or property_type}:{idx}"
        for idx, (x, y) in enumerate(candidates):
            if not any(self._rectangles_overlap(x, y, probe.width, probe.height, ox, oy, ow, oh) for ox, oy, ow, oh, _ in occupied):
                return Point(x=x, y=y), f"{facility_kind or property_type}:{idx}"
        fallback = candidates[0] if candidates else (10, 10)
        return Point(x=fallback[0], y=fallback[1]), f"{facility_kind or property_type}:0"

    @staticmethod
    def _rectangles_overlap(ax: int, ay: int, aw: int, ah: int, bx: int, by: int, bw: int, bh: int) -> bool:
        return not (ax + aw - 1 < bx or bx + bw - 1 < ax or ay + ah - 1 < by or by + bh - 1 < ay)

    def _property_anchor_candidates(self, asset: PropertyAsset) -> list[tuple[int, int]]:
        if asset.id in PROPERTY_LAYOUT_ANCHORS:
            return PROPERTY_LAYOUT_ANCHORS[asset.id]
        if asset.owner_type == "government":
            return self._government_facility_candidates(asset.property_type, asset.facility_kind)
        fallback_map = {
            "home_upgrade": [(6, 22), (9, 2), (11, 22), (21, 2), (24, 22), (38, 2)],
            "farm_plot": [(14, 14), (18, 14)],
            "rental_house": [(39, 12), (34, 12), (24, 22)],
            "shop": [(6, 14), (11, 12), (28, 11), (35, 8), (12, 14)],
            "greenhouse": [(23, 18), (22, 18), (23, 6)],
        }
        return fallback_map.get(asset.property_type, [(asset.position.x, asset.position.y)])

    def _can_place_property_anchor(
        self,
        asset: PropertyAsset,
        x: int,
        y: int,
        occupied: list[tuple[int, int, int, int, str]],
        *,
        ignore_asset_id: str = "",
    ) -> bool:
        if x < 1 or y < 1 or x + asset.width - 1 > self.state.world_width or y + asset.height - 1 > self.state.world_height:
            return False
        for check_x in range(x, x + asset.width):
            for check_y in range(y, y + asset.height):
                if self._is_blocked(check_x, check_y):
                    return False
        for ox, oy, ow, oh, owner_id in occupied:
            if owner_id == ignore_asset_id:
                continue
            if self._rectangles_overlap(x, y, asset.width, asset.height, ox, oy, ow, oh):
                return False
        return True

    def _sync_structural_landmarks(self) -> None:
        if getattr(self.state, "tourism", None) is None:
            self.state.tourism = TourismState()
        property_map = {asset.id: asset for asset in self.state.properties}
        home_asset_map = {
            "lin": "property-lin-cottage",
            "mika": "property-mika-cottage",
            "jo": "property-jo-cottage",
            "rae": "property-rae-cottage",
            "kai": "property-kai-cottage",
        }
        for agent in self.state.agents:
            asset_id = home_asset_map.get(agent.id)
            home_asset = property_map.get(asset_id) if asset_id else None
            if home_asset is None:
                continue
            agent.home_position = Point(x=home_asset.position.x, y=min(self.state.world_height, home_asset.position.y + 1))
            agent.home_label = home_asset.name
        inn_asset = property_map.get("property-tourist-inn")
        if inn_asset is not None:
            self.state.tourism.inn_position = Point(
                x=min(self.state.world_width, inn_asset.position.x + 1),
                y=min(self.state.world_height, inn_asset.position.y + 2),
            )
        else:
            self.state.tourism.inn_position = Point(x=35, y=14)
        market_asset = property_map.get("property-tourist-market")
        if market_asset is not None:
            self.state.tourism.market_position = Point(
                x=min(self.state.world_width, market_asset.position.x + 1),
                y=min(self.state.world_height, market_asset.position.y + 2),
            )
        else:
            self.state.tourism.market_position = Point(x=7, y=16)

    def _rebalance_property_layout(self) -> None:
        fixed_ids = set(PROPERTY_LAYOUT_ANCHORS)
        occupied: list[tuple[int, int, int, int, str]] = []
        ordering = sorted(
            self.state.properties,
            key=lambda asset: (
                0 if asset.id in fixed_ids else 1 if asset.owner_type != "government" else 2,
                asset.owner_type,
                asset.id,
            ),
        )
        for asset in ordering:
            candidates = self._property_anchor_candidates(asset)
            current = (asset.position.x, asset.position.y)
            if current in candidates and self._can_place_property_anchor(asset, current[0], current[1], occupied, ignore_asset_id=asset.id):
                occupied.append((current[0], current[1], asset.width, asset.height, asset.id))
                continue
            placed = False
            for x, y in candidates:
                if self._can_place_property_anchor(asset, x, y, occupied, ignore_asset_id=asset.id):
                    asset.position = Point(x=x, y=y)
                    occupied.append((x, y, asset.width, asset.height, asset.id))
                    placed = True
                    break
            if placed:
                continue
            if self._can_place_property_anchor(asset, asset.position.x, asset.position.y, occupied, ignore_asset_id=asset.id):
                occupied.append((asset.position.x, asset.position.y, asset.width, asset.height, asset.id))
                continue
            # Last resort: preserve the asset but keep it tracked so later assets avoid exact overlap.
            occupied.append((asset.position.x, asset.position.y, asset.width, asset.height, asset.id))
        self._sync_structural_landmarks()

    def _activity_anchor_points(self, anchor_id: str) -> list[Point]:
        candidates = ACTIVITY_ANCHORS.get(anchor_id, [])
        points: list[Point] = []
        for x, y in candidates:
            anchor_point = Point(x=x, y=y)
            points.append(self._nearest_walkable(anchor_point, self._room(self._room_for(x, y))))
        return points

    def _pick_activity_anchor(
        self,
        anchor_id: str,
        *,
        actor_position: Point | None = None,
        avoid_rooms: set[str] | None = None,
    ) -> Point:
        candidates = self._activity_anchor_points(anchor_id)
        if not candidates:
            fallback = actor_position or self.state.player.position
            return fallback.model_copy()
        avoid_rooms = avoid_rooms or set()

        def score(point: Point) -> float:
            room = self._room_for(point.x, point.y)
            score_value = 0.0
            if room in avoid_rooms:
                score_value -= 1.2
            if actor_position is not None:
                score_value -= (abs(point.x - actor_position.x) + abs(point.y - actor_position.y)) * 0.02
            score_value += self.random.uniform(-0.08, 0.08)
            return score_value

        best = max(candidates, key=score)
        return best.model_copy()

    def _government_facility_position(self, property_type: str, facility_kind: str = "") -> Point:
        position, _ = self._government_facility_anchor(property_type, facility_kind)
        return position

    def _rebalance_government_facilities(self) -> None:
        occupied = {
            (asset.position.x, asset.position.y)
            for asset in self.state.properties
            if asset.owner_type != "government"
        }
        seen: set[tuple[int, int]] = set()
        kind_offsets: dict[str, int] = {}
        government_assets = sorted(
            [asset for asset in self.state.properties if asset.owner_type == "government"],
            key=lambda asset: (asset.facility_kind or asset.property_type, asset.id),
        )
        for asset in government_assets:
            candidates = self._government_facility_candidates(asset.property_type, asset.facility_kind)
            current = (asset.position.x, asset.position.y)
            if not asset.anchor_slot and current in candidates:
                asset.anchor_slot = f"{asset.facility_kind or asset.property_type}:{candidates.index(current)}"
            duplicate = current in seen or current in occupied
            # Built government assets are real property. Once they have a valid anchor and do not
            # collide, keep them fixed in place instead of participating in every later rebalance.
            if (
                asset.status == "owned"
                and asset.built
                and asset.project_stage == ""
                and asset.anchor_slot
                and not duplicate
            ):
                seen.add(current)
                continue
            if not duplicate and current in candidates:
                seen.add(current)
                continue
            if asset.anchor_slot:
                try:
                    _, raw_index = asset.anchor_slot.rsplit(":", 1)
                    idx = int(raw_index)
                except ValueError:
                    idx = -1
                if 0 <= idx < len(candidates):
                    candidate = candidates[idx]
                    if candidate not in seen and candidate not in occupied:
                        asset.position = Point(x=candidate[0], y=candidate[1])
                        seen.add(candidate)
                        continue
            start = kind_offsets.get(asset.facility_kind or asset.property_type, 0)
            placed = False
            for idx in range(start, len(candidates)):
                candidate = candidates[idx]
                if candidate in seen or candidate in occupied:
                    continue
                asset.position = Point(x=candidate[0], y=candidate[1])
                asset.anchor_slot = f"{asset.facility_kind or asset.property_type}:{idx}"
                seen.add(candidate)
                kind_offsets[asset.facility_kind or asset.property_type] = idx + 1
                placed = True
                break
            if placed:
                continue
            for idx, candidate in enumerate(candidates):
                if candidate in seen:
                    continue
                asset.position = Point(x=candidate[0], y=candidate[1])
                asset.anchor_slot = f"{asset.facility_kind or asset.property_type}:{idx}"
                seen.add(candidate)
                kind_offsets[asset.facility_kind or asset.property_type] = idx + 1
                placed = True
                break
            if not placed:
                seen.add((asset.position.x, asset.position.y))

    def _government_event_title(self, title: str) -> str:
        return f"【政府决策】{title}"

    def set_big_government_mode(self, enabled: bool) -> WorldState:
        government = self.state.government
        government.big_mode_enabled = bool(enabled)
        if enabled:
            government.current_agenda = "大政府模式已启动：同时观察财政、住房、游客、利率和房价。"
            government.last_macro_action = "进入强干预模式，政府可以主动调税、调息、建设、拆除、收购和挂牌。"
            government.last_agent_reason = "大政府模式下，政府会以更高频率直接介入市场与公共服务。"
            government.last_agent_action_day = max(0, self.state.day - 3)
        else:
            government.current_agenda = "观察税收、游客和住房压力。"
            government.last_macro_action = "回到常规政府模式，只做温和财政与设施调节。"
            government.last_agent_reason = "常规模式下，政府保持较低频率的建设和制度干预。"
        self.state.events.insert(
            0,
            build_internal_event(
                title=self._government_event_title("切换政府机制"),
                summary="大政府模式已开启，政府会更积极介入税率、利率、房价和公共设施。" if enabled else "大政府模式已关闭，政府恢复到常规温和干预节奏。",
                slot=self.state.time_slot,
                category="policy",
            ),
        )
        self.state.events = self.state.events[:8]
        self._log("government_mode_updated", enabled=enabled)
        self._refresh_government_agent_state()
        return self.state

    def update_government_capabilities(self, updates: dict[str, bool]) -> WorldState:
        government = self.state.government
        capability_labels = {
            "can_tune_taxes": "调税",
            "can_tune_rates": "调息",
            "can_manage_construction": "建设拆除",
            "can_trade_assets": "收购出售",
            "can_intervene_prices": "价格干预",
        }
        changed: list[str] = []
        for field, label in capability_labels.items():
            if field in updates:
                value = bool(updates[field])
                if getattr(government, field) != value:
                    setattr(government, field, value)
                    changed.append(label)
        if changed:
            government.last_macro_action = f"更新大政府权限：{' / '.join(changed)}。"
            self.state.events.insert(
                0,
                build_internal_event(
                    title=self._government_event_title("调整政府权限"),
                    summary=f"政府本轮重新配置了权限：{'、'.join(changed)}。",
                    slot=self.state.time_slot,
                    category="policy",
                ),
            )
            self.state.events = self.state.events[:8]
            self._log("government_capabilities_updated", changed=changed)
        self._refresh_government_agent_state()
        return self.state

    def _run_big_government_controls(self) -> None:
        government = self.state.government
        bank = self.state.bank
        tourism = self.state.tourism
        tourist_pressure = self._active_tourist_count() / max(1, tourism.active_visitor_cap)
        inflation = self.state.market.inflation_index or 100.0
        average_assets = (
            self._player_total_assets() + sum(self._agent_total_assets(agent) for agent in self.state.agents)
        ) / max(1, len(self.state.agents) + 1)
        action_notes: list[str] = []

        if government.can_tune_taxes and (tourist_pressure >= 0.85 or tourism.buyer_leads_total > 0):
            next_transfer = min(9.5, max(2.0, government.property_transfer_tax_rate_pct + 0.4))
            next_holding = min(12.0, max(3.0, government.property_holding_tax_rate_pct + 0.3))
            if abs(next_transfer - government.property_transfer_tax_rate_pct) > 0.05:
                government.property_transfer_tax_rate_pct = round(next_transfer, 1)
                action_notes.append(f"地产过户税调到 {government.property_transfer_tax_rate_pct:.1f}%")
            if abs(next_holding - government.property_holding_tax_rate_pct) > 0.05:
                government.property_holding_tax_rate_pct = round(next_holding, 1)
                action_notes.append(f"地产持有税调到 {government.property_holding_tax_rate_pct:.1f}%")

        if government.can_tune_taxes and (inflation >= 132 or average_assets > 80000):
            next_consumption = min(9.5, max(3.0, government.consumption_tax_rate_pct + 0.2))
            if abs(next_consumption - government.consumption_tax_rate_pct) > 0.05:
                government.consumption_tax_rate_pct = round(next_consumption, 1)
                action_notes.append(f"消费税调到 {government.consumption_tax_rate_pct:.1f}%")
        elif government.can_tune_taxes and government.reserve_balance < 400:
            next_consumption = max(3.0, government.consumption_tax_rate_pct - 0.2)
            if abs(next_consumption - government.consumption_tax_rate_pct) > 0.05:
                government.consumption_tax_rate_pct = round(next_consumption, 1)
                action_notes.append(f"消费税回落到 {government.consumption_tax_rate_pct:.1f}%")

        target_rate = bank.base_daily_rate_pct
        if government.can_tune_rates and tourist_pressure >= 0.9 and inflation > 125:
            target_rate += 0.25
        if government.can_tune_rates and government.reserve_balance < 260:
            target_rate -= 0.25
        target_rate = max(1.2, min(8.6, target_rate))
        if government.can_tune_rates and abs(target_rate - bank.base_daily_rate_pct) >= 0.05:
            bank.base_daily_rate_pct = round(target_rate, 2)
            bank.base_deposit_daily_rate_pct = round(max(0.18, min(1.2, bank.base_daily_rate_pct * 0.13)), 2)
            bank.deposit_daily_rate_pct = bank.base_deposit_daily_rate_pct
            action_notes.append(f"银行基准日利率调到 {bank.base_daily_rate_pct:.2f}%")

        if government.can_intervene_prices and self.state.properties:
            overpriced_assets = [
                asset for asset in self.state.properties
                if asset.listed and asset.purchase_price > int(asset.estimated_value * 1.15)
            ]
            adjusted = 0
            for asset in overpriced_assets[:2]:
                new_price = max(int(asset.estimated_value * 0.95), int(asset.purchase_price * 0.92))
                if new_price < asset.purchase_price:
                    asset.purchase_price = new_price
                    adjusted += 1
            if adjusted:
                action_notes.append(f"压低 {adjusted} 项挂牌资产价格")

        if action_notes:
            government.last_macro_action = "；".join(action_notes)
            government.last_policy_note = "大政府模式自动微调：{}".format("；".join(action_notes))

    def _refresh_government_agent_state(self) -> None:
        government = self.state.government
        assets = self._government_owned_assets()
        facility_counts = self._government_facility_counts()
        daily_revenue = sum(max(0, asset.daily_income) for asset in assets)
        daily_maintenance = sum(max(0, asset.daily_maintenance) for asset in assets)
        government.daily_asset_revenue = daily_revenue
        government.daily_asset_maintenance = daily_maintenance
        government.daily_asset_net = daily_revenue - daily_maintenance
        tourist_pressure = round(((self._active_tourist_count() / max(1, self.state.tourism.active_visitor_cap)) * 100))
        average_satisfaction = round(
            (sum(agent.life_satisfaction for agent in self.state.agents) + self.state.player.life_satisfaction)
            / max(1, len(self.state.agents) + 1)
        )
        listed_assets = sum(1 for asset in self.state.properties if asset.owner_type == "government" and asset.listed)
        signals: list[str] = [
            f"游客承压 {tourist_pressure}/100，当前 {self._active_tourist_count()} 人在场",
            f"财政储备 ${government.reserve_balance}，政府设施净流 ${government.daily_asset_net}",
            f"住房支持 {government.housing_support_level}，居民平均满意 {average_satisfaction}",
        ]
        if self.state.tourism.latest_signal:
            signals.append(self.state.tourism.latest_signal)
        if listed_assets:
            signals.append(f"当前有 {listed_assets} 项财政设施已挂牌，等待私人接手")
        if self.state.market.regime == "risk":
            signals.append("市场处于风险市，政府会更偏向稳就业和稳住房")
        if government.big_mode_enabled:
            signals.append(f"大政府模式开启：{government.last_macro_action or '会主动调税、调息和处置公共资产'}")
            capabilities = []
            if government.can_tune_taxes:
                capabilities.append("调税")
            if government.can_tune_rates:
                capabilities.append("调息")
            if government.can_manage_construction:
                capabilities.append("建设拆除")
            if government.can_trade_assets:
                capabilities.append("收购出售")
            if government.can_intervene_prices:
                capabilities.append("价格干预")
            if capabilities:
                signals.append(f"当前权限：{' / '.join(capabilities)}")
        if (
            facility_counts["public_housing"] >= self._government_facility_cap("public_housing")
            and facility_counts["night_market_stall"] > 0
            and facility_counts["visitor_service_station"] > 0
            and (
                not government.current_agenda
                or "旅馆和集市" in government.current_agenda
                or "补住房" in government.current_agenda
            )
        ):
            government.current_agenda = "控制住房密度，把财政预算优先投向夜市和游客服务。"
        fine_ratio = government.revenues.get("fine", 0) / max(1, government.total_revenue)
        tax_load = (
            government.wage_tax_rate_pct
            + government.consumption_tax_rate_pct
            + government.property_holding_tax_rate_pct * 0.5
            + government.securities_tax_rate_pct * 0.35
        )
        service_average = (
            government.public_service_level
            + government.tourism_support_level
            + government.housing_support_level
        ) / 3
        approval = 58
        approval += round((service_average - 60) / 2.2)
        approval += round((average_satisfaction - 80) / 1.8)
        approval += round(max(-4, min(8, government.daily_asset_net / 18)))
        approval += 6 if government.total_welfare_paid > 0 or government.last_targeted_support > 0 else 0
        approval += 2 if government.last_coupon_pool > 0 else 0
        approval -= round(max(0, tax_load - 19) * 0.65)
        approval -= round(max(0, government.enforcement_level - 40) / 16)
        approval -= round(fine_ratio * 14)
        if government.big_mode_enabled:
            approval -= 1
        if government.reserve_balance >= 1800:
            approval += 3
        if government.reserve_balance >= 8000:
            approval += 2
        if self.state.market.regime == "bull":
            approval += 2
        government.approval_score = self._bounded(int(approval))
        if government.approval_score >= 78:
            government.approval_note = "公共服务、游客承接和财政稳态都不错，公众支持度偏高。"
        elif government.approval_score >= 58:
            government.approval_note = "公众总体认可政府维持秩序和服务，但仍盯着税负与监管。"
        elif government.approval_score >= 38:
            government.approval_note = "公众对税负、罚款和建设方向开始分裂，支持度处于拉扯状态。"
        else:
            government.approval_note = "公众明显不满当前税负、罚款或建设方向，政府口碑处于低位。"
        government.known_signals = signals[:4]

    def _government_sale_candidate(self) -> PropertyAsset | None:
        assets = [
            asset
            for asset in self._government_owned_assets()
            if not asset.listed and asset.property_type in {"shop", "greenhouse", "rental_house"}
        ]
        if not assets:
            return None
        tourism_assets = [asset for asset in assets if asset.property_type in {"shop", "rental_house"}]
        for asset in sorted(assets, key=lambda item: ((item.daily_income - item.daily_maintenance), item.estimated_value)):
            if asset.property_type in {"shop", "rental_house"} and len(tourism_assets) <= 1:
                continue
            return asset
        return assets[0]

    def _government_facility_cap(self, facility_kind: str) -> int:
        return {
            "public_housing": 2,
            "night_market_stall": 2,
            "visitor_service_station": 2,
        }.get(facility_kind, 2)

    def _government_facility_counts(self) -> dict[str, int]:
        counts = {
            "public_housing": 0,
            "night_market_stall": 0,
            "visitor_service_station": 0,
        }
        for asset in self.state.properties:
            if asset.owner_type != "government":
                continue
            if asset.status not in {"owned", "construction", "listed"}:
                continue
            if asset.facility_kind in counts:
                counts[asset.facility_kind] += 1
        return counts

    def _government_demolish_asset(self, asset: PropertyAsset, reason: str, salvage_rate: float = 0.42) -> None:
        government = self.state.government
        asset.listed = False
        asset.built = False
        asset.status = "demolishing"
        asset.project_stage = "demolish"
        asset.project_due_day = self.state.day + 1
        government.last_agent_action_day = self.state.day
        government.last_agent_action = f"启动拆除 {asset.name}"
        government.last_agent_reason = reason
        self._append_finance_record(
            actor_id="government",
            actor_name=government.name,
            category="government",
            action="demolish_start",
            summary=f"{government.name} 决定拆除 {asset.name}，施工队已经进场。",
            amount=0,
            asset_name=asset.name,
            counterparty="公共拆改",
        )
        self.state.events.insert(
            0,
            build_internal_event(
                title=self._government_event_title("启动拆除一处低效设施"),
                summary=f"{asset.name} 进入拆除期，原因是密度过高或维护压力过重。预计次日完成。",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]

    def _advance_government_projects(self) -> None:
        government = self.state.government
        remaining: list[PropertyAsset] = []
        for asset in self.state.properties:
            if asset.owner_type != "government" or asset.project_due_day <= 0 or self.state.day < asset.project_due_day:
                remaining.append(asset)
                continue
            if asset.project_stage == "build":
                asset.status = "owned"
                asset.built = True
                asset.project_stage = ""
                asset.project_due_day = 0
                government.last_agent_action = f"{asset.name} 完工"
                government.last_agent_reason = "政府设施施工完成，开始投入正式运营。"
                self._append_finance_record(
                    actor_id="government",
                    actor_name=government.name,
                    category="government",
                    action="build_complete",
                    summary=f"{government.name} 的 {asset.name} 已完工并投入运营。",
                    amount=0,
                    asset_name=asset.name,
                    counterparty="公共建设",
                )
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=self._government_event_title("一处设施完工"),
                        summary=f"{asset.name} 已完工，开始承接游客、居民和智能体的使用。",
                        slot=self.state.time_slot,
                        category="market",
                    ),
                )
                self.state.events = self.state.events[:8]
                remaining.append(asset)
                continue
            if asset.project_stage == "demolish":
                salvage = max(6, int(round(asset.estimated_value * 0.42)))
                government.reserve_balance += salvage
                government.revenues["salvage"] = government.revenues.get("salvage", 0) + salvage
                government.government_asset_ids = [asset_id for asset_id in government.government_asset_ids if asset_id != asset.id]
                government.last_agent_action = f"{asset.name} 已拆除"
                government.last_agent_reason = "拆除工程完工，财政回收了一部分材料价值。"
                self._append_finance_record(
                    actor_id="government",
                    actor_name=government.name,
                    category="government",
                    action="demolish_complete",
                    summary=f"{government.name} 完成拆除 {asset.name}，回收约 ${salvage} 的残值。",
                    amount=salvage,
                    asset_name=asset.name,
                    counterparty="公共拆改",
                )
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=self._government_event_title("一处设施拆除完成"),
                        summary=f"{asset.name} 已拆除，财政回收约 ${salvage}。",
                        slot=self.state.time_slot,
                        category="market",
                    ),
                )
                self.state.events = self.state.events[:8]
                continue
            remaining.append(asset)
        self.state.properties = remaining
        self._rebalance_government_facilities()
        self._sync_structural_landmarks()

    def _trim_government_facility_inventory(self) -> None:
        counts = self._government_facility_counts()
        if counts["public_housing"] <= self._government_facility_cap("public_housing"):
            return
        self.state.government.current_agenda = "收缩过密公共住房，改把预算留给夜市和游客服务。"
        public_housing_assets = sorted(
            [
                asset
                for asset in self._government_owned_assets()
                if asset.facility_kind == "public_housing"
            ],
            key=lambda asset: ((asset.daily_income - asset.daily_maintenance), asset.estimated_value),
            reverse=True,
        )
        keep_count = self._government_facility_cap("public_housing")
        for asset in public_housing_assets[keep_count:]:
            self._government_demolish_asset(asset, "公共住房密度过高，先收缩库存，避免维护费继续堆高。", salvage_rate=0.36)

    def _run_government_agent(self) -> None:
        government = self.state.government
        self._refresh_government_agent_state()
        if government.big_mode_enabled:
            self._run_big_government_controls()
        cooldown_days = 7 if government.big_mode_enabled else 10
        if self.state.day - government.last_agent_action_day < cooldown_days:
            return
        assets = self._government_owned_assets()
        facility_counts = self._government_facility_counts()
        tourist_ratio = self._active_tourist_count() / max(1, self.state.tourism.active_visitor_cap)
        average_satisfaction = (
            sum(agent.life_satisfaction for agent in self.state.agents) + self.state.player.life_satisfaction
        ) / max(1, len(self.state.agents) + 1)
        listed_market_assets = self._government_investment_targets()
        maintenance_burden = government.daily_asset_maintenance
        if government.can_manage_construction and facility_counts["public_housing"] > self._government_facility_cap("public_housing"):
            excess_housing = sorted(
                [
                    asset for asset in assets
                    if asset.facility_kind == "public_housing"
                ],
                key=lambda asset: ((asset.daily_income - asset.daily_maintenance), asset.estimated_value),
            )
            if excess_housing:
                government.current_agenda = "收缩过密公共住房，降低维护成本。"
                self._government_demolish_asset(
                    excess_housing[0],
                    "公共住房数量过多，政府决定先拆除一处低效住房，避免财政继续被维护费拖累。",
                    salvage_rate=0.4,
                )
                self._refresh_government_agent_state()
                return
        if government.can_trade_assets and government.reserve_balance < 120 and assets:
            government.current_agenda = "回笼资金，准备把低效设施挂牌给私人。"
            candidate = self._government_sale_candidate()
            if candidate is not None:
                candidate.listed = True
                candidate.status = "listed"
                candidate.estimated_value = max(candidate.purchase_price, candidate.estimated_value)
                government.last_agent_action_day = self.state.day
                government.last_agent_action = f"挂牌出售 {candidate.name}"
                government.last_agent_reason = f"财政储备偏低（${government.reserve_balance}），先把低效设施推向市场。"
                self._append_finance_record(
                    actor_id="government",
                    actor_name=government.name,
                    category="government",
                    action="list",
                    summary=f"{government.name} 决定把 {candidate.name} 挂牌给私人，希望回笼财政资金。",
                    amount=0,
                    asset_name=candidate.name,
                    counterparty="地产市场",
                )
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=self._government_event_title("挂牌一处设施"),
                        summary=f"{candidate.name} 被推向市场，原因是财政储备与维护压力都偏紧。",
                        slot=self.state.time_slot,
                        category="market",
                    ),
                )
                self.state.events = self.state.events[:8]
                self._refresh_government_agent_state()
            return
        if (
            government.can_manage_construction
            and
            maintenance_burden > max(12, government.daily_asset_revenue + 8)
            and facility_counts["public_housing"] >= 2
            and tourist_ratio < 0.9
        ):
            housing_assets = sorted(
                [
                    asset for asset in assets
                    if asset.facility_kind == "public_housing"
                ],
                key=lambda asset: ((asset.daily_income - asset.daily_maintenance), asset.estimated_value),
            )
            if housing_assets:
                government.current_agenda = "降低公共住房维护负担，把资源留给更活跃的设施。"
                self._government_demolish_asset(
                    housing_assets[0],
                    f"公共住房维护费已到 ${maintenance_burden}，政府决定先拆掉一处低效公房，把预算留给夜市和服务站。",
                    salvage_rate=0.45,
                )
                self._refresh_government_agent_state()
                return
        if tourist_ratio >= 0.8 and government.reserve_balance >= 80:
            government.current_agenda = "优先补夜市和游客服务，住房只保留基础供给。"
            if facility_counts["night_market_stall"] < self._government_facility_cap("night_market_stall"):
                preferred = "shop"
                preferred_kind = "night_market_stall"
            elif self.state.tourism.daily_messages_count >= 2 and facility_counts["visitor_service_station"] < self._government_facility_cap("visitor_service_station"):
                preferred = "greenhouse"
                preferred_kind = "visitor_service_station"
            elif self.state.tourism.buyer_leads_total > 0 and tourist_ratio >= 0.95 and facility_counts["public_housing"] < self._government_facility_cap("public_housing"):
                preferred = "rental_house"
                preferred_kind = "public_housing"
            else:
                preferred = "greenhouse" if facility_counts["visitor_service_station"] < self._government_facility_cap("visitor_service_station") else "shop"
                preferred_kind = "visitor_service_station" if preferred == "greenhouse" else "night_market_stall"
        elif average_satisfaction < 78 and government.reserve_balance >= 90:
            government.current_agenda = "补生活配套，优先稳住满意度而不是继续堆住房。"
            if facility_counts["visitor_service_station"] < self._government_facility_cap("visitor_service_station"):
                preferred = "greenhouse"
                preferred_kind = "visitor_service_station"
            elif facility_counts["public_housing"] < self._government_facility_cap("public_housing"):
                preferred = "rental_house"
                preferred_kind = "public_housing"
            else:
                preferred = "shop"
                preferred_kind = "night_market_stall"
        elif government.can_trade_assets and maintenance_burden > max(8, government.daily_asset_revenue + 4) and assets:
            government.current_agenda = "压缩财政维护负担，准备逐步出让部分资产。"
            candidate = self._government_sale_candidate()
            if candidate is not None:
                candidate.listed = True
                candidate.status = "listed"
                government.last_agent_action_day = self.state.day
                government.last_agent_action = f"启动 {candidate.name} 的资产出让"
                government.last_agent_reason = f"设施维护 ${maintenance_burden} 高于日常收益 ${government.daily_asset_revenue}，先卖掉一处低效率资产。"
                self._append_finance_record(
                    actor_id="government",
                    actor_name=government.name,
                    category="government",
                    action="list",
                    summary=f"{government.name} 因维护负担过高，开始挂牌出让 {candidate.name}。",
                    amount=0,
                    asset_name=candidate.name,
                    counterparty="地产市场",
                )
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=self._government_event_title("出让财政设施"),
                        summary=f"{candidate.name} 因维护压力过高被推向市场，后续可能由私人接手。",
                        slot=self.state.time_slot,
                        category="market",
                    ),
                )
                self.state.events = self.state.events[:8]
                self._refresh_government_agent_state()
            return
        elif government.can_trade_assets and listed_market_assets and government.reserve_balance >= (110 if government.big_mode_enabled else 130) and self.state.market.regime != "risk":
            government.current_agenda = "择机买入能承接游客和住房需求的挂牌资产。"
            preferred_asset = next(
                (
                    asset for asset in listed_market_assets
                    if (
                        (asset.property_type == "shop" and facility_counts["night_market_stall"] < self._government_facility_cap("night_market_stall"))
                        or (asset.property_type == "greenhouse" and facility_counts["visitor_service_station"] < self._government_facility_cap("visitor_service_station"))
                        or (asset.property_type == "rental_house" and facility_counts["public_housing"] < self._government_facility_cap("public_housing"))
                    )
                ),
                listed_market_assets[0],
            )
            preferred = preferred_asset.property_type
            preferred_kind = ""
        else:
            government.current_agenda = "观察游客、住房和财政储备，暂时维持运营。"
            government.last_agent_reason = "当前没有必要立刻建设或出让设施。"
            self._refresh_government_agent_state()
            return

        target_asset = next(
            (
                asset
                for asset in sorted(listed_market_assets, key=lambda item: item.purchase_price)
                if asset.property_type == preferred and asset.purchase_price <= government.reserve_balance
            ),
            None,
        )
        if target_asset is not None:
            target_asset.owner_type = "government"
            target_asset.owner_id = "government"
            target_asset.status = "owned"
            target_asset.listed = False
            government.reserve_balance -= target_asset.purchase_price
            government.total_public_investment += target_asset.purchase_price
            government.expenditures["investment"] = government.expenditures.get("investment", 0) + target_asset.purchase_price
            if target_asset.id not in government.government_asset_ids:
                government.government_asset_ids.append(target_asset.id)
            government.last_agent_action_day = self.state.day
            government.last_agent_action = f"买入 {target_asset.name}"
            government.last_agent_reason = "当前挂牌资产能更快补足游客承接或住房供给，所以优先收购。"
            self._append_finance_record(
                actor_id="government",
                actor_name=government.name,
                category="government",
                action="acquire",
                summary=f"{government.name} 看中 {target_asset.name} 的公共用途，直接从市场买入。",
                amount=target_asset.purchase_price,
                asset_name=target_asset.name,
                counterparty="地产市场",
            )
            self.state.events.insert(
                0,
                build_internal_event(
                    title=self._government_event_title("收购一处设施"),
                    summary=f"{target_asset.name} 被财政收购，后续会继续作为公共设施运营。",
                    slot=self.state.time_slot,
                    category="market",
                ),
            )
            self.state.events = self.state.events[:8]
            self._refresh_government_agent_state()
            return

        if not government.can_manage_construction:
            government.last_agent_reason = "大政府模式当前关闭了建设拆除权限，所以本轮只观察不新建。"
            self._refresh_government_agent_state()
            return

        budget = min(government.reserve_balance, 150 if preferred == "rental_house" else 120)
        built_asset = self._government_build_public_asset(budget, preferred_type=preferred, preferred_kind=preferred_kind)
        if built_asset is None:
            government.last_agent_reason = "想建新设施，但当前储备不足，或者该类设施已经达到密度上限。"
            self._refresh_government_agent_state()
            return
        self.state.properties.append(built_asset)
        government.reserve_balance -= built_asset.purchase_price
        government.total_public_investment += built_asset.purchase_price
        government.expenditures["investment"] = government.expenditures.get("investment", 0) + built_asset.purchase_price
        government.government_asset_ids.append(built_asset.id)
        government.last_agent_action_day = self.state.day
        government.last_agent_action = f"启动建设 {built_asset.name}"
        government.last_agent_reason = "根据游客承压、住房压力和财政储备，决定先启动施工，再等待设施完工投入运营。"
        self._append_finance_record(
            actor_id="government",
            actor_name=government.name,
            category="government",
            action="build_start",
            summary=f"{government.name} 启动 {built_asset.name} 的建设，后续会在完工后承接游客、居民和智能体使用。",
            amount=built_asset.purchase_price,
            asset_name=built_asset.name,
            counterparty="公共建设",
        )
        self.state.events.insert(
            0,
            build_internal_event(
                title=self._government_event_title("启动建设一处设施"),
                summary=f"{built_asset.name} 已进入施工期，完工后才会正式承接游客、居民和智能体使用。",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]
        self._refresh_government_agent_state()

    def _government_build_public_asset(
        self,
        budget: int,
        preferred_type: str | None = None,
        preferred_kind: str | None = None,
    ) -> PropertyAsset | None:
        build_options = [
            {
                "id": f"property-gov-stall-{uuid4().hex[:6]}",
                "property_type": "shop",
                "facility_kind": "night_market_stall",
                "name": "夜市摊位",
                "purchase_price": 68,
                "estimated_value": 74,
                "daily_income": 13,
                "daily_maintenance": 3,
                "comfort_bonus": 2,
                "social_bonus": 6,
                "description": "由财政投资建设的夜市摊位，用来承接游客夜间消费和本地交易。",
            },
            {
                "id": f"property-gov-lodge-{uuid4().hex[:6]}",
                "property_type": "rental_house",
                "facility_kind": "public_housing",
                "name": "公共住房",
                "purchase_price": 92,
                "estimated_value": 98,
                "daily_income": 11,
                "daily_maintenance": 4,
                "comfort_bonus": 7,
                "social_bonus": 2,
                "description": "由财政投资建设的公共住房，用来缓解住房压力并承接临时居住需求。",
            },
            {
                "id": f"property-gov-service-{uuid4().hex[:6]}",
                "property_type": "greenhouse",
                "facility_kind": "visitor_service_station",
                "name": "游客服务站",
                "purchase_price": 76,
                "estimated_value": 82,
                "daily_income": 9,
                "daily_maintenance": 3,
                "comfort_bonus": 3,
                "social_bonus": 5,
                "description": "由财政投资建设的游客服务站，用来承接咨询、导流和消息扩散。",
            },
        ]
        affordable = [option for option in build_options if option["purchase_price"] <= budget]
        if preferred_type:
            preferred = [option for option in affordable if option["property_type"] == preferred_type]
            if preferred:
                affordable = preferred
        if preferred_kind:
            preferred = [option for option in affordable if option["facility_kind"] == preferred_kind]
            if preferred:
                affordable = preferred
        affordable = [
            option
            for option in affordable
            if self._government_facility_counts().get(str(option["facility_kind"]), 0) < self._government_facility_cap(str(option["facility_kind"]))
        ]
        if not affordable:
            return None
        option = affordable[-1]
        position, anchor_slot = self._government_facility_anchor(str(option["property_type"]), str(option["facility_kind"]))
        return PropertyAsset(
            id=option["id"],
            owner_type="government",
            owner_id="government",
            property_type=option["property_type"],
            name=option["name"],
            position=position,
            purchase_price=option["purchase_price"],
            estimated_value=option["estimated_value"],
            daily_income=option["daily_income"],
            daily_maintenance=option["daily_maintenance"],
            comfort_bonus=option["comfort_bonus"],
            social_bonus=option["social_bonus"],
            debt_eligible=False,
            buildable=False,
            listed=False,
            built=False,
            status="construction",
            facility_kind=option["facility_kind"],
            anchor_slot=anchor_slot,
            project_stage="build",
            project_due_day=self.state.day + 2,
            description=option["description"],
        )

    def _run_fiscal_distribution_cycle(self) -> None:
        government = self.state.government
        if self.state.day < government.next_distribution_day or self.state.day == government.last_distribution_day:
            return
        recent_records = self._recent_finance_records(government.fiscal_cycle_days)
        cycle_tax = sum(abs(int(record.amount or 0)) for record in recent_records if record.category == "tax")
        if cycle_tax <= 0 and government.reserve_balance < 40:
            government.next_distribution_day = self.state.day + government.fiscal_cycle_days
            government.last_distribution_note = "本轮税收和储备都偏低，财政周期暂缓执行。"
            return
        base_pool = max(0, int(round(cycle_tax * 0.6 + max(0, government.reserve_balance - 120) * 0.4)))
        base_pool = min(base_pool, max(0, government.reserve_balance - 40))
        if base_pool <= 0:
            government.next_distribution_day = self.state.day + government.fiscal_cycle_days
            government.last_distribution_note = "财政池不足，本轮优先保留储备。"
            return
        support_pool = int(round(base_pool * 0.35))
        coupon_pool = int(round(base_pool * 0.25))
        public_service_spend = int(round(base_pool * 0.20))
        investment_pool = int(round(base_pool * 0.15))
        reserve_retained = max(0, base_pool - support_pool - coupon_pool - public_service_spend - investment_pool)

        payouts = 0
        support_targets: list[tuple[str, str, str, float]] = []
        player_weight = max(0.0, (55 - self.state.player.cash) * 0.5 + self.state.player.monthly_burden * 0.35 + max(0, 60 - self.state.player.life_satisfaction) * 0.2)
        if player_weight > 0:
            support_targets.append(("player", self.state.player.id, self.state.player.name, player_weight))
        for agent in self.state.agents:
            weight = max(0.0, (55 - agent.cash) * 0.5 + agent.monthly_burden * 0.35 + max(0, 60 - agent.life_satisfaction) * 0.2)
            if weight > 0:
                support_targets.append(("agent", agent.id, agent.name, weight))
        weight_sum = sum(weight for *_, weight in support_targets) or 1.0
        for recipient_type, recipient_id, recipient_name, weight in support_targets:
            amount = int(round(support_pool * (weight / weight_sum)))
            if amount <= 0 or government.reserve_balance <= 0:
                continue
            payout = self._disburse_welfare(
                recipient_type=recipient_type,
                recipient_id=recipient_id,
                recipient_name=recipient_name,
                current_cash=self.state.player.cash if recipient_type == "player" else self._find_agent(recipient_id).cash,
                total_assets=self._player_total_assets() if recipient_type == "player" else self._agent_total_assets(self._find_agent(recipient_id)),
                bankruptcy=False,
                agent=None if recipient_type == "player" else self._find_agent(recipient_id),
            )
            payouts += payout

        issued_coupons = 0
        coupon_scores: list[tuple[str, str, str, float]] = []
        player_consumption = self._recent_nonfine_consumption(self.state.player.id, self.state.player.name, government.fiscal_cycle_days)
        player_score = (player_consumption ** 0.5) + max(0, 35 - self.state.player.cash) * 0.16
        if player_score > 0:
            coupon_scores.append(("player", self.state.player.id, self.state.player.name, player_score))
        for agent in self.state.agents:
            essential = self._recent_nonfine_consumption(agent.id, agent.name, government.fiscal_cycle_days)
            score = (essential ** 0.5) + max(0, 35 - agent.cash) * 0.16
            if score > 0:
                coupon_scores.append(("agent", agent.id, agent.name, score))
        coupon_sum = sum(score for *_, score in coupon_scores) or 1.0
        for recipient_type, recipient_id, recipient_name, score in coupon_scores:
            amount = int(round(coupon_pool * (score / coupon_sum)))
            if amount <= 0:
                continue
            issued_coupons += self._issue_consumption_coupon(
                recipient_type=recipient_type,
                recipient_id=recipient_id,
                recipient_name=recipient_name,
                amount=amount,
                note="用于鼓励下一轮本地消费和社交支出。",
            )

        actual_public_service = min(government.reserve_balance, public_service_spend)
        if actual_public_service > 0:
            government.reserve_balance -= actual_public_service
            government.expenditures["public_service"] = government.expenditures.get("public_service", 0) + actual_public_service
            government.public_service_level = self._bounded(government.public_service_level + max(1, actual_public_service // 18))
            government.tourism_support_level = self._bounded(government.tourism_support_level + max(1, actual_public_service // 22))
            government.housing_support_level = self._bounded(government.housing_support_level + max(1, actual_public_service // 26))
            for agent in self.state.agents:
                agent.life_satisfaction = self._bounded(agent.life_satisfaction + 1)
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + 2)

        actual_investment = 0
        invested_any = False
        for asset in sorted(self._government_investment_targets(), key=lambda item: (item.property_type != "rental_house", item.purchase_price)):
            if investment_pool <= 0 or government.reserve_balance <= 0:
                break
            if asset.purchase_price > min(investment_pool, government.reserve_balance):
                continue
            asset.owner_type = "government"
            asset.owner_id = "government"
            asset.status = "owned"
            asset.listed = False
            asset.built = True
            government.reserve_balance -= asset.purchase_price
            investment_pool -= asset.purchase_price
            actual_investment += asset.purchase_price
            government.total_public_investment += asset.purchase_price
            government.expenditures["investment"] = government.expenditures.get("investment", 0) + asset.purchase_price
            if asset.id not in government.government_asset_ids:
                government.government_asset_ids.append(asset.id)
            invested_any = True
            self._append_finance_record(
                actor_id="government",
                actor_name=government.name,
                category="government",
                action="invest",
                summary=f"{government.name} 买入了 {asset.name}，准备把它当作公共服务或稳定性资产来运营。",
                amount=asset.purchase_price,
                asset_name=asset.name,
                counterparty="地产市场",
            )
        if not invested_any and investment_pool > 0 and government.reserve_balance > 0:
            built_asset = self._government_build_public_asset(min(investment_pool, government.reserve_balance))
            if built_asset is not None:
                self.state.properties.append(built_asset)
                government.reserve_balance -= built_asset.purchase_price
                actual_investment += built_asset.purchase_price
                government.total_public_investment += built_asset.purchase_price
                government.expenditures["investment"] = government.expenditures.get("investment", 0) + built_asset.purchase_price
                government.government_asset_ids.append(built_asset.id)
                self._append_finance_record(
                    actor_id="government",
                    actor_name=government.name,
                    category="government",
                    action="invest",
                    summary=f"{government.name} 新建了 {built_asset.name}，用来承接游客、公共服务和本地交易需求。",
                    amount=built_asset.purchase_price,
                    asset_name=built_asset.name,
                    counterparty="公共建设",
                )

        government.last_distribution_day = self.state.day
        government.next_distribution_day = self.state.day + government.fiscal_cycle_days
        government.last_targeted_support = payouts
        government.last_coupon_pool = issued_coupons
        government.last_public_service_spend = actual_public_service
        government.last_investment_spend = actual_investment
        government.last_reserve_retained = reserve_retained
        government.last_cycle_tax_revenue = cycle_tax
        government.last_cycle_nonfine_consumption = sum(
            abs(int(record.amount or 0))
            for record in recent_records
            if record.category == "consume" and record.action in {"buy", "expense"}
        )
        government.last_distribution_note = (
            f"第 {self.state.day} 天完成财政结算：定向补贴 ${payouts}、消费券 ${issued_coupons}、公共服务 ${actual_public_service}、政府投资 ${actual_investment}。"
        )
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"财政完成第 {self.state.day} 天结算",
                summary=government.last_distribution_note,
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]

    def _collect_tax(
        self,
        *,
        payer_type: str,
        payer_id: str,
        payer_name: str,
        revenue_key: str,
        label: str,
        base_amount: int,
        rate_pct: float,
        minimum: int = 0,
    ) -> int:
        if base_amount <= 0 or rate_pct <= 0:
            return 0
        tax = max(minimum, int(round(base_amount * rate_pct / 100)))
        if tax <= 0:
            return 0
        if payer_type == "player":
            actual = min(tax, self.state.player.cash)
            self.state.player.cash = max(0, self.state.player.cash - actual)
        elif payer_type == "tourist":
            tourist = self._find_tourist(payer_id)
            actual = min(tax, tourist.cash)
            tourist.cash = max(0, tourist.cash - actual)
        else:
            agent = self._find_agent(payer_id)
            actual = min(tax, agent.cash)
            agent.cash = max(0, agent.cash - actual)
        self.state.government.total_revenue += actual
        self.state.government.reserve_balance += actual
        self.state.government.revenues[revenue_key] = self.state.government.revenues.get(revenue_key, 0) + actual
        self._append_finance_record(
            actor_id=payer_id,
            actor_name=payer_name,
            category="tax",
            action="tax",
            summary=f"{payer_name} 因{label}缴了 ${actual} 税费。",
            amount=-actual,
            asset_name=label,
            counterparty=self.state.government.name,
        )
        return actual

    def _apply_property_cycle(self) -> None:
        regime = self.state.market.regime or "bull"
        cycle_day = max(1, self.state.day)
        cyclical_discount = -0.05 if cycle_day % 9 == 0 else -0.02 if cycle_day % 6 == 0 else 0.0
        regime_discount = {"bull": 0.015, "sideways": -0.01, "risk": -0.035}.get(regime, -0.01)
        inflation_drag = -max(0.0, ((self.state.market.inflation_index or 100.0) - 118.0) / 550)
        for asset in self.state.properties:
            base_maintenance = {
                "home_upgrade": 3,
                "farm_plot": 4,
                "rental_house": 5,
                "shop": 4,
                "greenhouse": 6,
                "casino": 5,
            }.get(asset.property_type, max(2, asset.daily_maintenance or 3))
            owner_count = 0
            if asset.owner_type == "player":
                owner_count = len(self.state.player.owned_property_ids or [])
            elif asset.owner_type == "agent":
                owner = self._find_agent(asset.owner_id)
                owner_count = len(owner.owned_property_ids or [])
            inflation_factor = max(1.0, (self.state.market.inflation_index or 100.0) / 112)
            maintenance_factor = inflation_factor + max(0.0, (owner_count - 1) * 0.08) + (0.14 if regime == "risk" else 0.04 if regime == "sideways" else 0.0)
            asset.daily_maintenance = max(base_maintenance, int(round(base_maintenance * maintenance_factor)))
            if asset.status != "owned":
                continue
            valuation_delta = regime_discount + cyclical_discount + inflation_drag
            next_value = int(round(asset.estimated_value * (1 + valuation_delta)))
            floor = int(round(asset.purchase_price * 0.58))
            ceiling = int(round(asset.purchase_price * 1.42))
            asset.estimated_value = max(floor, min(ceiling, next_value))

    def _maybe_trigger_regulatory_audit(self) -> None:
        government = self.state.government
        effective_cooldown = max(2, government.audit_cooldown_days + max(0, round((55 - government.enforcement_level) / 12)))
        if self.state.day - (government.last_audit_day or 0) < effective_cooldown:
            return
        wealth_targets: list[tuple[float, str, str, str]] = []
        player_net = self._player_total_assets()
        wealth_targets.append((player_net, "player", self.state.player.id, self.state.player.name))
        for agent in self.state.agents:
            wealth_targets.append((self._agent_total_assets(agent), "agent", agent.id, agent.name))
        wealth, target_type, target_id, target_name = max(wealth_targets, key=lambda item: item[0])
        property_count = len(self.state.player.owned_property_ids or []) if target_type == "player" else len(self._find_agent(target_id).owned_property_ids or [])
        gray_risk = sum(1 for case in self.state.gray_cases if case.status == "active" and target_id in case.participants)
        casino_risk = sum(
            1
            for case in self.state.gray_cases
            if case.status == "active"
            and ("gambl" in case.case_type or "casino" in case.case_type or "赌" in case.summary)
            and (target_id in case.participants or target_type == "player")
        )
        enforcement_factor = max(0.05, government.enforcement_level / 100)
        audit_score = max(0.0, wealth / 8000) + property_count * 0.16 + gray_risk * 1.1 + casino_risk * 0.7 + min(1.6, (self.state.casino.daily_wagers or 0) / 900)
        if wealth < 4500 and property_count < 4 and gray_risk == 0 and casino_risk == 0:
            return
        trigger_probability = min(0.085, (0.002 + audit_score / 34) * enforcement_factor)
        if self.random.random() > trigger_probability:
            return
        fine_rate = 0.0008 + government.enforcement_level / 32000
        fine_base = max(2, int(round(wealth * fine_rate))) + property_count + gray_risk * 2 + casino_risk * 1
        fine = self._collect_tax(
            payer_type=target_type,
            payer_id=target_id,
            payer_name=target_name,
            revenue_key="fine",
            label="监管抽查罚缴",
            base_amount=fine_base,
            rate_pct=100.0,
        )
        if target_type == "player":
            self._apply_player_intervention_cost("audit", amount=2)
        else:
            agent = self._find_agent(target_id)
            agent.credit_score = self._bounded(agent.credit_score - 4 - gray_risk * 2 - casino_risk)
            agent.state.stress = self._bounded(agent.state.stress + 6 + gray_risk * 2 + casino_risk)
        self.state.lab.reputation = self._bounded(self.state.lab.reputation - min(6, 2 + gray_risk))
        government.last_audit_day = self.state.day
        audit_event = build_internal_event(
            title=f"监管抽查盯上了 {target_name}",
            summary=f"{target_name} 因资产规模、持有地产、灰线风险或地下赌场风声被抽查，缴出 ${fine}，大家开始重新估算暴露风险。",
            slot=self.state.time_slot,
            category="market",
        )
        self.state.events.insert(0, audit_event)
        self.state.events = self.state.events[:8]

    def update_tax_policy(self, payload: dict[str, float | int | str | None]) -> WorldState:
        government = self.state.government
        for key in [
            "wage_tax_rate_pct",
            "securities_tax_rate_pct",
            "property_transfer_tax_rate_pct",
            "property_holding_tax_rate_pct",
            "consumption_tax_rate_pct",
            "luxury_tax_rate_pct",
        ]:
            value = payload.get(key)
            if value is not None:
                setattr(government, key, max(0.0, min(35.0, float(value))))
        if payload.get("enforcement_level") is not None:
            government.enforcement_level = self._bounded(int(payload["enforcement_level"]))
            government.audit_cooldown_days = max(2, min(10, 2 + round((100 - government.enforcement_level) / 12)))
        if payload.get("welfare_low_cash_threshold") is not None:
            government.welfare_low_cash_threshold = max(0, min(60, int(payload["welfare_low_cash_threshold"])))
        if payload.get("welfare_base_support") is not None:
            government.welfare_base_support = max(0, min(80, int(payload["welfare_base_support"])))
        if payload.get("welfare_bankruptcy_support") is not None:
            government.welfare_bankruptcy_support = max(0, min(120, int(payload["welfare_bankruptcy_support"])))
        note = str(payload.get("note") or "手动调整税制。").strip()
        government.last_policy_note = note
        self.state.events.insert(
            0,
            build_internal_event(
                title="税制参数被重新调整",
                summary=f"政府把工资、证券、地产或消费税参数重新改了一轮。备注：{note}",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]
        self._log("tax_policy_updated", government=government.model_dump())
        return self.state

    def _build_analysis_point(self) -> AnalysisPoint:
        avg_stress = round(sum(agent.state.stress for agent in self.state.agents) / max(1, len(self.state.agents)), 2)
        avg_satisfaction = round(sum(agent.life_satisfaction for agent in self.state.agents) / max(1, len(self.state.agents)), 2)
        avg_credit = round(sum(agent.credit_score for agent in self.state.agents) / max(1, len(self.state.agents)), 2)
        team_deposits = sum(agent.deposit_balance for agent in self.state.agents)
        business_daily_revenue = sum(max(0, business.daily_revenue) for business in self.state.businesses or [])
        business_daily_customers = sum(max(0, business.daily_customers) for business in self.state.businesses or [])
        competition_heat = 0
        active_businesses = [business for business in self.state.businesses or [] if business.capacity > 0]
        if active_businesses:
            reputations = [business.reputation for business in active_businesses]
            price_gap = max(business.price_level for business in active_businesses) - min(business.price_level for business in active_businesses)
            reputation_gap = max(reputations) - min(reputations)
            competition_heat = max(8, min(100, 24 + price_gap + reputation_gap + business_daily_customers // 2))
        return AnalysisPoint(
            day=self.state.day,
            time_slot=self.state.time_slot,
            team_cash=self._team_cash_total(),
            team_assets=sum(self._agent_total_assets(agent) for agent in self.state.agents),
            team_deposits=team_deposits,
            player_cash=self.state.player.cash,
            player_assets=self._player_total_assets(),
            reputation=self.state.lab.reputation,
            market_index=round(self.state.market.index_value, 2),
            inflation_index=round(self.state.market.inflation_index, 2),
            avg_stress=avg_stress,
            avg_satisfaction=avg_satisfaction,
            avg_credit=avg_credit,
            active_events=len(self.state.events or []),
            active_gray_cases=sum(1 for case in self.state.gray_cases if case.status == "active"),
            tourists_active=self._active_tourist_count(),
            tourist_revenue_daily=self.state.tourism.daily_revenue if self.state.tourism else 0,
            government_reserve=self.state.government.reserve_balance if self.state.government else 0,
            casino_heat=self.state.casino.current_heat if self.state.casino else 0,
            casino_daily_visits=self.state.casino.daily_visits if self.state.casino else 0,
            casino_daily_wagers=self.state.casino.daily_wagers if self.state.casino else 0,
            casino_daily_tax=self.state.casino.daily_tax if self.state.casino else 0,
            business_daily_revenue=business_daily_revenue,
            business_daily_customers=business_daily_customers,
            business_competition_heat=competition_heat,
        )

    def _record_analysis_point(self) -> None:
        if self.state.analysis_history is None:
            self.state.analysis_history = []
        point = self._build_analysis_point()
        if self.state.analysis_history:
            last = self.state.analysis_history[-1]
            same_frame = (
                last.day == point.day
                and last.time_slot == point.time_slot
                and last.team_cash == point.team_cash
                and last.team_assets == point.team_assets
                and last.team_deposits == point.team_deposits
                and last.player_cash == point.player_cash
                and last.player_assets == point.player_assets
                and last.reputation == point.reputation
                and round(last.market_index, 2) == round(point.market_index, 2)
                and round(last.inflation_index, 2) == round(point.inflation_index, 2)
                and round(last.avg_stress, 2) == round(point.avg_stress, 2)
                and round(last.avg_satisfaction, 2) == round(point.avg_satisfaction, 2)
                and round(last.avg_credit, 2) == round(point.avg_credit, 2)
                and last.active_events == point.active_events
                and last.active_gray_cases == point.active_gray_cases
                and last.tourists_active == point.tourists_active
                and last.tourist_revenue_daily == point.tourist_revenue_daily
                and last.government_reserve == point.government_reserve
                and last.casino_heat == point.casino_heat
                and last.casino_daily_visits == point.casino_daily_visits
                and last.casino_daily_wagers == point.casino_daily_wagers
                and last.casino_daily_tax == point.casino_daily_tax
                and last.business_daily_revenue == point.business_daily_revenue
                and last.business_daily_customers == point.business_daily_customers
                and last.business_competition_heat == point.business_competition_heat
            )
            if same_frame:
                return
        self.state.analysis_history.append(point)
        self.state.analysis_history = self.state.analysis_history[-72:]

    def _record_daily_economy_point(
        self,
        day: int,
        *,
        tourism_private_income: int = 0,
        tourism_government_income: int = 0,
        tourism_public_income: int = 0,
    ) -> None:
        if self.state.daily_economy_history is None:
            self.state.daily_economy_history = []
        resident_consumption = sum(
            abs(int(record.amount or 0))
            for record in self.state.finance_history
            if record.day == day and record.category == "consume"
        )
        tourist_consumption = sum(
            abs(int(record.amount or 0))
            for record in self.state.finance_history
            if record.day == day and record.category == "tourism"
        )
        government_asset_income = sum(
            int(record.amount or 0)
            for record in self.state.finance_history
            if record.day == day and record.category == "government" and record.action in {"operate", "income"}
        )
        point = DailyEconomyPoint(
            day=day,
            resident_consumption=resident_consumption,
            tourist_consumption=tourist_consumption,
            tourism_private_income=tourism_private_income,
            tourism_government_income=tourism_government_income,
            tourism_public_income=tourism_public_income,
            government_asset_income=government_asset_income,
        )
        if self.state.daily_economy_history and self.state.daily_economy_history[-1].day == day:
            self.state.daily_economy_history[-1] = point
        else:
            self.state.daily_economy_history.append(point)
            self.state.daily_economy_history = self.state.daily_economy_history[-90:]

    def _record_daily_bank_point(self, day: int) -> None:
        if self.state.daily_bank_history is None:
            self.state.daily_bank_history = []
        loans_issued = sum(
            int(record.amount or 0)
            for record in self.state.finance_history
            if record.day == day and record.category == "bank" and record.action == "borrow"
        )
        loans_repaid = sum(
            abs(int(record.amount or 0))
            for record in self.state.finance_history
            if record.day == day and record.category == "bank" and record.action == "repay"
        )
        deposits_in = sum(
            int(record.amount or 0)
            for record in self.state.finance_history
            if record.day == day and record.category == "bank" and record.action == "deposit"
        )
        deposits_out = sum(
            abs(int(record.amount or 0))
            for record in self.state.finance_history
            if record.day == day and record.category == "bank" and record.action == "withdraw"
        )
        previous_outstanding = self.state.daily_bank_history[-1].outstanding_balance if self.state.daily_bank_history else 0
        previous_deposits = self.state.daily_bank_history[-1].total_deposits if self.state.daily_bank_history else 0
        point = DailyBankPoint(
            day=day,
            loans_issued=loans_issued,
            loans_repaid=loans_repaid,
            deposits_in=deposits_in,
            deposits_out=deposits_out,
            outstanding_balance=max(0, previous_outstanding + loans_issued - loans_repaid),
            total_deposits=max(0, previous_deposits + deposits_in - deposits_out),
        )
        if self.state.daily_bank_history and self.state.daily_bank_history[-1].day == day:
            self.state.daily_bank_history[-1] = point
        else:
            self.state.daily_bank_history.append(point)
            self.state.daily_bank_history = self.state.daily_bank_history[-90:]

    def _record_daily_casino_point(self, day: int) -> None:
        if self.state.daily_casino_history is None:
            self.state.daily_casino_history = []
        casino = self.state.casino or CasinoState()
        point = DailyCasinoPoint(
            day=day,
            visits=int(casino.daily_visits or 0),
            wagers=int(casino.daily_wagers or 0),
            payouts=int(casino.daily_payouts or 0),
            tax=int(casino.daily_tax or 0),
            big_wins=int(casino.daily_big_wins or 0),
            heat=int(casino.current_heat or 0),
        )
        if self.state.daily_casino_history and self.state.daily_casino_history[-1].day == day:
            self.state.daily_casino_history[-1] = point
        else:
            self.state.daily_casino_history.append(point)
            self.state.daily_casino_history = self.state.daily_casino_history[-90:]

    def _record_daily_business_point(self, day: int) -> None:
        if self.state.daily_business_history is None:
            self.state.daily_business_history = []
        self.state.daily_business_history = [point for point in self.state.daily_business_history if point.day != day]
        for business in self.state.businesses or []:
            self.state.daily_business_history.append(
                DailyBusinessPoint(
                    day=day,
                    business_id=business.id,
                    business_name=business.name,
                    category=business.category,
                    customers=int(business.daily_customers or 0),
                    resident_customers=int(business.daily_resident_customers or 0),
                    tourist_customers=int(business.daily_tourist_customers or 0),
                    revenue=int(business.daily_revenue or 0),
                    cost=int(business.daily_cost or 0),
                    profit=int(business.daily_profit or 0),
                    tax_paid=int(business.daily_tax_paid or 0),
                    reputation=int(business.reputation or 0),
                    price_level=int(business.price_level or 0),
                    quality_level=int(business.quality_level or 0),
                    lifecycle_stage=business.lifecycle_stage or "operating",
                )
            )
        self.state.daily_business_history.sort(key=lambda item: (item.day, item.business_name))
        self.state.daily_business_history = self.state.daily_business_history[-540:]

    def _reset_daily_business_metrics(self) -> None:
        for business in self.state.businesses or []:
            business.daily_customers = 0
            business.daily_resident_customers = 0
            business.daily_tourist_customers = 0
            business.daily_revenue = 0
            business.daily_cost = 0
            business.daily_profit = 0
            business.daily_tax_paid = 0
            business.market_share_hint = 0

    def _business_property(self, business: BusinessEntity) -> PropertyAsset | None:
        if not business.property_id:
            return None
        return next((asset for asset in self.state.properties if asset.id == business.property_id), None)

    def _business_post_serial(self, day: int, slot: str) -> int:
        return day * len(SLOT_SEQUENCE) + SLOT_SEQUENCE.index(slot) if slot in SLOT_SEQUENCE else day * len(SLOT_SEQUENCE)

    def _business_can_post(self, business: BusinessEntity, min_gap_slots: int = 3) -> bool:
        if not business.last_post_day or not business.last_post_slot:
            return True
        last_serial = self._business_post_serial(business.last_post_day, business.last_post_slot)
        current_serial = self._business_post_serial(self.state.day, self.state.time_slot)
        return current_serial - last_serial >= min_gap_slots

    def _sync_business_locations(self) -> None:
        property_lookup = {asset.id: asset for asset in self.state.properties or []}
        for business in self.state.businesses or []:
            if business.location_key in ROOM_LABELS:
                business.location_label = ROOM_LABELS[business.location_key]
            if not business.property_id:
                continue
            asset = property_lookup.get(business.property_id)
            if asset is None:
                continue
            anchors = PROPERTY_LAYOUT_ANCHORS.get(asset.id) or []
            if anchors:
                anchor_x, anchor_y = anchors[0]
                asset.position = Point(x=anchor_x, y=anchor_y)

    def _active_businesses(self) -> list[BusinessEntity]:
        return [
            business
            for business in (self.state.businesses or [])
            if business.lifecycle_stage not in {"closed", "acquired"} and business.capacity > 0
        ]

    def _business_tax_rate_pct(self) -> float:
        government = self.state.government
        base = max(1.8, (government.consumption_tax_rate_pct or 0) * 0.58)
        if government.big_mode_enabled and government.can_tune_taxes:
            base += 0.8
        if government.enforcement_level >= 72:
            base += 0.4
        return round(min(6.2, base), 2)

    def _collect_business_tax(self, business: BusinessEntity, base_amount: int) -> int:
        if base_amount <= 0:
            return 0
        rate_pct = self._business_tax_rate_pct()
        actual = max(1, int(round(base_amount * rate_pct / 100)))
        self.state.government.total_revenue += actual
        self.state.government.reserve_balance += actual
        self.state.government.revenues["business"] = self.state.government.revenues.get("business", 0) + actual
        business.daily_tax_paid += actual
        business.total_tax_paid += actual
        business.daily_profit -= actual
        business.total_profit -= actual
        self._append_finance_record(
            actor_id=business.id,
            actor_name=business.name,
            category="tax",
            action="tax",
            summary=f"{business.name} 按营业额缴了 ${actual} 营业税。",
            amount=-actual,
            asset_name="营业税",
            counterparty=self.state.government.name,
        )
        return actual

    def _emit_business_lifecycle_event(self, title: str, summary: str) -> None:
        self.state.events.insert(
            0,
            build_internal_event(
                title=title,
                summary=summary,
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]

    def _evaluate_business_lifecycle(self) -> None:
        businesses = list(self.state.businesses or [])
        active_businesses = [business for business in businesses if business.lifecycle_stage not in {"closed", "acquired"}]
        for business in active_businesses:
            strong_profit = business.daily_profit >= max(18, int((business.daily_revenue or 0) * 0.18))
            weak_day = business.daily_profit < -max(10, int((business.daily_cost or 0) * 0.18)) or (
                business.daily_customers == 0 and business.capacity >= 8
            )
            business.growth_streak_days = business.growth_streak_days + 1 if strong_profit else 0
            business.loss_streak_days = business.loss_streak_days + 1 if weak_day else max(0, business.loss_streak_days - 1)
            business.public_heat = max(
                0,
                min(
                    100,
                    12
                    + int(business.market_share_hint or 0) // 2
                    + max(0, 60 - business.reputation) // 3
                    + (8 if business.strategy == "gray" else 0),
                ),
            )
            if business.lifecycle_stage in {"expanding", "contracting"} and not strong_profit and not weak_day:
                business.lifecycle_stage = "operating"

        for business in active_businesses:
            if business.growth_streak_days >= 3 and business.capacity < 28:
                business.lifecycle_stage = "expanding"
                business.expansion_level += 1
                business.capacity = min(32, business.capacity + 2)
                business.quality_level = self._bounded(business.quality_level + 1)
                business.reputation = self._bounded(business.reputation + 1)
                business.last_note = f"{business.name} 这几天客流和利润都稳，已经开始扩张。"
                self._emit_business_lifecycle_event(
                    f"{business.name} 开始扩张",
                    f"{business.name} 连续几天利润和客流都稳住了，决定把规模往上抬一格。",
                )
                business.growth_streak_days = 0

        for business in list(active_businesses):
            if business.loss_streak_days < 2:
                continue
            if business.loss_streak_days >= 5:
                acquirer = next(
                    (
                        candidate
                        for candidate in sorted(active_businesses, key=lambda item: item.daily_profit, reverse=True)
                        if candidate.id != business.id
                        and candidate.lifecycle_stage not in {"closed", "acquired"}
                        and candidate.daily_profit > 0
                        and candidate.target_segment in {business.target_segment, "mixed"}
                    ),
                    None,
                )
                if acquirer is not None and self.random.random() < 0.48:
                    absorbed_capacity = max(2, min(6, max(2, business.capacity // 2)))
                    acquirer.capacity = min(36, acquirer.capacity + absorbed_capacity)
                    acquirer.reputation = max(18, min(92, int(round((acquirer.reputation * 3 + business.reputation) / 4))))
                    acquirer.last_note = f"{acquirer.name} 刚把 {business.name} 的生意并进来，准备吃下它原来的客流。"
                    business.lifecycle_stage = "acquired"
                    business.merged_into_id = acquirer.id
                    business.capacity = 0
                    business.last_note = f"{business.name} 这轮扛不住了，已经被 {acquirer.name} 并了进去。"
                    property_asset = self._business_property(business)
                    if property_asset is not None:
                        property_asset.status = "acquired"
                    self._emit_business_lifecycle_event(
                        f"{business.name} 被并购",
                        f"{business.name} 连续亏损后被 {acquirer.name} 吃下，原本的客流和位置开始并进更强的一方。",
                    )
                    continue
                business.lifecycle_stage = "closed"
                business.capacity = 0
                business.last_note = f"{business.name} 连续几天扛不住亏损，这轮已经停业。"
                property_asset = self._business_property(business)
                if property_asset is not None:
                    property_asset.status = "closed"
                self._emit_business_lifecycle_event(
                    f"{business.name} 停业",
                    f"{business.name} 因为连续亏损和客流下滑，已经暂时停业退出竞争。",
                )
                continue
            if business.capacity > 6:
                business.lifecycle_stage = "contracting"
                business.capacity = max(6, business.capacity - 2)
                business.price_level = max(18, business.price_level - 1)
                business.last_note = f"{business.name} 连着几天没稳住，这轮先收缩规模。"
                self._emit_business_lifecycle_event(
                    f"{business.name} 开始收缩",
                    f"{business.name} 最近几天利润和客流都在掉，只能先缩掉一部分规模止损。",
                )
                business.loss_streak_days = max(2, business.loss_streak_days - 1)

    def _business_ticket_value(self, business: BusinessEntity, segment: str) -> int:
        base = {
            "inn": 34,
            "market": 16,
            "workshop": 26,
            "co_op": 11,
            "backstreet": 14,
        }.get(business.category, 12)
        value = base + business.price_level // 4 + business.quality_level // 9
        if business.strategy == "premium" and segment == "tourist":
            value += 12
        if business.strategy == "low_price":
            value = max(7, value - 6)
        if business.strategy == "gray":
            value = max(9, value - 2)
        return max(6, value)

    def _business_segment_weight(self, business: BusinessEntity, segment: str) -> float:
        if business.target_segment == "mixed":
            return 1.0
        if business.target_segment == segment:
            return 1.22
        if business.target_segment == "producer" and segment == "resident":
            return 0.88
        return 0.42

    def _business_competition_score(self, business: BusinessEntity, segment: str) -> float:
        reputation = business.reputation * 0.44
        quality = business.quality_level * 0.31
        price = business.price_level * 0.28
        support = business.government_support * 0.26
        gray_bonus = business.gray_risk * (0.1 if segment == "resident" else 0.06)
        tourist_bias = 5.0 if segment == "tourist" and business.category in {"inn", "market"} else 0.0
        resident_bias = 6.0 if segment == "resident" and business.category == "co_op" else 0.0
        if segment == "resident" and self.state.market.living_cost_pressure >= 55 and business.strategy == "low_price":
            resident_bias += 8.0
        if segment == "tourist" and (
            self.state.tourism.event_day_title or self.state.tourism.latest_signal
        ):
            tourist_bias += 3.0
        if business.strategy == "gray":
            gray_bonus += 6.0
            if self.state.government.enforcement_level >= 65:
                gray_bonus -= 5.0
        return (
            self._business_segment_weight(business, segment) * 12.0
            + reputation
            + quality
            - price
            + support
            + gray_bonus
            + tourist_bias
            + resident_bias
            + self.random.uniform(-6.0, 6.0)
        )

    def _weighted_business_pick(self, businesses: list[BusinessEntity], segment: str) -> BusinessEntity | None:
        if not businesses:
            return None
        scored = [(business, max(0.1, self._business_competition_score(business, segment))) for business in businesses]
        total = sum(score for _, score in scored)
        if total <= 0:
            return self.random.choice(businesses)
        roll = self.random.uniform(0.0, total)
        running = 0.0
        for business, score in scored:
            running += score
            if running >= roll:
                return business
        return scored[-1][0]

    def _businesses_for_segment(self, segment: str) -> list[BusinessEntity]:
        businesses = self._active_businesses()
        if segment == "tourist":
            return [business for business in businesses if business.target_segment in {"tourist", "mixed"}]
        if segment == "resident":
            return [business for business in businesses if business.target_segment in {"resident", "mixed", "producer"}]
        return businesses

    def _business_feed_category(self, business: BusinessEntity) -> str:
        if business.category in {"inn", "market"}:
            return "tourism"
        if business.category == "backstreet":
            return "gossip"
        return "market"

    def _business_topic_tags(self, business: BusinessEntity, extra: list[str] | None = None) -> list[str]:
        base = [business.name]
        base.append(
            {
                "inn": "住宿服务",
                "market": "集市零售",
                "workshop": "手作工坊",
                "co_op": "生活供给",
                "backstreet": "后街生意",
            }.get(business.category, "生意"),
        )
        if business.strategy == "low_price":
            base.append("低价抢客")
        elif business.strategy == "premium":
            base.append("品质口碑")
        elif business.strategy == "gray":
            base.append("灰色引流")
        elif business.strategy == "service":
            base.append("服务体验")
        if extra:
            base.extend(extra)
        return list(dict.fromkeys(base))

    def _business_threat_score(self, content: str) -> int:
        text = str(content or "")
        patterns = [
            r"不服",
            r"别来",
            r"别怪",
            r"谁敢",
            r"敢来试试",
            r"后果自负",
            r"爱买不买",
            r"不买拉倒",
            r"闭嘴",
            r"滚",
            r"给我等着",
            r"别逼我",
            r"收拾你",
            r"盯死你",
            r"嫌贵就走",
            r"爱来不来",
            r"少废话",
            r"你自己掂量",
            r"别找事",
            r"别逼着我",
            r"闹大了不好看",
            r"出了事别怪",
            r"少在这儿",
            r"你看着办",
        ]
        score = sum(1 for pattern in patterns if re.search(pattern, text))
        if "！" in text and any(word in text for word in ["别", "敢", "后果", "滚"]):
            score += 1
        return min(3, score)

    def _apply_business_post_language_effects(self, business: BusinessEntity, post: FeedPost) -> None:
        threat_score = self._business_threat_score(post.content)
        if threat_score <= 0:
            return
        reputation_penalty = 8 + threat_score * 6
        profit_penalty = 45 + threat_score * 35
        business.reputation = max(18, min(92, business.reputation - reputation_penalty))
        business.public_heat = max(0, min(100, business.public_heat + 8 + threat_score * 6))
        business.daily_profit -= profit_penalty
        business.total_profit -= profit_penalty
        business.loss_streak_days = max(2, business.loss_streak_days + 2)
        business.growth_streak_days = 0
        if threat_score >= 2 and business.lifecycle_stage == "operating":
            business.lifecycle_stage = "contracting"
        business.last_note = f"{business.name} 刚因为公开话术太冲被骂了一轮，企业信誉、利润和客流预期都被拖住了。"
        post.credibility = max(12, min(96, int((post.credibility or 50) - (12 + threat_score * 12))))
        post.views = max(post.views or 0, (post.views or 0) + 16 + threat_score * 18)
        post.likes = max(0, (post.likes or 0) - max(0, threat_score - 1))
        post.topic_tags = list(dict.fromkeys((post.topic_tags or []) + ["话术翻车"]))
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"{business.name} 因公开话术翻车",
                summary=f"{business.name} 的公开回应被嫌说得太冲，客流和口碑一下都开始往下滑。",
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]

    def _build_business_feed_post(self, business: BusinessEntity, *, reason: str = "daily", context: str = "") -> FeedPost:
        category = self._business_feed_category(business)
        mood = "neutral"
        if business.daily_profit >= max(36, business.daily_revenue // 3):
            mood = "spark"
        elif business.daily_profit < 0 or business.reputation <= 40:
            mood = "tense"
        tags: list[str] = []
        if reason == "pressure":
            tags.extend(["价格", "服务调整"])
        elif reason == "staff":
            tags.extend(["员工状态", "赶工压力"])
        elif reason == "gray":
            tags.extend(["后街风声", "抢客"])
            mood = "tense"
        elif business.daily_tourist_customers > business.daily_resident_customers:
            tags.append("游客口碑")
            mood = "warm"
        else:
            tags.append("客流")
        regular_style = business.strategy != "gray"
        if business.category == "inn":
            options = (
                [
                    f"{business.name} 今天入住比昨天更稳。热水、床品和夜里的安静，我们会继续守住，欢迎来住一晚看看。",
                    f"{business.name} 这轮住客比预想多。房间整理、入住节奏和夜间安静都已经重新收稳了。",
                    f"{business.name} 今天夜住需求抬起来了。想找干净、安静、住得踏实的地方，可以来这边看看。",
                ]
                if regular_style
                else [
                    f"{business.name} 今晚还是主打住得快、住得省心。临时想歇脚的，可以直接来问还有没有空房。",
                    f"{business.name} 这边今晚房间周转顺，拎包就能住，想少折腾的人可以先来看看。",
                    f"{business.name} 今天后街这边住一晚更省事。想赶紧落脚的，可以直接来问价。",
                ]
            )
        elif business.category == "market":
            options = (
                [
                    f"{business.name} 今天人流比昨天更挤。摊位更顺、东西更新鲜，欢迎再来逛一圈。",
                    f"{business.name} 这轮客人多，越忙越得把东西摆齐、把招呼打顺，别让人逛到一半就想走。",
                    f"{business.name} 今天接住了一波客流。价要实在，东西也得挑得出来，这才留得住回头客。",
                ]
                if regular_style
                else [
                    f"{business.name} 今天这边还是主打便宜、拿得快。想顺手买点实在东西的，可以先来这边转一圈。",
                    f"{business.name} 这边今天货转得快，价也压得低。想省一点、少绕一点的，可以直接来挑。",
                    f"{business.name} 今天这边还是图一个来得快、拿得走。看中就拿，不用多绕路。",
                ]
            )
        elif business.category == "workshop":
            options = (
                [
                    f"{business.name} 这两天单子更满了。定制、修补和手作件都在排单，想做细一点的可以直接来问。",
                    f"{business.name} 现在最重要的是把手上的活按时交出去，别让品质在赶工里掉下来。想看做工细节，欢迎来店里聊。",
                    f"{business.name} 这一轮工单更多了。想做定制、想看手艺、想问交期，都可以直接来店里细聊。",
                ]
                if regular_style
                else [
                    f"{business.name} 这边今天出活更快。想少等一点、赶进度一点的，可以先来问这一轮排单。",
                    f"{business.name} 这边主打快做快拿。想赶时间、又不想多绕的，可以直接来说需求。",
                    f"{business.name} 今天工单还是排得紧，但能快交的活我们会尽量先安排，先到先排。",
                ]
            )
        elif business.category == "co_op":
            options = (
                [
                    f"{business.name} 这几天盯的是每天都要买的那点东西。价稳、货足，大家买着才踏实。",
                    f"{business.name} 做的是日常供给。米面、蔬菜和常用货不断档，就是我们今天最重要的事。",
                    f"{business.name} 今天继续把常用货摆稳。想买实在的日常东西，可以先来这边看一圈。",
                ]
                if regular_style
                else [
                    f"{business.name} 今天常用货还是摆得很实。想买得快一点、价别太虚的，可以先来这边看看。",
                    f"{business.name} 这边今天还是主打实在和省心。米面蔬菜这些常用货，到了就能拿。",
                    f"{business.name} 今天把常用货备得更足了。想少跑两趟的人，可以先来这边补一轮。",
                ]
            )
        else:
            options = [
                f"{business.name} 今天后街又热了一点。想图快、图省钱的，可以来看看这一轮新到的货。",
                f"{business.name} 这边今天主打快和实惠。东西和价都先摆明白，合不合适你自己一眼能看出来。",
                f"{business.name} 今天还是主打便宜和现货。想省一点、拿得快一点，可以先来这边看看。",
            ]
        if business.strategy == "gray":
            if reason == "pressure" and context:
                options = [
                    f"{business.name} 已经听见大家在念“{context}”。接下来先把价格说明和货路解释讲清楚，免得越传越偏。",
                    f"{business.name} 这两天被人拿“{context}”说得很多。我们会把现在卖的货、现在给的价都摊开说清楚。",
                ]
            elif reason == "gray":
                options = [
                    f"{business.name} 最近风声有点杂。该摆出来的货和价我们都会摆出来，想省一点的可以自己来看看。",
                    f"{business.name} 外面怎么传是一回事，来这里能买到什么、值不值，还是得你自己来店里看一眼。",
                ]
            else:
                options = [
                    f"{business.name} 今天还是主打快和实惠。想图便宜、想少绕路的，可以直接来后街看看。",
                    f"{business.name} 这边货转得快、价也压得低。想快点拿到东西的人，通常会先拐来这里。",
                    f"{business.name} 今天后街又热了一点。省钱、省时间、拿得到货，这三样我们都尽量给到。",
                ]
        content = options[self.random.randint(0, len(options) - 1)]
        if reason == "pressure" and context:
            content = (
                f"{business.name} 已经记下今天这波“{context}”的抱怨。接下来会先把价格说明、货架摆放和招呼人的方式收拾清楚，欢迎回来再看看我们有没有改到位。"
                if regular_style
                else f"{business.name} 最近一直被人拿“{context}”说事。我们会先把现在卖的货、现在给的价和今天的做法讲清楚，省得外面越传越偏。"
            )
        elif reason == "staff":
            content = (
                f"{business.name} 也听见了“{context}”这类议论。接下来会先把排班和做事节奏收一收，别让客人和员工都顶着难受。"
                if regular_style
                else f"{business.name} 最近被人拿“{context}”念得很紧。我们会先把排班和交接理顺，别让前台后场都绷着。"
            )
        elif reason == "gray":
            content = f"{business.name} 这几天被人拿“{context}”反复念叨。接下来会先把货路、价格说明和对外回应讲清楚，别让风声一直压着生意。"
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type="business",
            author_id=business.id,
            author_name=business.name,
            day=self.state.day,
            time_slot=self.state.time_slot,
            category=category,
            mood=self._normalize_feed_mood(mood),
            content=self._clean_feed_text(content),
            topic_tags=self._business_topic_tags(business, tags),
            desire_tags=["利润最大化", "留住客流", "压低负面舆情"],
            likes=4 + max(0, business.reputation // 18) + self.random.randint(0, 3),
            views=36 + business.daily_customers * 10 + self.random.randint(0, 22),
            summary=f"{business.name} 发了一条营业说明。",
            impacts=["影响客流判断", "影响微博讨论"],
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _build_business_public_comment(self, business: BusinessEntity, *, tone: str, topic: str) -> FeedPost | None:
        use_tourist = business.category in {"inn", "market"} and self.state.tourists and self.random.random() < 0.62
        if use_tourist:
            tourist = self.random.choice(self.state.tourists)
            if tone == "positive":
                options = [
                    f"{business.name} 这轮让我愿意多停一会儿。东西不一定最便宜，但起码让人觉得钱没白花。",
                    f"我今天在 {business.name} 绕了两圈，最后记住的不是热闹，是它没有把人当流水线上的钱包。",
                    f"{business.name} 这边体验顺，价和品质至少对得上，不像有些地方只会把人往里拽。",
                ]
            else:
                options = [
                    f"{business.name} 这边今天有点拧巴。{topic} 这种事一冒出来，游客的脚马上就会慢下来。",
                    f"{business.name} 这两天被人念得最多的就是“{topic}”。外面的人其实很简单，感觉不舒服就不想多花钱。",
                    f"说游客视角的话，{business.name} 一旦被盯上“{topic}”，停留和消费都会先掉一截。",
                ]
            author_type = "tourist"
            author_id = tourist.id
            author_name = tourist.name
            category = "tourism"
            desire_tags = [tourist.favorite_topic or "体验感"]
        else:
            agent = self.random.choice(self.state.agents)
            if tone == "positive":
                options = [
                    f"{business.name} 这轮客流上得不冤。价、品质和做事的路数，至少看得出是在认真守口碑。",
                    f"现在大家都在比谁更会抢人，但 {business.name} 这种能把品质守住的，最后更容易把客留住。",
                    f"{business.name} 今天跑得顺，不只是因为热闹，是因为它没把东西做糙、也没把人逼得太狠。",
                ]
            else:
                options = [
                    f"{business.name} 这边现在最伤的是“{topic}”。客可能还能抢回来，口碑和人心一散就没那么好补了。",
                    f"{business.name} 这轮被人拿“{topic}”说得很多。价格、货路和怎么对自己人，迟早都会在微博上翻出来。",
                    f"{business.name} 要是真继续往“{topic}”上拖，眼前那点利润，很快就会被负面舆情吃掉。",
                ]
            author_type = "agent"
            author_id = agent.id
            author_name = agent.name
            category = "gossip" if tone != "positive" else "market"
            desire_tags = [DESIRE_LABELS.get(dominant_desire_for_agent(self.state, agent)[0], "眼前这件事")]
        post = FeedPost(
            id=f"feed-{uuid4().hex[:8]}",
            author_type=author_type,
            author_id=author_id,
            author_name=author_name,
            day=self.state.day,
            time_slot=self.state.time_slot,
            category=category,
            mood="warm" if tone == "positive" else "tense",
            content=self._clean_feed_text(options[self.random.randint(0, len(options) - 1)]),
            topic_tags=self._business_topic_tags(business, [topic]),
            desire_tags=desire_tags,
            likes=3 + self.random.randint(0, 5),
            views=28 + business.daily_customers * 8 + self.random.randint(0, 18),
            summary=f"{author_name} 在微博上谈到了 {business.name}。",
            impacts=["影响客流判断", "影响企业口碑"],
        )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        return post

    def _businesses_mentioned_in_post(self, post: FeedPost) -> list[BusinessEntity]:
        text = f"{post.content} {' '.join(post.topic_tags or [])}"
        matches = [business for business in self.state.businesses or [] if business.name and business.name in text]
        return matches

    def _apply_business_public_reaction(self, post: FeedPost) -> None:
        businesses = self._businesses_mentioned_in_post(post)
        if not businesses or post.author_type == "business":
            return
        tone = self._feed_tone(post.content)
        heat_weight = max(1, min(6, post.heat // 35 + 1))
        text = f"{post.content} {' '.join(post.topic_tags or [])}"
        topic = "口碑"
        if re.search(r"贵|涨价|不值|宰人|价", text):
            topic = "价格"
        elif re.search(r"工人|员工|太累|没歇|压榨|赶工", text):
            topic = "员工状态"
        elif re.search(r"质量|糙|假|货路|灰货|不踏实|服务|慢", text):
            topic = "品质和服务"
        for business in businesses:
            if tone > 0:
                business.reputation = max(18, min(92, business.reputation + heat_weight))
                if business.strategy in {"premium", "steady"} and business.daily_customers >= max(2, business.capacity // 3):
                    business.price_level = max(18, min(90, business.price_level + 1))
                business.last_note = f"{business.name} 刚被微博夸到“{topic}”，眼下客流更愿意往这边靠。"
                continue
            if tone < 0:
                business.reputation = max(18, min(92, business.reputation - heat_weight * 2))
                if topic == "价格":
                    business.price_level = max(18, business.price_level - max(1, heat_weight // 2))
                elif topic == "品质和服务":
                    business.quality_level = max(18, min(92, business.quality_level + max(1, heat_weight // 2)))
                elif topic == "员工状态":
                    business.capacity = max(5, business.capacity - 1)
                    business.quality_level = max(18, min(92, business.quality_level + 1))
                if business.strategy == "gray":
                    business.gray_risk = max(0, min(100, business.gray_risk + heat_weight))
                business.last_note = f"{business.name} 被微博抓着“{topic}”不放，眼下不得不先回应这波舆情。"

    def _emit_business_public_discourse(self) -> None:
        businesses = sorted(self.state.businesses or [], key=lambda item: item.daily_revenue, reverse=True)
        if not businesses:
            return
        current_slot_posts = [
            post for post in (self.state.feed_timeline or [])[:40]
            if post.day == self.state.day and post.time_slot == self.state.time_slot
        ]
        if sum(1 for post in current_slot_posts if post.author_type == "business") >= 2:
            return
        leader = businesses[0]
        laggard = businesses[-1]
        recent_mentions = {
            business.id: [
                post for post in (self.state.feed_timeline or [])[:24]
                if business.name in f"{post.content} {' '.join(post.topic_tags or [])}"
            ]
            for business in businesses
        }
        if leader.daily_customers >= 3 and self._business_can_post(leader, 4) and self.random.random() < 0.14:
            self._append_feed_post(self._build_business_feed_post(leader), remember=True, apply_impacts=True)
        if laggard.daily_profit < 0 and self._business_can_post(laggard, 4) and self.random.random() < 0.1:
            self._append_feed_post(self._build_business_feed_post(laggard, reason="pressure", context="价格和品质"), remember=True, apply_impacts=True)
        if (
            leader.category == "backstreet"
            and leader.daily_customers >= 3
            and self._business_can_post(leader, 5)
            and self.random.random() < 0.12
        ):
            comment = self._build_business_public_comment(leader, tone="negative", topic="灰色引流和压价")
            if comment is not None:
                self._append_feed_post(comment, remember=True, apply_impacts=True)
        spotlight = next(
            (
                business
                for business in businesses
                if business.category != "backstreet"
                and business.daily_customers >= 2
                and business.reputation >= 58
            ),
            None,
        )
        if spotlight is not None and self.random.random() < 0.18:
            comment = self._build_business_public_comment(spotlight, tone="positive", topic="品质和做事路数")
            if comment is not None:
                self._append_feed_post(comment, remember=True, apply_impacts=True)
        for business in businesses[:3]:
            mentions = recent_mentions.get(business.id) or []
            if not mentions:
                continue
            negative_mentions = [post for post in mentions if self._feed_tone(post.content) < 0 and post.author_type != "business"]
            if (
                negative_mentions
                and self._business_can_post(business, 3)
                and not any(post.author_type == "business" and post.author_id == business.id for post in current_slot_posts)
            ):
                issue = "价格和品质"
                merged = " ".join(post.content for post in negative_mentions[:2])
                if re.search(r"工人|员工|太累|赶工|没歇", merged):
                    issue = "员工状态"
                    reason = "staff"
                elif re.search(r"灰货|后街|路数|不踏实|货路", merged):
                    issue = "灰色引流"
                    reason = "gray"
                else:
                    reason = "pressure"
                self._append_feed_post(
                    self._build_business_feed_post(business, reason=reason, context=issue),
                    remember=True,
                    apply_impacts=True,
                )
                break

    def _emit_business_competition_signals(self) -> None:
        businesses = sorted(self.state.businesses or [], key=lambda item: item.daily_revenue, reverse=True)
        if len(businesses) < 2:
            return
        leader = businesses[0]
        runner_up = businesses[1]
        if leader.daily_revenue <= 0:
            return
        if leader.daily_revenue - runner_up.daily_revenue >= 48 and self.random.random() < 0.14:
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{leader.name} 把今天的客流吃得更满",
                    summary=f"{leader.name} 这一时段抢走了更多客流，{runner_up.name} 开始明显感到压力。",
                    slot=self.state.time_slot,
                    category="market",
                ),
            )
            self.state.events = self.state.events[:8]
        if leader.category == "backstreet" and leader.daily_revenue >= 48 and self.random.random() < 0.2:
            self.state.gray_cases.insert(
                0,
                GrayCase(
                    id=f"gray-{uuid4().hex[:8]}",
                    case_type="business_gray_competition",
                    participants=["gray-market"],
                    participant_names=[leader.name],
                    topic="低价和灰货同时抢客",
                    summary=f"{leader.name} 用低价和灰货把客流往后街带，正规生意已经开始抱怨。",
                    amount=leader.daily_revenue,
                    severity=2,
                    start_day=self.state.day,
                    exposure_risk=34,
                    status="active",
                ),
            )
            self.state.gray_cases = self.state.gray_cases[:12]
        if leader.price_level + 12 <= runner_up.price_level and leader.daily_customers >= 2 and self.random.random() < 0.18:
            self.state.gray_cases.insert(
                0,
                GrayCase(
                    id=f"gray-{uuid4().hex[:8]}",
                    case_type="business_price_undercut",
                    participants=[leader.id, runner_up.id],
                    participant_names=[leader.name, runner_up.name],
                    topic="低价抢客",
                    summary=f"{leader.name} 这轮把价格压得更低，{runner_up.name} 已经开始怀疑对方是不是在拿灰色货源抢客。",
                    amount=max(0, leader.daily_revenue - runner_up.daily_revenue),
                    severity=2,
                    start_day=self.state.day,
                    exposure_risk=28,
                    status="active",
                ),
            )
            self.state.gray_cases = self.state.gray_cases[:12]

    def _tick_business_competition(self) -> None:
        businesses = self._active_businesses()
        if not businesses:
            return
        slot_stats = {
            business.id: {
                "customers": 0,
                "resident": 0,
                "tourist": 0,
                "revenue": 0,
                "cost": 0,
            }
            for business in businesses
        }
        resident_slot_weight = {
            "morning": 0.6,
            "noon": 1.15,
            "afternoon": 0.85,
            "evening": 1.05,
            "night": 0.45,
        }.get(self.state.time_slot, 0.8)
        tourist_slot_weight = {
            "morning": 0.5,
            "noon": 0.95,
            "afternoon": 1.1,
            "evening": 1.18,
            "night": 0.9,
        }.get(self.state.time_slot, 0.9)
        resident_pool = max(
            1,
            int((len(self.state.agents) + 1) * resident_slot_weight + self.state.lab.team_atmosphere / 55),
        )
        tourist_pool = max(0, int(len(self.state.tourists or []) * tourist_slot_weight))
        for _ in range(resident_pool):
            business = self._weighted_business_pick(self._businesses_for_segment("resident"), "resident")
            if business is None:
                continue
            spend = self._business_ticket_value(business, "resident") + self.random.randint(-4, 6)
            spend = max(6, spend)
            business.daily_customers += 1
            business.daily_resident_customers += 1
            business.daily_revenue += spend
            cost = max(3, int(spend * 0.48))
            business.daily_cost += cost
            slot_stats[business.id]["customers"] += 1
            slot_stats[business.id]["resident"] += 1
            slot_stats[business.id]["revenue"] += spend
            slot_stats[business.id]["cost"] += cost
        for _ in range(tourist_pool):
            business = self._weighted_business_pick(self._businesses_for_segment("tourist"), "tourist")
            if business is None:
                continue
            spend = self._business_ticket_value(business, "tourist") + self.random.randint(-5, 12)
            spend = max(8, spend)
            business.daily_customers += 1
            business.daily_tourist_customers += 1
            business.daily_revenue += spend
            cost = max(4, int(spend * 0.46))
            business.daily_cost += cost
            slot_stats[business.id]["customers"] += 1
            slot_stats[business.id]["tourist"] += 1
            slot_stats[business.id]["revenue"] += spend
            slot_stats[business.id]["cost"] += cost
        for business in businesses:
            slot_overhead = max(2, business.capacity // 6)
            business.daily_cost += slot_overhead
            slot_stats[business.id]["cost"] += slot_overhead
            business.daily_profit = business.daily_revenue - business.daily_cost
            business.total_customers += slot_stats[business.id]["customers"]
            business.total_revenue += slot_stats[business.id]["revenue"]
            business.total_profit += slot_stats[business.id]["revenue"] - slot_stats[business.id]["cost"]
            if slot_stats[business.id]["revenue"] > 0:
                self._collect_business_tax(business, slot_stats[business.id]["revenue"])
            share_hint = business.daily_customers * 4 + max(0, business.daily_tourist_customers * 3)
            business.market_share_hint = max(0, min(100, share_hint))
            reputation_shift = 0
            if business.daily_customers >= max(3, business.capacity // 2):
                reputation_shift += 1
            if business.daily_profit < 0:
                reputation_shift -= 1
            if business.strategy == "gray" and self.state.government.enforcement_level >= 60 and business.daily_customers > 0:
                reputation_shift -= 1
            business.reputation = max(18, min(92, business.reputation + reputation_shift))
            if business.id == "business-workshop" and business.daily_profit > 0:
                self.state.company.total_work_sessions += 0
            if business.id == "business-qingsong-coop" and business.daily_profit > 0:
                self.state.market.living_cost_pressure = max(0, self.state.market.living_cost_pressure - 1)
            business.last_note = (
                f"{business.name} 这一时段接了 {business.daily_customers} 单，净流 {business.daily_profit:+}。"
                if business.daily_customers
                else f"{business.name} 这一时段客流偏淡，大家暂时还在观望。"
            )
            if slot_stats[business.id]["customers"] > 0:
                self._append_finance_record(
                    actor_id=business.id,
                    actor_name=business.name,
                    category="business",
                    action="operate",
                    summary=(
                        f"{business.name} 这一时段接了 {slot_stats[business.id]['customers']} 单，"
                        f"收入 ${slot_stats[business.id]['revenue']}，净流 ${slot_stats[business.id]['revenue'] - slot_stats[business.id]['cost']}。"
                    ),
                    amount=slot_stats[business.id]["revenue"],
                    asset_name=business.location_label or business.name,
                    counterparty=f"{slot_stats[business.id]['resident']} 位居民 / {slot_stats[business.id]['tourist']} 位游客",
                )
        self._emit_business_competition_signals()
        self._emit_business_public_discourse()

    def _backfill_daily_economy_history_from_finance(self) -> None:
        if self.state.daily_economy_history:
            return
        available_days = sorted({record.day for record in self.state.finance_history if record.day is not None})
        for day in available_days[-30:]:
            self._record_daily_economy_point(day)

    def _backfill_daily_bank_history_from_finance(self) -> None:
        if self.state.daily_bank_history:
            return
        available_days = sorted(
            {
                record.day
                for record in self.state.finance_history
                if record.day is not None and record.category == "bank"
            }
        )
        for day in available_days[-30:]:
            self._record_daily_bank_point(day)

    def _backfill_daily_casino_history_from_finance(self) -> None:
        if self.state.daily_casino_history:
            return
        available_days = sorted(
            {
                record.day
                for record in self.state.finance_history
                if record.day is not None and record.category == "casino"
            }
        )
        if not available_days:
            return
        trailing_days = available_days[-10:]
        for day in trailing_days:
            day_records = [record for record in self.state.finance_history if record.day == day and record.category == "casino"]
            visits = len({record.actor_id for record in day_records})
            wagers = sum(abs(int(record.amount or 0)) for record in day_records if record.action == "gamble")
            payouts = 0
            tax = 0
            big_wins = 0
            point = DailyCasinoPoint(
                day=day,
                visits=visits,
                wagers=wagers,
                payouts=payouts,
                tax=tax,
                big_wins=big_wins,
                heat=0,
            )
            self.state.daily_casino_history.append(point)
        self.state.daily_casino_history = self.state.daily_casino_history[-90:]

    def _backfill_casino_dialogue_history_from_finance(self) -> None:
        if self.state.dialogue_history is None:
            self.state.dialogue_history = []
        if any(record.gray_trade_type == "地下赌博" for record in self.state.dialogue_history):
            return
        casino_records = [
            record
            for record in self.state.finance_history or []
            if record.category == "casino" and record.action == "gamble"
        ]
        if not casino_records:
            return
        for record in reversed(casino_records[:20]):
            summary = record.summary or f"{record.actor_name} 在后巷地下赌场试了手气。"
            self.state.dialogue_history.insert(
                0,
                DialogueRecord(
                    id=f"dialogue-{uuid4().hex[:8]}",
                    kind="gray_trade",
                    day=record.day,
                    time_slot=record.time_slot,
                    participants=[record.actor_id],
                    participant_names=[record.actor_name],
                    topic="地下赌场",
                    summary=summary,
                    key_point=summary,
                    transcript=[summary],
                    desire_labels={record.actor_name: "想搏一把运气和现金缓冲"},
                    mood="warm" if (record.amount or 0) > 0 else "tense" if (record.amount or 0) < 0 else "neutral",
                    financial_note=f"{record.actor_name} 在 {record.asset_name or '后巷地下赌场'} 参与了地下赌博，净变化 ${record.amount or 0}。",
                    gray_trade=True,
                    gray_trade_type="地下赌博",
                    gray_trade_severity=2 if (record.amount or 0) >= 0 else 3,
                ),
            )
        self.state.dialogue_history = self.state.dialogue_history[:1000]

    def _player_desire_label(self, text: str) -> str:
        normalized = text.strip()
        if not normalized:
            return "想先试探气氛"
        if any(token in normalized for token in ["钱", "借", "预算", "请", "报销", "利息", "股票", "买", "卖"]):
            return "想缓解钱压"
        if any(token in normalized for token in ["累", "困", "回去", "休息", "睡"]):
            return "想先喘口气"
        if any(token in normalized for token in ["陪", "聊", "想你", "一起", "听我", "你还好吗"]):
            return "想被接住"
        if any(token in normalized for token in ["为什么", "怎么", "证据", "讲清", "解释"]):
            return "想把话讲清"
        if any(token in normalized for token in ["机会", "热点", "消息", "外部", "新闻"]):
            return "想抓机会"
        if any(token in normalized for token in ["科研", "GeoAI", "实验", "模型"]):
            return "想把事情往前推"
        return "想继续聊下去"

    def _player_dialogue_key_point(
        self,
        dialogue: DialogueOutcome,
        agent_name: str,
        player_desire: str,
        agent_desire: str,
        financial_note: str,
        relation_delta: int,
    ) -> str:
        if financial_note:
            return f"这轮对话落到了钱上：{financial_note}"
        if relation_delta <= -3:
            return f"你在试探“{player_desire}”，{agent_name} 则更受“{agent_desire}”驱动，气氛偏顶。"
        if relation_delta >= 3:
            return f"你在试探“{player_desire}”，{agent_name} 顺着“{agent_desire}”接住了这轮话。"
        return f"这轮主要在围绕“{dialogue.topic or '眼前这件事'}”互相摸清对方当下最在意什么。"

    def _advance_geoai_progress(self, amount: int, reason: str = "") -> None:
        if amount <= 0:
            return
        previous = self.state.lab.geoai_progress
        self.state.lab.geoai_progress = max(0, previous + amount)
        self._emit_geoai_milestones(previous, self.state.lab.geoai_progress, reason)

    def _emit_geoai_milestones(self, previous: int, current: int, reason: str) -> None:
        if self.state.geoai_milestones is None:
            self.state.geoai_milestones = []
        candidate_milestones = geoai_milestones_up_to(current)
        crossed = [threshold for threshold in candidate_milestones if previous < threshold <= current and threshold not in self.state.geoai_milestones]
        if not crossed:
            return
        for threshold in crossed:
            self.state.geoai_milestones.append(threshold)
            self.state.lab.reputation = self._bounded(self.state.lab.reputation + (4 if threshold >= 260 else 3))
            milestone_event = LabEvent(
                id=f"event-{uuid4().hex[:8]}",
                category="geoai",
                title=f"空间智能研究突破 {threshold} 点里程碑",
                summary=f"实验室的空间智能研究累计推进到 {current} 点，已跨过 {threshold} 点档位。触发原因与“{reason or '近期持续对话与外部信号'}”相关，市场开始重新定价 GEO 板块。",
                source="实验室新闻台",
                time_slot=self.state.time_slot,
                impacts={"collective_reasoning": 2, "research_progress": 1},
                participants=[],
                tone_hint=2,
                market_target="GEO",
                market_strength=5 if threshold >= 260 else 4,
            )
            self.state.events.insert(0, milestone_event)
            self.state.events = self.state.events[:8]
            for agent in self.state.agents:
                self._apply_event_to_agent(agent, milestone_event)
            self._apply_event_to_market(milestone_event)
            self._log(
                "geoai_milestone",
                milestone={"threshold": threshold, "current": current, "reason": reason or "持续推进"},
            )

    def _ambient_dialogue_key_point(
        self,
        first_name: str,
        second_name: str,
        topic: str,
        mood: str,
        first_desire: str,
        second_desire: str,
        financial_note: str,
    ) -> str:
        topic = self._humanize_dialogue_topic(topic)
        if financial_note:
            return f"这几句没白说，最后已经落成了一笔实实在在的动作：{financial_note}"
        if mood == "tense":
            variants = [
                f"{first_name} 惦记的是“{first_desire}”，{second_name} 更在意“{second_desire}”，所以这几句越说越顶。",
                f"{first_name} 盯着“{first_desire}”，{second_name} 放不下“{second_desire}”，谁都没肯先让一步。",
                f"{first_name} 想先顾“{first_desire}”，{second_name} 偏要把“{second_desire}”摆在前面，话自然就拧起来了。",
            ]
            return self.random.choice(variants)
        if mood in {"warm", "spark"} and first_desire == second_desire:
            variants = [
                f"两个人这会儿都惦记着“{first_desire}”，所以很快就站到了一边。",
                f"他们心里想的其实差不多，都是“{first_desire}”，这轮自然更容易说到一起。",
                f"因为都在顾“{first_desire}”，这几句反而让他们更容易接上彼此。",
            ]
            return self.random.choice(variants)
        if mood in {"warm", "spark"}:
            variants = [
                f"虽然各有各的心思，但他们都愿意顺着“{topic}”继续往下说。",
                f"这轮没有谁急着把话掐掉，反而都想顺着“{topic}”再往前探一步。",
                f"他们看重的点不完全一样，但都愿意把“{topic}”继续接下去。",
            ]
            return self.random.choice(variants)
        variants = [
            f"这几句主要是在摸彼此到底怎么看“{topic}”。",
            f"这轮话还在试探阶段，谁也在看对方会怎么接“{topic}”。",
            f"他们嘴上没把话挑明，但都在试探对方对“{topic}”到底是什么态度。",
        ]
        return self.random.choice(variants)

    def _propagate_shared_signal_relationships(self, event: LabEvent) -> None:
        if event.category not in {"geoai", "tech", "market"}:
            return
        pairs = [("lin", "jo"), ("lin", "mika"), ("mika", "rae"), ("rae", "kai")]
        for left_id, right_id in pairs:
            left = self._find_agent(left_id)
            right = self._find_agent(right_id)
            if left.credit_score <= 35 or right.credit_score <= 35:
                self._adjust_relation(left, right, 0, f"虽然都看到了“{event.title}”，但低口碑让他们没太愿意互相接招。")
                continue
            delta = 3 if min(left.credit_score, right.credit_score) >= 70 else 1
            self._adjust_relation(left, right, delta, f"一起被“{event.title}”激发了讨论。")

    def _room_for(self, x: int, y: int) -> str:
        for room in ROOMS:
            if room.contains(x, y):
                return room.name
        return "foyer"

    def _room(self, room_name: str) -> Room:
        for room in ROOMS:
            if room.name == room_name:
                return room
        return ROOMS[0]

    def _is_property_blocked(self, x: int, y: int) -> bool:
        for asset in self.state.properties:
            if asset.status not in {"owned", "listed", "operating"}:
                continue
            if asset.position.x <= x <= asset.position.x + asset.width - 1 and asset.position.y <= y <= asset.position.y + asset.height - 1:
                return True
        return False

    def _is_blocked(self, x: int, y: int) -> bool:
        return any(obstacle.contains(x, y) for obstacle in OBSTACLES) or self._is_property_blocked(x, y)

    def _is_walkable(self, x: int, y: int) -> bool:
        return 1 <= x <= self.state.world_width and 1 <= y <= self.state.world_height and not self._is_blocked(x, y)

    def _move_with_collision(self, point: Point, dx: int, dy: int) -> Point:
        candidates = [(dx, dy)]
        if dx != 0 and dy != 0:
            candidates.extend([(dx, 0), (0, dy)])
        for step_x, step_y in candidates:
            next_x = max(1, min(self.state.world_width, point.x + step_x))
            next_y = max(1, min(self.state.world_height, point.y + step_y))
            if self._is_walkable(next_x, next_y):
                return Point(x=next_x, y=next_y)
        return point

    def _move_in_room(self, point: Point, room: Room, candidates: list[tuple[int, int]]) -> Point:
        for step_x, step_y in candidates:
            next_point = room.clamp(point.x + step_x, point.y + step_y)
            if self._is_walkable(next_point.x, next_point.y):
                return next_point
        return point

    def _nearest_walkable(self, point: Point, room: Room) -> Point:
        if self._is_walkable(point.x, point.y):
            return point
        for radius in range(1, 4):
            for offset_x in range(-radius, radius + 1):
                for offset_y in range(-radius, radius + 1):
                    candidate = room.clamp(point.x + offset_x, point.y + offset_y)
                    if self._is_walkable(candidate.x, candidate.y):
                        return candidate
        return point

    def _remember(self, agent: Agent, text: str, importance: int, long_term: bool = False) -> None:
        entry = MemoryEntry(text=text, day=self.state.day, time_slot=self.state.time_slot, importance=importance)
        agent.short_term_memory.insert(0, entry)
        agent.short_term_memory = agent.short_term_memory[:5]
        if long_term:
            self._remember_long_term(agent, text, importance)

    def _remember_tourist(self, tourist: TouristAgent, text: str, importance: int = 1) -> None:
        entry = MemoryEntry(text=text, day=self.state.day, time_slot=self.state.time_slot, importance=importance)
        tourist.short_term_memory.insert(0, entry)
        tourist.short_term_memory = tourist.short_term_memory[:4]

    def _memory_signature(self, text: str) -> str:
        normalized = (
            text.replace("你刚刚", "")
            .replace("刚刚", "")
            .replace("刚收到", "")
            .replace("今天", "")
            .replace("这一轮", "")
            .replace("第 ", "第")
            .replace("。", "")
            .replace("，", "")
            .replace("：", "")
            .replace("“", "")
            .replace("”", "")
            .strip()
        )
        return normalized[:72]

    def _summarize_long_term_memory(self, text: str) -> str:
        summary = text.strip()
        summary = summary.replace("实验室", "小镇")
        if summary.startswith("LabDaily："):
            brief = summary.replace("LabDaily：", "", 1).strip()
            if brief.startswith("股市速写："):
                market_line = brief.replace("股市速写：", "", 1).split("；", 1)[0].strip("。 ")
                summary = f"今天一早大家还在念叨：{market_line}。"
            elif "；" in brief:
                first, second = brief.split("；", 1)
                summary = f"晨报里反复提到：{first.strip()}，{second.strip()}。"
            else:
                summary = f"晨报里反复提到：{brief.strip()}。"
        if summary.startswith("晨报一直在提醒：股市速写："):
            market_line = summary.replace("晨报一直在提醒：股市速写：", "", 1).split("，板块主线", 1)[0].strip("。 ")
            summary = f"今天一早大家还在念叨：{market_line}。"
        if summary.startswith("游客消息："):
            message = summary.replace("游客消息：", "", 1).strip("。 ")
            summary = f"外地传来的“{message}”这件事，还挂在心里。"
        event_match = re.match(r"^“(.+?)”可能会?改变小镇接下来的讨论方向。?$", summary)
        if event_match:
            summary = f"“{event_match.group(1)}”这件事，大家到现在还没放下。"
        event_match = re.match(r"^“(.+?)”这件事，接下来多半会影响小镇里的看法。?$", summary)
        if event_match:
            summary = f"这两天大家都绕不开“{event_match.group(1)}”这件事。"
        feed_match = re.match(r"^(?:微博：|微博上有人提到：)(.+?说“.+)$", summary)
        if feed_match:
            text = feed_match.group(1).strip()
            if len(text) > 34:
                text = text[:32].rstrip("，。、“”\" ") + "…"
            summary = f"那条微博还挂在心里：{text}"
        replacements = [
            ("你刚刚回复玩家：", "你和玩家已经说到："),
            ("玩家刚刚说：", "玩家提过："),
            ("刚收到外部事件：", "外部消息："),
            ("刚收到外部事件：“", "外部消息“"),
            ("关于“", "“"),
            ("”的讨论值得继续追。", "”这件事值得继续留意。"),
            ("可能改变实验室接下来的讨论方向。", "可能会改变小镇接下来的讨论方向。"),
            ("你在", ""),
            ("和玩家聊了“", "和玩家聊过“"),
            ("天气是", "当时天气是"),
            ("微博：", "微博上有人提到："),
        ]
        for source, target in replacements:
            summary = summary.replace(source, target)
        summary = re.sub(r"第\s*(\d+)\s*天开始了。", r"第\1天开头的那阵子，", summary)
        summary = re.sub(r"你在[^和]{0,12}和玩家聊过“", "和玩家聊过“", summary)
        summary = re.sub(r"刚|刚刚|这一轮", "", summary)
        summary = re.sub(r"\s+", "", summary)
        summary = summary.strip("，。 ")
        summary = summary.replace("。。", "。")
        if len(summary) > 48:
            summary = summary[:46].rstrip("，。 ") + "…"
        if not summary.endswith(("。", "！", "？")):
            summary += "。"
        return summary

    def _extract_market_memory_info(self, text: str) -> dict[str, object] | None:
        match = re.match(
            r"^今天一早大家还在念叨：大盘(?P<tone>承压|走强|震荡)，指数收在(?P<close>\d+(?:\.\d+)?)，昨日日内(?P<change>[+-]\d+(?:\.\d+)?)%。$",
            text.strip(),
        )
        if not match:
            return None
        return {
            "tone": match.group("tone"),
            "close": float(match.group("close")),
            "change": float(match.group("change")),
        }

    def _merge_long_term_memories(self, memories: list[MemoryEntry]) -> list[MemoryEntry]:
        merged: list[MemoryEntry] = []
        market_memories: list[tuple[MemoryEntry, dict[str, object]]] = []
        for memory in memories:
            info = self._extract_market_memory_info(memory.text)
            if info is None:
                merged.append(memory)
                continue
            market_memories.append((memory, info))
        if market_memories:
            latest_memory, latest_info = market_memories[0]
            tones = [str(info["tone"]) for _, info in market_memories]
            unique_tones = list(dict.fromkeys(tones))
            if len(market_memories) == 1:
                merged.insert(0, latest_memory)
            else:
                if len(unique_tones) == 1:
                    tone_phrase = {
                        "承压": "这几天盘面一直偏弱",
                        "走强": "这几天盘面一直偏强",
                        "震荡": "这几天盘面一直在来回晃",
                    }.get(unique_tones[0], "这几天盘面一直在变")
                else:
                    tone_phrase = "这几天盘面来回拉扯"
                summary = (
                    f"{tone_phrase}，大家嘴上一直在念叨大盘；"
                    f"最近一次收在{latest_info['close']:.2f}，单日{latest_info['change']:+.2f}%。"
                )
                merged.insert(
                    0,
                    MemoryEntry(
                        text=summary,
                        day=latest_memory.day,
                        time_slot=latest_memory.time_slot,
                        importance=max(memory.importance for memory, _ in market_memories),
                    ),
                )
        merged.sort(key=lambda item: (item.day, SLOT_SEQUENCE.index(item.time_slot), item.importance), reverse=True)
        return merged[:4]

    def _remember_long_term(self, agent: Agent, text: str, importance: int) -> None:
        if importance < 3:
            return
        summary = self._summarize_long_term_memory(text)
        signature = self._memory_signature(summary)
        existing = agent.long_term_memory or []
        if any(self._memory_signature(memory.text) == signature for memory in existing[:4]):
            return
        todays_long_term = [memory for memory in existing if memory.day == self.state.day]
        if importance < 4 and len(todays_long_term) >= 1:
            return
        if importance >= 4 and len(todays_long_term) >= 2:
            return
        entry = MemoryEntry(text=summary, day=self.state.day, time_slot=self.state.time_slot, importance=importance)
        agent.long_term_memory.insert(0, entry)
        agent.long_term_memory = self._merge_long_term_memories(agent.long_term_memory[:6])

    def _cooldown_for(self, owner: Agent | object, target_id: str) -> int:
        return int(getattr(owner, "relation_cooldowns", {}).get(target_id, 0))

    def _set_relation_cooldown(self, left: Agent | object, right_id: str, turns: int) -> None:
        if not hasattr(left, "relation_cooldowns") or getattr(left, "relation_cooldowns") is None:
            setattr(left, "relation_cooldowns", {})
        getattr(left, "relation_cooldowns")[right_id] = max(0, turns)

    def _scaled_relation_delta(self, current: int, delta: int, cooldown: int, observer: bool = False) -> int:
        if delta == 0:
            return 0
        scaled = float(delta)
        if observer:
            scaled *= 0.6
        if cooldown > 0:
            scaled *= max(0.35, 1.0 - cooldown * 0.24)
        if delta > 0 and current >= 70:
            scaled *= 0.42
        elif delta > 0 and current >= 45:
            scaled *= 0.68
        elif delta < 0 and current <= -55:
            scaled *= 0.45
        elif delta < 0 and current <= -28:
            scaled *= 0.72
        if delta > 0 and current < -25:
            scaled *= 1.18
        if delta < 0 and current > 55:
            scaled *= 1.12
        if abs(current) >= 86 and delta * current > 0:
            scaled *= 0.28
        rounded = int(round(scaled))
        if rounded == 0:
            return 1 if delta > 0 and current < 88 else -1 if delta < 0 and current > -88 else 0
        return rounded

    def _apply_relation_rebound(self) -> None:
        processed: set[tuple[str, str]] = set()
        for first in self.state.agents:
            for second in self.state.agents:
                if first.id == second.id:
                    continue
                pair = tuple(sorted((first.id, second.id)))
                if pair in processed:
                    continue
                processed.add(pair)
                left = first.relations.get(second.id, 0)
                right = second.relations.get(first.id, 0)
                new_left = self._relation_rebound_value(left)
                new_right = self._relation_rebound_value(right)
                first.relations[second.id] = new_left
                second.relations[first.id] = new_right
        for agent in self.state.agents:
            current = agent.relations.get("player", 0)
            adjusted = self._relation_rebound_value(current, player_link=True)
            agent.relations["player"] = adjusted
            self.state.player.social_links[agent.id] = adjusted

    def _relation_rebound_value(self, value: int, player_link: bool = False) -> int:
        if value >= 82:
            value -= 4
        elif value >= 68:
            value -= 2
        elif value <= -70:
            value += 4
        elif value <= -42:
            value += 2
        if player_link and value >= 72:
            value -= 1
        return max(-100, min(100, value))

    def _tick_relation_cooldowns(self) -> None:
        def decay(mapping: dict[str, int]) -> dict[str, int]:
            return {key: value - 1 for key, value in mapping.items() if value - 1 > 0}

        self.state.player.relation_cooldowns = decay(self.state.player.relation_cooldowns or {})
        for agent in self.state.agents:
            agent.relation_cooldowns = decay(agent.relation_cooldowns or {})

    def _normalize_extreme_relations_on_upgrade(self) -> None:
        for agent in self.state.agents:
            for target_id, value in list((agent.relations or {}).items()):
                if value >= 92:
                    agent.relations[target_id] = 78
                elif value <= -92:
                    agent.relations[target_id] = -74
            current = agent.relations.get("player", self.state.player.social_links.get(agent.id, 0))
            if current >= 92:
                current = 80
            elif current <= -92:
                current = -72
            agent.relations["player"] = current
            self.state.player.social_links[agent.id] = current

    def _observer_dialogue_intensity(self, agent: Agent) -> float:
        relation = agent.relations.get("player", 0)
        if relation >= 70:
            return 0.12
        if relation >= 45:
            return 0.18
        return 0.24

    def _apply_player_intervention_cost(self, reason: str, amount: int = 1, reward: bool = False) -> int:
        delta = amount if reward else -amount
        before = self.state.player.reputation_score
        self.state.player.reputation_score = self._bounded(self.state.player.reputation_score + delta)
        after = self.state.player.reputation_score
        actual = after - before
        if actual != 0:
            self.state.player.daily_actions.append(f"intervene:{reason}:{actual}")
        return actual

    def _adjust_relation(self, first: Agent, second: Agent, delta: int, reason: str) -> None:
        previous = first.relations.get(second.id, 0)
        cooldown = max(self._cooldown_for(first, second.id), self._cooldown_for(second, first.id))
        effective_delta = self._scaled_relation_delta(previous, delta, cooldown)
        updated = max(-100, min(100, previous + effective_delta))
        first.relations[second.id] = updated
        second_previous = second.relations.get(first.id, 0)
        second_effective = self._scaled_relation_delta(second_previous, delta, cooldown)
        second.relations[first.id] = max(-100, min(100, second_previous + second_effective))
        self._set_relation_cooldown(first, second.id, 2 if abs(effective_delta) >= 3 else 1)
        self._set_relation_cooldown(second, first.id, 2 if abs(second_effective) >= 3 else 1)
        threshold_labels = [
            (75, "关系有点暧昧了"),
            (55, "默契明显升高"),
            (35, "开始熟悉彼此"),
            (-25, "气氛变得有些紧张"),
        ]
        for threshold, label in threshold_labels:
            crossed_up = previous < threshold <= updated and threshold > 0
            crossed_down = previous > threshold >= updated and threshold < 0
            if crossed_up or crossed_down:
                self._remember(first, f"和 {second.name} 的关系变化了：{label}。原因是{reason}", 3, long_term=True)
                self._remember(second, f"和 {first.name} 的关系变化了：{label}。原因是{reason}", 3, long_term=True)
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=f"{first.name} 与 {second.name} 的关系发生变化",
                        summary=f"因为{reason}，他们现在更像“{label.replace('了', '')}”。",
                        slot=self.state.time_slot,
                        category="general",
                    ),
                )
                self.state.events = self.state.events[:8]
                break

    def _adjust_player_relation(self, agent: Agent, delta: int, reason: str, observer: bool = False) -> int:
        previous = agent.relations.get("player", 0)
        cooldown = max(self._cooldown_for(agent, "player"), self._cooldown_for(self.state.player, agent.id))
        reputation_scale = 0.62 + (self.state.player.reputation_score / 140)
        scaled = int(round(delta * reputation_scale))
        effective_delta = self._scaled_relation_delta(previous, scaled, cooldown, observer=observer)
        updated = max(-100, min(100, previous + effective_delta))
        agent.relations["player"] = updated
        self.state.player.social_links[agent.id] = updated
        self._set_relation_cooldown(agent, "player", 2 if abs(effective_delta) >= 3 else 1)
        self._set_relation_cooldown(self.state.player, agent.id, 2 if abs(effective_delta) >= 3 else 1)
        if previous < 40 <= updated:
            self._remember(agent, f"你对玩家的好感明显提高了。原因是{reason}", 3, long_term=True)
        if previous < 65 <= updated:
            self._remember(agent, f"你开始期待下一次和玩家单独聊天。", 4, long_term=True)
        return effective_delta

    def _apply_player_dialogue_impact(self, agent: Agent, dialogue: DialogueOutcome, intensity: float = 1.0) -> tuple[int, dict[str, int]]:
        player_text = " ".join(filter(None, [dialogue.player_text, dialogue.topic]))
        support = self._keyword_hits(player_text, ["谢谢", "辛苦", "理解", "支持", "一起", "慢慢", "相信", "喜欢", "麻烦你", "拜托"])
        pressure = self._keyword_hits(player_text, ["不对", "问题", "bug", "风险", "怀疑", "分歧", "卡住", "着急", "质疑", "别扯", "别废话"])
        hostility = self._keyword_hits(player_text, ["骂", "滚", "闭嘴", "傻", "蠢", "烦", "恶心", "讨厌", "废物", "有病", "懒得"])
        dominance = self._keyword_hits(player_text, ["直接", "立刻", "马上", "给我", "必须", "少废话"])
        inquiry = self._keyword_hits(player_text, ["为什么", "怎么", "验证", "证据", "数据", "推理", "线索", "实验"])
        resonance = self._persona_resonance(agent, player_text)
        constructive = self._keyword_hits(player_text, ["一起看", "梳理", "帮我", "分析", "讨论", "复盘", "解释"])
        relation_delta = 1 + resonance + support + constructive + (1 if inquiry > 0 and hostility == 0 else 0) - pressure * 2 - hostility * 4 - dominance
        relation_delta = max(-12, min(10, relation_delta))
        raw_changes = {
            "mood": max(-9, min(8, resonance + support + constructive - pressure * 2 - hostility * 3 - dominance)),
            "stress": max(-6, min(9, pressure * 2 + hostility * 3 + dominance - support - (1 if constructive > 0 else 0))),
            "focus": max(-5, min(6, inquiry + (1 if agent.persona in {"rational", "engineering"} else 0) - hostility - (1 if support > inquiry + 1 else 0))),
            "energy": max(-4, min(3, -1 + support + constructive - pressure - hostility * 2)),
            "curiosity": max(-4, min(7, resonance + inquiry + constructive - hostility)),
            "geo_reasoning_skill": 1 if self._is_geoai_topic(player_text) and hostility == 0 else 0,
        }
        if intensity != 1.0:
            relation_delta = int(round(relation_delta * intensity))
            changes = {
                "mood": int(round(raw_changes["mood"] * max(0.25, intensity))),
                "stress": int(round(raw_changes["stress"] * max(0.25, intensity))),
                "focus": int(round(raw_changes["focus"] * max(0.25, intensity))),
                "energy": int(round(raw_changes["energy"] * max(0.2, intensity * 0.8))),
                "curiosity": int(round(raw_changes["curiosity"] * max(0.25, intensity))),
                "geo_reasoning_skill": 0 if intensity < 0.6 else raw_changes["geo_reasoning_skill"],
            }
        else:
            changes = raw_changes
        self._shift_agent_state(agent, **changes)
        projected_relation = max(-100, min(100, agent.relations.get("player", 0) + relation_delta))
        topic = dialogue.topic or "刚才的话题"
        agent.current_activity = f"刚和你聊完“{topic}”，还在消化这轮交流。"
        agent.status_summary = self._build_status_summary(agent, projected_relation, topic, from_player=True)
        agent.last_interaction = f"刚在{ROOM_LABELS.get(agent.current_location, agent.current_location)}和你聊了“{topic}”。"
        return relation_delta, changes

    def _extract_money_amount(self, text: str) -> int | None:
        match = re.search(r"(\d+)\s*(?:美元|刀|块|元|美金)", text)
        if match:
            return max(1, int(match.group(1)))
        return None

    def _extract_interest_rate(self, text: str) -> int | None:
        match = re.search(r"(\d+)\s*(?:%|利息|点利)", text)
        if match:
            return max(1, min(25, int(match.group(1))))
        return None

    def _player_money_intent(self, text: str) -> tuple[str | None, int | None]:
        normalized = text.replace(" ", "")
        amount = self._extract_money_amount(normalized)
        if any(token in normalized for token in ["借给你", "借你", "给你", "转你", "赞助你", "报销你", "请你", "我来付", "我付"]):
            return ("give", amount)
        if any(token in normalized for token in ["借给我", "借我", "给我", "转我", "赞助我", "报销我", "请我", "帮我付"]):
            return ("ask", amount)
        return (None, amount)

    def _ambient_money_exchange(
        self,
        requester: Agent,
        donor: Agent,
        request_line: str,
        response_line: str,
        topic: str,
        mood: str,
        gray_plan: dict[str, object] | None = None,
    ) -> dict[str, object] | None:
        if gray_plan and requester.id == str(gray_plan.get("requester_id")) and donor.id == str(gray_plan.get("donor_id")):
            gray_result = self._execute_gray_trade_plan(requester, donor, topic, mood, gray_plan)
            if gray_result is not None:
                return gray_result
        gray_request_tokens = [
            "私下",
            "别挂到账",
            "别摆到台面",
            "灰色",
            "非正式",
            "不走正式挂牌",
            "不挂牌",
            "灰市规矩",
            "按灰市规矩",
            "钥匙和租约",
            "塞给你",
        ]
        gray_offer_tokens = [
            "私下给你",
            "先别挂账",
            "这笔先不摆到台面",
            "非正式资源交换",
            "别往外说",
            "我给",
            "我先给",
            "别跟别人说",
            "别跟别人提",
            "别让别人知道",
            "按灰市规矩",
            "不走正式挂牌",
            "不挂牌",
        ]
        explicit_gray_request = any(token in request_line for token in gray_request_tokens)
        explicit_gray_offer = any(token in response_line for token in gray_offer_tokens)
        if not explicit_gray_request and any(token in request_line for token in ["空屋", "租约", "钥匙"]) and any(
            token in request_line for token in ["不走正式挂牌", "不挂牌", "灰市规矩", "塞给你"]
        ):
            explicit_gray_request = True
        if not explicit_gray_offer and self._extract_money_amount(f"{request_line}{response_line}") and any(
            token in response_line for token in ["我给", "我出", "我来给", "先给你", "可以，我给", "行，$"]
        ):
            explicit_gray_offer = True
        if explicit_gray_request and explicit_gray_offer and donor.cash > 0:
            amount = self._extract_money_amount(f"{request_line}{response_line}") or max(5, requester.money_urgency // 18)
            relation = (donor.relations.get(requester.id, 0) + requester.relations.get(donor.id, 0)) / 2
            joined = f"{request_line} {response_line} {topic}"
            strong_gray_signal = sum(
                1
                for token in [
                    "不走正式挂牌",
                    "不挂牌",
                    "灰市规矩",
                    "按灰市规矩",
                    "钥匙和租约",
                    "钥匙",
                    "租约",
                    "塞给你",
                    "账外",
                    "回扣",
                    "私货",
                    "拉高出货",
                    "灰盘",
                ]
                if token in joined
            )
            judgement = self._loan_judgement_score(donor, requester, amount) + int(relation // 3) + strong_gray_signal * 5
            if mood == "tense":
                judgement -= 4
            relation_floor = 8 if strong_gray_signal >= 2 else 18
            judgement_floor = 20 if strong_gray_signal >= 2 else 34
            if judgement < judgement_floor or relation < relation_floor:
                return None
            amount = min(amount, donor.cash)
            if amount <= 0:
                return None
            gray_type = self._infer_explicit_gray_trade_type(requester, donor, request_line, response_line, topic)
            donor.cash -= amount
            requester.cash += amount
            self._remember(requester, f"{donor.name} 刚私下塞给你 ${amount}，算一笔不公开的资源交换。", 2)
            self._remember(donor, f"你刚私下给了 {requester.name} ${amount}，这笔没有摆到公开台面上。", 2)
            self._adjust_relation(requester, donor, 1, f"围绕“{topic}”完成了一次不公开的资源交换。")
            asset_name = self._gray_case_label(gray_type)
            self._append_finance_record(
                actor_id=requester.id,
                actor_name=requester.name,
                category="gray",
                action="receive",
                summary=f"{requester.name} 通过“{asset_name}”从 {donor.name} 手里拿到 ${amount}。",
                amount=amount,
                asset_name=asset_name,
                counterparty=donor.name,
            )
            self._append_finance_record(
                actor_id=donor.id,
                actor_name=donor.name,
                category="gray",
                action="pay",
                summary=f"{donor.name} 在“{asset_name}”里把 ${amount} 递给了 {requester.name}。",
                amount=-amount,
                asset_name=asset_name,
                counterparty=requester.name,
            )
            self._register_gray_case(
                requester,
                donor,
                topic,
                {
                    "type": gray_type,
                    "severity": 2 if gray_type in {"rent_rigging", "pump_dump"} else 1,
                    "note": f"{requester.name} 和 {donor.name} 私下围着“{self._humanize_dialogue_topic(topic)}”做了一笔见不得光的{self._gray_case_label(gray_type)}。",
                },
                amount,
            )
            self._log(
                "agent_gray_trade",
                trade={"from": donor.id, "to": requester.id, "amount": amount, "topic": topic},
            )
            return {
                "note": f"{donor.name} 和 {requester.name} 做了一笔非正式{self._gray_case_label(gray_type)} ${amount}",
                "interest_rate": None,
                "gray_trade": True,
                "gray_trade_type": gray_type,
                "gray_trade_severity": 2 if gray_type in {"rent_rigging", "pump_dump"} else 1,
            }
        explicit_request = any(token in request_line for token in ["借我", "能不能借", "先垫", "能不能报销", "赞助我", "请我", "能不能支一点"])
        explicit_offer = any(token in response_line for token in ["借你", "我先垫", "我报销", "我请", "我来出", "行，我给你"])
        if not explicit_request or not explicit_offer or donor.cash <= 0:
            return None
        requested_amount = self._extract_money_amount(f"{request_line}{response_line}") or max(4, requester.money_urgency // 20)
        interest_rate = self._extract_interest_rate(request_line) or self._proposed_interest_rate(requester)
        amount_due = requested_amount + max(1, round(requested_amount * interest_rate / 100))
        judgement = self._loan_judgement_score(donor, requester, amount_due)
        if mood == "warm":
            judgement += 6
        if mood == "tense":
            judgement -= 10
        if judgement < 28:
            return None
        amount = min(requested_amount, donor.cash)
        if amount <= 0:
            return None
        donor.cash -= amount
        requester.cash += amount
        loan = self._create_loan(donor, requester, amount, interest_rate, topic)
        self._remember(requester, f"{donor.name} 刚答应借你 ${amount}，明天还，利息 {interest_rate}%。", 2)
        self._remember(donor, f"你刚答应借给 {requester.name} ${amount}，明天收回，利息 {interest_rate}%。", 2)
        self._adjust_relation(requester, donor, 2, f"围绕“{topic}”达成了一笔借款。")
        self._log(
            "agent_loan_created",
            loan={"id": loan.id, "lender": donor.id, "borrower": requester.id, "principal": amount, "interest_rate": interest_rate, "due_day": loan.due_day},
            topic=topic,
        )
        return {
            "note": f"{donor.name} 借给了 {requester.name} ${amount}，明天按 {interest_rate}% 收回",
            "interest_rate": interest_rate,
            "gray_trade": False,
        }

    def _gray_trade_catalog(
        self,
        requester: Agent,
        donor: Agent,
        topic: str,
        mood: str,
        first_desire: str,
        second_desire: str,
    ) -> list[dict[str, object]]:
        pair_relation = (donor.relations.get(requester.id, 0) + requester.relations.get(donor.id, 0)) / 2
        amount = max(4, min(18, max(requester.money_urgency, donor.money_urgency, 36) // 12))
        options: list[dict[str, object]] = []
        if {first_desire, second_desire} & {"money", "opportunity"}:
            options.append(
                {
                    "type": "insider_tip_sale",
                    "severity": 2,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount,
                    "judgement_floor": 26,
                    "line_a": f"这条盘前风向我可以提前告诉你，但别往外传，你私下给我 {amount} 美元，我把具体时点递给你。",
                    "line_b": f"行，这笔我私下给你 ${amount}，你把那条内部风向先放给我。",
                    "note": f"{donor.name} 花 ${amount} 向 {requester.name} 买了一条内幕消息。",
                    "memory_requester": f"你刚把一条未公开的盘前消息私下卖给了 {donor.name}，拿到 ${amount}。",
                    "memory_donor": f"你刚私下付给 {requester.name} ${amount}，换来一条内部风向。",
                    "relation_delta": 1,
                    "cash_delta": amount,
                    "requester_credit": 4,
                    "donor_credit": 2,
                    "lab_reputation": -1,
                    "market_sentiment": 1,
                    "event_title": "有人私下倒卖内幕消息",
                    "event_summary": f"{requester.name} 把一条没摆上台面的风向卖给了 {donor.name}。",
                }
            )
        if requester.credit_score <= 62 or requester.money_urgency >= 78:
            options.append(
                {
                    "type": "fake_reimbursement",
                    "severity": 2,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount,
                    "judgement_floor": 22,
                    "line_a": f"你先给我 {amount} 美元，我把这笔包装成设备维护报销，过两天我补你一份假的凭据。",
                    "line_b": f"好，这笔我先垫给你 ${amount}，但你答应的那份报销凭据别拖。",
                    "note": f"{requester.name} 用假报销说辞从 {donor.name} 手里套走了 ${amount}。",
                    "memory_requester": f"你刚拿“设备维护报销”的说法从 {donor.name} 手里换到了 ${amount}。",
                    "memory_donor": f"你刚给了 {requester.name} ${amount}，这笔说是要走假报销单据。",
                    "relation_delta": -1,
                    "cash_delta": amount,
                    "requester_credit": 5,
                    "donor_credit": 3,
                    "lab_reputation": -2,
                    "stress_donor": 2,
                    "event_title": "有人打起了假报销的主意",
                    "event_summary": f"{requester.name} 和 {donor.name} 私下谈了一笔带着假单据味道的款子。",
                }
            )
        if pair_relation >= 8 and mood != "warm":
            options.append(
                {
                    "type": "data_theft",
                    "severity": 3,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount + 2,
                    "judgement_floor": 20,
                    "line_a": f"服务器里那份原始数据我今晚能偷拷一份给你，你拿 {amount + 2} 美元来换，别在明面上提我。",
                    "line_b": f"行，${amount + 2} 我给，你把那份原始数据拷出来，但名字别留下。",
                    "note": f"{requester.name} 私拷了一份原始数据给 {donor.name}，换走了 ${amount + 2}。",
                    "memory_requester": f"你刚答应把一份原始数据私拷给 {donor.name}，换到 ${amount + 2}。",
                    "memory_donor": f"你刚花 ${amount + 2} 从 {requester.name} 那里买到一份未公开原始数据。",
                    "relation_delta": 1,
                    "cash_delta": amount + 2,
                    "requester_credit": 7,
                    "donor_credit": 4,
                    "lab_reputation": -3,
                    "market_sentiment": -1,
                    "event_title": "原始数据被私下挪走",
                    "event_summary": f"{requester.name} 把一份没公开的数据私下递给了 {donor.name}。",
                }
            )
        if pair_relation <= 4 or mood == "tense":
            options.append(
                {
                    "type": "blackmail",
                    "severity": 4,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount + 3,
                    "judgement_floor": 8,
                    "line_a": f"你要么现在给我 {amount + 3} 美元封口，要么我就把你那笔逾期和私账往外抖。",
                    "line_b": f"别把这事往外传，我给你 ${amount + 3}，但你最好今天就闭嘴。",
                    "note": f"{requester.name} 向 {donor.name} 收了一笔 ${amount + 3} 的封口费。",
                    "memory_requester": f"你刚逼着 {donor.name} 给了你 ${amount + 3} 封口费。",
                    "memory_donor": f"你刚被 {requester.name} 逼着交了 ${amount + 3} 封口费，这事很伤脸。",
                    "relation_delta": -6,
                    "cash_delta": amount + 3,
                    "requester_credit": 9,
                    "donor_credit": 1,
                    "lab_reputation": -4,
                    "stress_requester": 2,
                    "stress_donor": 8,
                    "mood_override": "tense",
                    "event_title": "实验室里出现封口费",
                    "event_summary": f"{requester.name} 拿着 {donor.name} 的把柄要钱，气氛已经很脏。",
                }
            )
        if donor.cash >= amount + 2 and requester.cash <= 22:
            options.append(
                {
                    "type": "fraud",
                    "severity": 3,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount,
                    "judgement_floor": 18,
                    "line_a": f"你先给我 {amount} 美元，我今晚就替你把那条关系打通，明早前肯定有结果。",
                    "line_b": f"行，这 ${amount} 我先给你，你别让我白等到明早。",
                    "note": f"{requester.name} 以“走关系”为名从 {donor.name} 那里套走了 ${amount}。",
                    "memory_requester": f"你刚用“替人走关系”的说法从 {donor.name} 手里拿到了 ${amount}。",
                    "memory_donor": f"你刚给了 {requester.name} ${amount}，想让他替你把一条关系打通。",
                    "relation_delta": -3,
                    "cash_delta": amount,
                    "requester_credit": 8,
                    "donor_credit": 2,
                    "lab_reputation": -2,
                    "stress_donor": 4,
                    "event_title": "有人用模糊承诺骗了一笔钱",
                    "event_summary": f"{requester.name} 用一套很虚的承诺从 {donor.name} 那里拿走了钱。",
                }
            )
        if requester.materialism >= 58 or donor.materialism >= 58:
            options.append(
                {
                    "type": "counterfeit_goods",
                    "severity": 2,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount + 1,
                    "judgement_floor": 20,
                    "line_a": f"这批货看起来跟真的差不多，你私下给我 {amount + 1} 美元，我今晚就把箱子塞到你屋后。",
                    "line_b": f"行，${amount + 1} 我出，但别让我明天一开箱就翻车。",
                    "note": f"{requester.name} 私下向 {donor.name} 倒了一批来路不明的货，拿走了 ${amount + 1}。",
                    "memory_requester": f"你刚把一批来路不明的货私下倒给了 {donor.name}，拿到 ${amount + 1}。",
                    "memory_donor": f"你刚花 ${amount + 1} 从 {requester.name} 手里接了一批不太干净的货。",
                    "relation_delta": -1,
                    "cash_delta": amount + 1,
                    "requester_credit": 5,
                    "donor_credit": 3,
                    "lab_reputation": -2,
                    "event_title": "实验室里开始有人倒卖假货",
                    "event_summary": f"{requester.name} 把一批来路不明的货私下塞给了 {donor.name}。",
                }
            )
        if requester.owned_property_ids and donor.cash >= amount + 4:
            options.append(
                {
                    "type": "rent_rigging",
                    "severity": 3,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount + 4,
                    "judgement_floor": 18,
                    "line_a": f"我手里那间空屋可以不走正式挂牌，{amount + 4} 美元你先给我，我把钥匙和租约都按灰市规矩塞给你。",
                    "line_b": f"行，${amount + 4} 我给，但你别明天又说这屋子还有别人盯着。",
                    "note": f"{requester.name} 把一间没走正式流程的屋子私下转给了 {donor.name}，拿走 ${amount + 4}。",
                    "memory_requester": f"你刚把一间没走正式流程的屋子私下转给了 {donor.name}。",
                    "memory_donor": f"你刚花 ${amount + 4} 从 {requester.name} 手里接了一间不太干净的屋子。",
                    "relation_delta": -2,
                    "cash_delta": amount + 4,
                    "requester_credit": 6,
                    "donor_credit": 4,
                    "lab_reputation": -2,
                    "event_title": "有人私下转租了一处房产",
                    "event_summary": f"{requester.name} 没走正式挂牌，就把一处屋子私下递给了 {donor.name}。",
                }
            )
        if requester.current_location == "compute" or donor.current_location == "compute":
            options.append(
                {
                    "type": "wage_kickback",
                    "severity": 2,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount,
                    "judgement_floor": 16,
                    "line_a": f"这轮公司那边的活我能给你多塞一点，你私下回我 {amount} 美元回扣，这事谁也别提。",
                    "line_b": f"行，这 ${amount} 我回给你，你把那轮轻松又赚钱的活先留给我。",
                    "note": f"{requester.name} 以“工作回扣”为名从 {donor.name} 手里拿了 ${amount}。",
                    "memory_requester": f"你刚借着公司活口从 {donor.name} 手里拿了一笔回扣。",
                    "memory_donor": f"你刚私下回给 {requester.name} ${amount}，想换一轮更顺的公司活。",
                    "relation_delta": -1,
                    "cash_delta": amount,
                    "requester_credit": 4,
                    "donor_credit": 2,
                    "lab_reputation": -1,
                    "event_title": "公司活里开始冒出回扣",
                    "event_summary": f"{requester.name} 和 {donor.name} 为了公司那边的活口私下递了一笔回扣。",
                }
            )
            options.append(
                {
                    "type": "dispatch_rigging",
                    "severity": 2,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount + 1,
                    "judgement_floor": 14,
                    "line_a": f"下轮公司那边的轻活我能先塞给你，但你得先回我 {amount + 1} 美元，别让别人知道派单往你这边偏了。",
                    "line_b": f"行，${amount + 1} 我回给你，你把那轮轻松又能赚的活先留给我。",
                    "note": f"{requester.name} 和 {donor.name} 私下做了一笔派单倾斜交易，金额 ${amount + 1}。",
                    "memory_requester": f"你刚通过偏派公司活，从 {donor.name} 手里拿到 ${amount + 1}。",
                    "memory_donor": f"你刚私下回给 {requester.name} ${amount + 1}，想让下一轮公司活向你倾斜。",
                    "relation_delta": -2,
                    "cash_delta": amount + 1,
                    "requester_credit": 5,
                    "donor_credit": 3,
                    "lab_reputation": -2,
                    "event_title": "公司内部派单开始不均",
                    "event_summary": f"{requester.name} 和 {donor.name} 围着公司派单私下递了一笔钱。",
                }
            )
            options.append(
                {
                    "type": "wage_laundering",
                    "severity": 3,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount + 2,
                    "judgement_floor": 18,
                    "line_a": f"这笔钱我给你挂成公司工资名义走，你先把 ${amount + 2} 私下递过来，台账上只写加班补贴。",
                    "line_b": f"行，${amount + 2} 我先递给你，你把它伪装成工资补贴走掉。",
                    "note": f"{requester.name} 和 {donor.name} 借工资名义洗了一笔 ${amount + 2}。",
                    "memory_requester": f"你刚借工资补贴名义替 {donor.name} 洗了一笔 ${amount + 2}。",
                    "memory_donor": f"你刚把 ${amount + 2} 通过工资补贴的名义洗了一层。",
                    "relation_delta": -2,
                    "cash_delta": amount + 2,
                    "requester_credit": 8,
                    "donor_credit": 5,
                    "lab_reputation": -3,
                    "event_title": "有人借工资名义洗钱",
                    "event_summary": f"{requester.name} 和 {donor.name} 把一笔钱伪装成工资补贴走账。",
                }
            )
            options.append(
                {
                    "type": "labor_for_insider",
                    "severity": 2,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount,
                    "judgement_floor": 16,
                    "line_a": f"你替我把今晚那轮公司活顶掉，我就把明天那条内部风向先给你，钱我们先不明着算。",
                    "line_b": f"行，这轮活我替你扛，你把那条内部风向先递给我。",
                    "note": f"{requester.name} 和 {donor.name} 用劳动换了一条内部消息。",
                    "memory_requester": f"你刚拿内部风向和 {donor.name} 交换了一轮劳动。",
                    "memory_donor": f"你刚替 {requester.name} 顶掉一轮活，换来一条内部风向。",
                    "relation_delta": 1,
                    "cash_delta": 0,
                    "requester_credit": 4,
                    "donor_credit": 2,
                    "lab_reputation": -1,
                    "event_title": "有人用劳动换内部消息",
                    "event_summary": f"{requester.name} 和 {donor.name} 拿劳动和内部风向私下做了置换。",
                }
            )
            options.append(
                {
                    "type": "wage_arrears",
                    "severity": 3,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount + 1,
                    "judgement_floor": 12,
                    "line_a": f"我先把你那轮工资压两天，你现在把 ${amount + 1} 回给我，后面我再想法子帮你补回来。",
                    "line_b": f"先别压太狠，我把 ${amount + 1} 回给你，但你得记着这笔工资还欠着。",
                    "note": f"{requester.name} 以拖工资为由从 {donor.name} 身上榨出 ${amount + 1}。",
                    "memory_requester": f"你刚借拖工资的口子，从 {donor.name} 那里挤出 ${amount + 1}。",
                    "memory_donor": f"你刚被 {requester.name} 借着拖工资的名义压走 ${amount + 1}。",
                    "relation_delta": -4,
                    "cash_delta": amount + 1,
                    "requester_credit": 7,
                    "donor_credit": 4,
                    "lab_reputation": -3,
                    "stress_donor": 6,
                    "event_title": "工资拖欠开始在公司活里蔓延",
                    "event_summary": f"{requester.name} 借着公司工资结算拖了 {donor.name} 一笔钱。",
                }
            )
        if requester.money_urgency >= 72 and donor.cash >= amount + 2:
            options.append(
                {
                    "type": "pump_dump",
                    "severity": 3,
                    "requester_id": requester.id,
                    "donor_id": donor.id,
                    "amount": amount + 2,
                    "judgement_floor": 22,
                    "line_a": f"明天开盘你就跟着我把那只票往上顶，先给我 {amount + 2} 美元，我带你一起拉高出货。",
                    "line_b": f"行，${amount + 2} 我先给，你别让我最后接在高位。",
                    "note": f"{requester.name} 拉着 {donor.name} 做了一笔拉高出货的灰盘，先拿走 ${amount + 2}。",
                    "memory_requester": f"你刚说动 {donor.name} 陪你做一笔拉高出货，先拿到 ${amount + 2}。",
                    "memory_donor": f"你刚给了 {requester.name} ${amount + 2}，准备一起去拉一只票的灰盘。",
                    "relation_delta": -2,
                    "cash_delta": amount + 2,
                    "requester_credit": 7,
                    "donor_credit": 3,
                    "lab_reputation": -3,
                    "market_sentiment": -2,
                    "event_title": "有人想在盘前做拉高出货",
                    "event_summary": f"{requester.name} 拉着 {donor.name} 想做一笔先拉后砸的盘前灰盘。",
                }
            )
        return options

    def _execute_gray_trade_plan(
        self,
        requester: Agent,
        donor: Agent,
        topic: str,
        mood: str,
        plan: dict[str, object],
    ) -> dict[str, object] | None:
        amount = min(int(plan.get("amount", 0) or 0), donor.cash)
        if amount <= 0:
            return None
        relation = (donor.relations.get(requester.id, 0) + requester.relations.get(donor.id, 0)) / 2
        judgement = self._loan_judgement_score(donor, requester, amount) + int(relation // 4)
        judgement += 6 if mood == "warm" else 0
        judgement -= 6 if mood == "tense" else 0
        if plan.get("type") == "blackmail":
            judgement += 18
        if judgement < int(plan.get("judgement_floor", 24)):
            return None
        donor.cash -= amount
        requester.cash += amount
        requester.credit_score = max(0, requester.credit_score - int(plan.get("requester_credit", 3)))
        donor.credit_score = max(0, donor.credit_score - int(plan.get("donor_credit", 1)))
        self.state.lab.reputation = self._bounded(self.state.lab.reputation - int(plan.get("lab_reputation", 1)))
        self.state.market.sentiment = self._bounded(self.state.market.sentiment + int(plan.get("market_sentiment", 0)))
        if plan.get("stress_requester"):
            self._shift_agent_state(requester, stress=int(plan["stress_requester"]))
        if plan.get("stress_donor"):
            self._shift_agent_state(donor, stress=int(plan["stress_donor"]))
        relation_delta = int(plan.get("relation_delta", -1))
        self._adjust_relation(requester, donor, relation_delta, f"围绕“{topic}”做了一笔地下交易：{plan.get('type')}")
        self._remember(requester, str(plan.get("memory_requester") or f"你刚完成了一笔灰色交易，拿到 ${amount}。"), 3, long_term=True)
        self._remember(donor, str(plan.get("memory_donor") or f"你刚在一笔灰色交易里付出 ${amount}。"), 3, long_term=True)
        requester.last_interaction = f"刚和 {donor.name} 完成了一笔地下交易。"
        donor.last_interaction = f"刚被卷进和 {requester.name} 的地下交易。"
        asset_name = self._gray_case_label(str(plan.get("type") or "under_table_exchange"))
        self._append_finance_record(
            actor_id=requester.id,
            actor_name=requester.name,
            category="gray",
            action="receive",
            summary=f"{requester.name} 通过“{asset_name}”从 {donor.name} 手里拿到 ${amount}。",
            amount=amount,
            asset_name=asset_name,
            counterparty=donor.name,
        )
        self._append_finance_record(
            actor_id=donor.id,
            actor_name=donor.name,
            category="gray",
            action="pay",
            summary=f"{donor.name} 在“{asset_name}”里把 ${amount} 递给了 {requester.name}。",
            amount=-amount,
            asset_name=asset_name,
            counterparty=requester.name,
        )
        event_title = str(plan.get("event_title") or "实验室里冒出一笔地下交易")
        event_summary = str(plan.get("event_summary") or f"{requester.name} 和 {donor.name} 围绕“{topic}”搞了一笔见不得光的交换。")
        self.state.events.insert(
            0,
            build_internal_event(
                title=event_title,
                summary=event_summary,
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._log(
            "agent_gray_trade",
            trade={
                "from": donor.id,
                "to": requester.id,
                "amount": amount,
                "topic": topic,
                "type": plan.get("type"),
                "severity": plan.get("severity", 2),
            },
        )
        self._register_gray_case(requester, donor, topic, plan, amount)
        return {
            "note": str(plan.get("note") or f"{requester.name} 从 {donor.name} 手里搞到了一笔不干净的钱 ${amount}"),
            "interest_rate": None,
            "gray_trade": True,
            "gray_trade_type": str(plan.get("type") or "under_table_exchange"),
            "gray_trade_severity": int(plan.get("severity", 2)),
        }

    def _register_gray_case(
        self,
        requester: Agent,
        donor: Agent,
        topic: str,
        plan: dict[str, object],
        amount: int,
    ) -> None:
        exposure = min(96, 18 + int(plan.get("severity", 2)) * 16 + max(0, 40 - requester.credit_score) // 2)
        due_day = self.state.day + (1 if int(plan.get("severity", 2)) >= 3 else 2)
        case = GrayCase(
            id=f"gray-{uuid4().hex[:8]}",
            case_type=str(plan.get("type") or "under_table_exchange"),
            participants=[requester.id, donor.id],
            participant_names=[requester.name, donor.name],
            topic=topic,
            summary=str(plan.get("note") or f"{requester.name} 和 {donor.name} 刚做了一笔地下交易。"),
            amount=amount,
            severity=int(plan.get("severity", 2)),
            start_day=self.state.day,
            due_day=due_day,
            exposure_risk=exposure,
            status="active",
        )
        self.state.gray_cases.insert(0, case)
        self.state.gray_cases = self.state.gray_cases[:16]

    def _advance_gray_cases(self, daily_roll: bool = False) -> None:
        if not self.state.gray_cases:
            return
        active: list[GrayCase] = []
        for case in self.state.gray_cases:
            if case.status != "active":
                continue
            risk_bump = 10 if daily_roll else 4
            if self.state.weather == "drizzle":
                risk_bump += 2
            if self.state.market.sentiment <= -10:
                risk_bump += 2
            case.exposure_risk = min(100, case.exposure_risk + risk_bump)
            if case.due_day is not None and self.state.day >= case.due_day:
                case.exposure_risk = min(100, case.exposure_risk + 12)
                if self.random.random() < 0.34:
                    self._escalate_gray_case(case)
            exposure_roll = self.random.randint(1, 100)
            if exposure_roll <= case.exposure_risk:
                self._expose_gray_case(case)
                continue
            if daily_roll and case.severity <= 2 and self.state.day >= case.start_day + 2:
                case.status = "settled"
                self._settle_gray_case(case)
                continue
            active.append(case)
        archived = [case for case in self.state.gray_cases if case.status != "active"]
        self.state.gray_cases = (active + archived)[:16]

    def _settle_gray_case(self, case: GrayCase) -> None:
        self.state.lab.reputation = self._bounded(self.state.lab.reputation + 1)
        self.state.events.insert(
            0,
            build_internal_event(
                title="一笔地下交易暂时沉了下去",
                summary=f"{case.summary} 目前还没被捅到台面上，但知道的人并没有忘。",
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]

    def _escalate_gray_case(self, case: GrayCase) -> None:
        first = next((agent for agent in self.state.agents if agent.id == case.participants[0]), None)
        second = next((agent for agent in self.state.agents if agent.id == case.participants[1]), None)
        if first is None or second is None:
            return
        branch = self.random.choice(["debt", "retaliation", "counterbite"])
        if branch == "debt":
            chaser, target = (second, first) if case.case_type in {"fraud", "fake_reimbursement"} else (first, second)
            target.state.stress = self._bounded(target.state.stress + 6)
            chaser.state.stress = self._bounded(chaser.state.stress + 3)
            target.current_bubble = "这笔钱被盯上了。"
            chaser.current_bubble = "这笔账我得追回来。"
            self._adjust_relation(chaser, target, -3, "地下交易过后开始追账。")
            case.summary = f"{chaser.name} 开始追着 {target.name} 要回那笔 ${case.amount}。"
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{chaser.name} 开始追一笔地下账",
                    summary=case.summary,
                    slot=self.state.time_slot,
                    category="general",
                ),
            )
        elif branch == "retaliation":
            attacker, defender = second, first
            attacker.state.stress = self._bounded(attacker.state.stress + 5)
            defender.state.stress = self._bounded(defender.state.stress + 7)
            attacker.current_bubble = "这事我不会就这么算了。"
            defender.current_bubble = "他已经开始报复了。"
            self._adjust_relation(attacker, defender, -5, "地下交易之后开始互相报复。")
            case.summary = f"{attacker.name} 对 {defender.name} 起了报复心，整件事更难压住。"
            case.exposure_risk = min(100, case.exposure_risk + 14)
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{attacker.name} 开始报复",
                    summary=case.summary,
                    slot=self.state.time_slot,
                    category="general",
                ),
            )
        else:
            biter, target = first, second
            biter.state.focus = self._bounded(biter.state.focus + 4)
            target.state.stress = self._bounded(target.state.stress + 5)
            biter.current_bubble = "真要翻出来，我也不会一个人背。"
            target.current_bubble = "他已经想反咬了。"
            self._adjust_relation(biter, target, -4, "地下交易后开始反咬一口。")
            case.summary = f"{biter.name} 准备把这件事往 {target.name} 身上引，风向开始乱了。"
            case.exposure_risk = min(100, case.exposure_risk + 18)
            self.state.events.insert(
                0,
                build_internal_event(
                    title=f"{biter.name} 准备反咬一口",
                    summary=case.summary,
                    slot=self.state.time_slot,
                    category="general",
                ),
            )
        self.state.events = self.state.events[:8]

    def _expose_gray_case(self, case: GrayCase) -> None:
        case.status = "exposed"
        requester = next((agent for agent in self.state.agents if agent.id == case.participants[0]), None)
        donor = next((agent for agent in self.state.agents if agent.id == case.participants[1]), None)
        if requester is not None:
            requester.state.stress = self._bounded(requester.state.stress + 8 + case.severity)
            requester.state.mood = self._bounded(requester.state.mood - 5 - case.severity)
            requester.current_bubble = "这事还是被翻出来了。"
            self._remember(requester, f"你那笔“{case.summary}”被翻出来了，压力一下子上来了。", 3, long_term=True)
        if donor is not None:
            donor.state.stress = self._bounded(donor.state.stress + 6 + case.severity)
            donor.state.mood = self._bounded(donor.state.mood - 4)
            donor.current_bubble = "果然还是传开了。"
            self._remember(donor, f"你卷进去的那笔地下交易被翻了出来，大家已经开始议论。", 3, long_term=True)
        if requester is not None and donor is not None:
            self._adjust_relation(requester, donor, -4 - case.severity, "地下交易被公开后开始互相怨。")
        if requester is not None:
            self._collect_tax(
                payer_type="agent",
                payer_id=requester.id,
                payer_name=requester.name,
                revenue_key="fine",
                label="灰产曝光罚缴",
                base_amount=max(6, case.amount // 2 + case.severity * 3),
                rate_pct=100.0,
            )
        if donor is not None:
            self._collect_tax(
                payer_type="agent",
                payer_id=donor.id,
                payer_name=donor.name,
                revenue_key="fine",
                label="灰产曝光罚缴",
                base_amount=max(4, case.amount // 3 + case.severity * 2),
                rate_pct=100.0,
            )
        self.state.lab.reputation = self._bounded(self.state.lab.reputation - (4 + case.severity * 2))
        self.state.lab.team_atmosphere = self._bounded(self.state.lab.team_atmosphere - (2 + case.severity))
        self.state.market.sentiment = self._bounded(self.state.market.sentiment - (3 + case.severity))
        case_event = LabEvent(
            id=f"event-{uuid4().hex[:8]}",
            category="market",
            title=f"地下交易曝光：{self._gray_case_label(case.case_type)}",
            summary=f"{case.summary} 这件事被传开了，实验室口碑和市场情绪都受到了拖累。",
            source="系统新闻台",
            time_slot=self.state.time_slot,
            impacts={"collective_reasoning": -1, "research_progress": -1},
            participants=case.participants,
            tone_hint=-2,
            market_target=self._gray_case_market_target(case.case_type),
            market_strength=min(5, 2 + case.severity),
        )
        self.state.events.insert(0, case_event)
        self.state.events = self.state.events[:8]
        self._apply_event_to_market(case_event)
        self._log(
            "gray_case_exposed",
            case={
                "id": case.id,
                "type": case.case_type,
                "severity": case.severity,
                "participants": case.participants,
                "amount": case.amount,
            },
        )

    def _related_gray_case(self, case_id: str) -> GrayCase:
        case = next((item for item in self.state.gray_cases if item.id == case_id), None)
        if case is None:
            raise KeyError(case_id)
        return case

    def _execute_player_short(self, symbol: str, shares: int, reason: str) -> bool:
        quote = self._quote(symbol)
        if quote is None or shares <= 0:
            return False
        proceeds = int(round(quote.price * shares))
        held = self.state.player.short_positions.get(symbol, 0)
        current_avg = self.state.player.short_average_price.get(symbol, quote.price)
        new_total = held + shares
        weighted_avg = ((current_avg * held) + (quote.price * shares)) / max(1, new_total)
        self.state.player.short_positions[symbol] = new_total
        self.state.player.short_average_price[symbol] = round(weighted_avg, 2)
        self.state.player.cash += proceeds
        self.state.player.last_trade_summary = f"借机做空 {quote.name} {shares} 股，先回笼 ${proceeds}。"
        self.state.events.insert(
            0,
            build_internal_event(
                title=f"你做空了 {quote.name}",
                summary=f"你借着灰色事件的风向做空 {quote.name} {shares} 股。{reason}",
                slot=self.state.time_slot,
                category="market",
            ),
        )
        self.state.events = self.state.events[:8]
        self._log(
            "player_market_trade",
            trade={"symbol": symbol, "name": quote.name, "side": "short", "shares": shares, "amount": proceeds, "manual": True, "reason": reason},
        )
        return True

    def resolve_gray_case_action(self, case_id: str, action: str) -> WorldState:
        case = self._related_gray_case(case_id)
        if case.status != "active":
            raise ValueError("这条地下案件已经不是可操作状态了。")
        case.resolution_action = action
        case.resolution_label = self._gray_resolution_label(action)
        if action == "suppress":
            cost = max(6, 4 + case.severity * 3)
            if self.state.player.cash < cost:
                raise ValueError(f"压消息至少需要 ${cost}。")
            self.state.player.cash -= cost
            case.exposure_risk = max(6, case.exposure_risk - (18 + case.severity * 4))
            case.summary = f"你花了 ${cost} 先把“{self._gray_case_label(case.case_type)}”往下压了一层。"
            case.resolution_note = "你把风声压住了一层，但外面未必就此信服。"
            self.state.player.last_trade_summary = f"花 ${cost} 压了“{self._gray_case_label(case.case_type)}”的消息。"
            self.state.lab.reputation = self._bounded(self.state.lab.reputation - 1)
            self._apply_player_intervention_cost("gray_suppress", amount=2)
            self.state.events.insert(
                0,
                build_internal_event(
                    title="你出手压下了一条风声",
                    summary=case.summary,
                    slot=self.state.time_slot,
                    category="general",
                ),
            )
        elif action == "report":
            case.summary = f"你主动把“{self._gray_case_label(case.case_type)}”捅到了台面上。"
            case.resolution_note = "你把案子公开化了，后续会更容易进入舆论和监管视野。"
            self._expose_gray_case(case)
            self.state.lab.reputation = self._bounded(self.state.lab.reputation + 2)
            self.state.player.last_trade_summary = f"你主动举报了“{self._gray_case_label(case.case_type)}”。"
            self._apply_player_intervention_cost("gray_report", amount=2, reward=True)
        elif action == "mediate":
            cost = max(8, case.severity * 4)
            if self.state.player.cash < cost:
                raise ValueError(f"和解至少需要 ${cost}。")
            self.state.player.cash -= cost
            case.status = "settled"
            case.summary = f"你拿出 ${cost} 试着把“{self._gray_case_label(case.case_type)}”按和解的方式收掉。"
            case.resolution_note = "案子表面收住了，但参与者未必都真正服气。"
            for agent_id in case.participants:
                agent = next((item for item in self.state.agents if item.id == agent_id), None)
                if agent is not None:
                    agent.state.stress = self._bounded(agent.state.stress - 6)
                    agent.current_bubble = "先这样收住吧。"
            self.state.lab.team_atmosphere = self._bounded(self.state.lab.team_atmosphere + 2)
            self.state.player.last_trade_summary = f"你花 ${cost} 让一条地下案子先收住了。"
            self._apply_player_intervention_cost("gray_mediate", amount=1)
            self._settle_gray_case(case)
        elif action == "short":
            symbol = self._gray_case_market_target(case.case_type)
            if symbol == "broad":
                symbol = min(self.state.market.stocks, key=lambda item: item.day_change_pct).symbol if self.state.market.stocks else "SIG"
            shares = max(1, min(3, 1 + case.severity // 2))
            if not self._execute_player_short(symbol, shares, f"你借着“{self._gray_case_label(case.case_type)}”的风向下手。"):
                raise ValueError("这条案子目前找不到可做空的目标。")
            case.exposure_risk = min(100, case.exposure_risk + 8)
            case.resolution_note = "你借着风向下手套利了，这件事本身也可能被拿出来说。"
            self._apply_player_intervention_cost("gray_short", amount=1)
        else:
            raise ValueError("不支持的地下案件操作。")
        self._apply_gray_case_resolution_effects(case, action)
        self._maybe_publicize_gray_case_resolution(case, action)
        self.state.player.daily_actions.append(f"gray_case:{action}:{case.id}")
        self._log(
            "player_gray_case_action",
            action=action,
            case={"id": case.id, "type": case.case_type, "status": case.status, "risk": case.exposure_risk, "resolution_exposed": case.resolution_exposed},
            player={
                "cash": self.state.player.cash,
                "last_trade_summary": self.state.player.last_trade_summary,
                "reputation": self.state.player.reputation_score,
                "credit": self.state.player.credit_score,
                "life_satisfaction": self.state.player.life_satisfaction,
            },
        )
        self.state.events = self.state.events[:8]
        self._refresh_tasks()
        self._refresh_memory_streams()
        return self.state

    def _gray_case_label(self, case_type: str) -> str:
        return {
            "under_table_exchange": "私下交换",
            "insider_tip_sale": "内幕倒卖",
            "fake_reimbursement": "假报销",
            "data_theft": "数据窃取",
            "blackmail": "封口费",
            "fraud": "诈骗",
            "counterfeit_goods": "私货过手",
            "rent_rigging": "房产私下转手",
            "wage_kickback": "账外回扣",
            "dispatch_rigging": "派单倾斜",
            "wage_laundering": "工资洗钱",
            "labor_for_insider": "劳动换内幕",
            "wage_arrears": "工资拖欠",
            "pump_dump": "拉高出货",
            "business_gray_competition": "灰色引流抢客",
            "business_price_undercut": "压价抢客",
        }.get(case_type, case_type)

    def _gray_case_market_target(self, case_type: str) -> str:
        return {
            "insider_tip_sale": "SIG",
            "data_theft": "GEO",
            "fake_reimbursement": "broad",
            "blackmail": "broad",
            "fraud": "broad",
            "under_table_exchange": "AGR",
            "counterfeit_goods": "AGR",
            "rent_rigging": "AGR",
            "wage_kickback": "broad",
            "dispatch_rigging": "broad",
            "wage_laundering": "SIG",
            "labor_for_insider": "SIG",
            "wage_arrears": "broad",
            "pump_dump": "SIG",
            "business_gray_competition": "AGR",
            "business_price_undercut": "AGR",
        }.get(case_type, "broad")

    def _gray_resolution_label(self, action: str) -> str:
        return {
            "suppress": "压消息",
            "report": "举报",
            "mediate": "和解",
            "short": "借机做空",
        }.get(action, action)

    def _apply_gray_case_resolution_effects(self, case: GrayCase, action: str) -> None:
        if action == "suppress":
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction - 1)
        elif action == "report":
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction - 1)
            self.state.player.credit_score = self._bounded(self.state.player.credit_score + 1)
        elif action == "mediate":
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + 1)
        elif action == "short":
            self.state.player.life_satisfaction = self._bounded(self.state.player.life_satisfaction + 2)
            self.state.player.credit_score = self._bounded(self.state.player.credit_score - 1)

    def _maybe_publicize_gray_case_resolution(self, case: GrayCase, action: str) -> None:
        base_probability = {
            "suppress": 0.26,
            "report": 0.52,
            "mediate": 0.12,
            "short": 0.34,
        }.get(action, 0.18)
        probability = min(
            0.88,
            base_probability
            + (case.severity * 0.04)
            + (case.exposure_risk * 0.0025)
            + (0.06 if any(post.heat >= 16 and post.category in {"gossip", "policy"} for post in self.state.feed_timeline[:12]) else 0.0)
            - max(0, self.state.player.reputation_score - 70) * 0.002,
        )
        if self.random.random() >= probability:
            case.resolution_exposed = False
            case.resolution_note = "处理结果暂时只停留在线下，没有立刻传到公开舆论场。"
            return

        label = self._gray_case_label(case.case_type)
        actor_names = "、".join(case.participant_names[:2]) or "几个人"
        if action == "suppress":
            content = f"后巷又在传，有人想把“{label}”往下按。真要干净，何必急着捂？"
            summary = f"有人怀疑“{label}”被压消息。"
            author_type = "tourist"
        elif action == "report":
            content = f"关于“{label}”的情况，已收到举报并转入正式核查。涉及 {actor_names} 的部分，后续会给公开说明。"
            summary = f"政府公开回应了一条“{label}”举报。"
            author_type = "government"
        elif action == "mediate":
            content = f"听说“{label}”最后是私下谈掉了。表面安静了，可谁心里真服气，还不好说。"
            summary = f"有人在议论“{label}”被和解。"
            author_type = "tourist"
        else:
            content = f"“{label}”刚起风，就有人顺手拿它做空。嘴上都说不是冲钱去的，谁信啊。"
            summary = f"“{label}”被传和做空套利扯到一起。"
            author_type = "system"

        if author_type == "government":
            post = FeedPost(
                id=f"feed-{uuid4().hex[:8]}",
                author_type="government",
                author_id="government",
                author_name="小镇财政与监管局",
                day=self.state.day,
                time_slot=self.state.time_slot,
                category="policy",
                content=self._clean_feed_text(content),
                topic_tags=["监管", "案件处置", label],
                desire_tags=["稳定运行"],
                likes=4 + self.random.randint(0, 4),
                views=48 + self.random.randint(0, 24),
                summary=summary,
                impacts=["影响政府页", "进入政策观察", "进入晨报"],
            )
        elif author_type == "tourist":
            tourist = self.state.tourists[0] if self.state.tourists else None
            post = FeedPost(
                id=f"feed-{uuid4().hex[:8]}",
                author_type="tourist" if tourist else "system",
                author_id=tourist.id if tourist else "system",
                author_name=tourist.name if tourist else "系统新闻台",
                day=self.state.day,
                time_slot=self.state.time_slot,
                category="gossip",
                content=self._clean_feed_text(content),
                topic_tags=["八卦", "灰案", label],
                desire_tags=[tourist.favorite_topic if tourist else "传闻"],
                likes=3 + self.random.randint(0, 5),
                views=36 + self.random.randint(0, 20),
                summary=summary,
                impacts=["影响关系", "影响游客", "进入晨报"],
            )
        else:
            post = FeedPost(
                id=f"feed-{uuid4().hex[:8]}",
                author_type="system",
                author_id="system",
                author_name="系统新闻台",
                day=self.state.day,
                time_slot=self.state.time_slot,
                category="market",
                content=self._clean_feed_text(content),
                topic_tags=["市场", "灰案", label],
                desire_tags=["看风向"],
                likes=2 + self.random.randint(0, 4),
                views=34 + self.random.randint(0, 18),
                summary=summary,
                impacts=["影响市场", "进入晨报"],
            )
        post.credibility = self._feed_credibility_for_post(post)
        post.heat = self._compute_feed_heat(post)
        self._append_feed_post(post, remember=True, apply_impacts=True)
        case.resolution_exposed = True
        case.resolution_note = f"{self._gray_resolution_label(action)}的结果被发到了小镇微博。"
        self._log("gray_case_resolution_feed", action=action, case={"id": case.id, "type": case.case_type}, post={"author": post.author_name, "category": post.category, "heat": post.heat})

    def _resolve_player_money_exchange(self, agent: Agent, dialogue: DialogueOutcome, relation_delta: int) -> list[str]:
        intent, explicit_amount = self._player_money_intent(dialogue.player_text)
        effects: list[str] = []
        if intent == "give" and self.state.player.cash > 0:
            amount = explicit_amount or max(4, 2 + agent.money_urgency // 18)
            amount = min(amount, self.state.player.cash)
            if amount > 0:
                self.state.player.cash -= amount
                agent.cash += amount
                self._remember(agent, f"玩家刚刚明确说要给你 ${amount}。", 2)
                effects.append(f"你给了 {agent.name} ${amount}")
            return effects
        if intent == "ask" and agent.cash > 0 and (agent.generosity + agent.relations.get("player", 0)) >= 24:
            amount = explicit_amount or max(3, 1 + agent.generosity // 16)
            amount = min(amount, agent.cash)
            if amount > 0:
                agent.cash -= amount
                self.state.player.cash += amount
                self._remember(agent, f"你刚刚明确答应给玩家 ${amount}。", 2)
                effects.append(f"{agent.name} 给了你 ${amount}")
            return effects
        return effects

    def _player_dialogue_effects(self, agent: Agent, relation_delta: int, changes: dict[str, int]) -> list[str]:
        return [
            f"{agent.name} 对你关系 {self._format_delta(relation_delta)}",
            f"心情 {self._format_delta(changes['mood'])}",
            f"压力 {self._format_delta(changes['stress'])}",
            f"专注 {self._format_delta(changes['focus'])}",
            f"好奇心 {self._format_delta(changes['curiosity'])}",
        ]

    def _apply_pair_dialogue_state(
        self,
        first: Agent,
        second: Agent,
        topic: str,
        mood: str,
        gray_plan: dict[str, object] | None = None,
    ) -> dict[str, object] | None:
        if mood == "warm":
            deltas = {"mood": 4, "stress": -3, "focus": 1, "energy": -1, "curiosity": 1}
        elif mood == "spark":
            deltas = {"mood": 3, "stress": -1, "focus": 2, "energy": -1, "curiosity": 3, "geo_reasoning_skill": 1 if self._is_geoai_topic(topic) else 0}
        elif mood == "tense":
            deltas = {"mood": -3, "stress": 4, "focus": 2, "energy": -2, "curiosity": 1}
        else:
            deltas = {"mood": 1, "stress": -1, "focus": 1, "energy": -1, "curiosity": 1}
        self._shift_agent_state(first, **deltas)
        self._shift_agent_state(second, **deltas)
        first.current_activity = f"刚和 {second.name} 聊完“{topic}”，还在回味对方的话。"
        second.current_activity = f"刚和 {first.name} 接完“{topic}”，脑子里还停在那几句上。"
        first.status_summary = self._build_status_summary(first, first.relations.get(second.id, 0), topic, counterpart=second.name)
        second.status_summary = self._build_status_summary(second, second.relations.get(first.id, 0), topic, counterpart=first.name)
        first.last_interaction = f"刚在{ROOM_LABELS.get(first.current_location, first.current_location)}和 {second.name} 围绕“{topic}”聊了一轮。"
        second.last_interaction = f"刚在{ROOM_LABELS.get(second.current_location, second.current_location)}和 {first.name} 接着聊了“{topic}”。"
        transferred = self._resolve_pair_money_exchange(first, second, topic, mood, gray_plan)
        if transferred and self.state.ambient_dialogues:
            self.state.ambient_dialogues[0].effects.append(str(transferred["note"]))
        return transferred

    def _apply_desire_pair_impact(self, first: Agent, second: Agent, first_desire: str, second_desire: str, mood: str) -> None:
        if first_desire == second_desire and mood in {"warm", "spark"}:
            if first_desire == "money":
                self._shift_agent_state(first, focus=1, stress=-1)
                self._shift_agent_state(second, focus=1, stress=-1)
            elif first_desire == "rest":
                self._shift_agent_state(first, energy=2, stress=-2)
                self._shift_agent_state(second, energy=2, stress=-2)
            elif first_desire in {"bond", "care"}:
                self._shift_agent_state(first, mood=2, stress=-1)
                self._shift_agent_state(second, mood=2, stress=-1)
            elif first_desire in {"clarity", "validation", "opportunity"}:
                self._shift_agent_state(first, focus=2, curiosity=1)
                self._shift_agent_state(second, focus=2, curiosity=1)
        elif self._desires_collide(first_desire, second_desire):
            self._shift_agent_state(first, mood=-1, stress=2)
            self._shift_agent_state(second, mood=-1, stress=2)

    def _resolve_pair_money_exchange(
        self,
        first: Agent,
        second: Agent,
        topic: str,
        mood: str,
        gray_plan: dict[str, object] | None = None,
    ) -> dict[str, object] | None:
        if not self.state.ambient_dialogues:
            return None
        latest = self.state.ambient_dialogues[0]
        line = latest.line
        if f"{first.name}：" not in line or f"{second.name}：" not in line:
            return None
        try:
            left_line = line.split(f"{first.name}：", 1)[1].split(f"{second.name}：", 1)[0].strip()
            right_line = line.split(f"{second.name}：", 1)[1].strip()
        except IndexError:
            return None
        first_to_second = self._ambient_money_exchange(first, second, left_line, right_line, topic, mood, gray_plan)
        if first_to_second is not None:
            return first_to_second
        second_to_first = self._ambient_money_exchange(second, first, right_line, left_line, topic, mood, gray_plan)
        if second_to_first is not None:
            return second_to_first
        return None

    def _build_status_summary(
        self,
        agent: Agent,
        relation_value: int,
        topic: str,
        counterpart: str = "你",
        from_player: bool = False,
    ) -> str:
        relation_text = (
            "明显升温"
            if relation_value >= 55
            else "还算顺"
            if relation_value >= 15
            else "有点僵"
            if relation_value <= -15
            else "仍在观察"
        )
        mood_text = "心情很好" if agent.state.mood >= 78 else "情绪平稳" if agent.state.mood >= 55 else "情绪有点低"
        stress_text = "压力偏高" if agent.state.stress >= 65 else "不太紧绷" if agent.state.stress <= 35 else "还有点绷着"
        focus_text = "思路很聚焦" if agent.state.focus >= 78 else "注意力一般" if agent.state.focus <= 52 else "还能稳稳接话"
        lead = "和你这轮聊完后" if from_player else f"和 {counterpart} 这一轮交流后"
        return f"{lead}，关系{relation_text}；现在{mood_text}、{stress_text}，而且{focus_text}。话题还停在“{topic[:18]}”。"

    def _shift_agent_state(self, agent: Agent, **changes: int) -> None:
        agent.state.mood = self._bounded(agent.state.mood + changes.get("mood", 0))
        agent.state.stress = self._bounded(agent.state.stress + changes.get("stress", 0))
        agent.state.focus = self._bounded(agent.state.focus + changes.get("focus", 0))
        agent.state.energy = self._bounded(agent.state.energy + changes.get("energy", 0))
        agent.state.curiosity = self._bounded(agent.state.curiosity + changes.get("curiosity", 0))
        agent.state.geo_reasoning_skill = self._bounded(agent.state.geo_reasoning_skill + changes.get("geo_reasoning_skill", 0))

    def _persona_resonance(self, agent: Agent, text: str) -> int:
        keywords = {
            "rational": ["证据", "验证", "数据", "推理", "误差"],
            "creative": ["灵感", "角度", "想法", "重组", "可能性"],
            "engineering": ["实现", "系统", "流程", "稳定", "日志"],
            "empathetic": ["感受", "状态", "情绪", "慢慢", "陪"],
            "opportunist": ["信号", "机会", "风向", "外部", "趋势"],
        }
        return self._keyword_hits(text, keywords.get(agent.persona, []))

    def _keyword_hits(self, text: str, keywords: list[str]) -> int:
        return sum(1 for keyword in keywords if keyword in text)

    def _is_geoai_topic(self, topic: str) -> bool:
        return any(keyword in topic for keyword in ["GeoAI", "推理", "线索", "实验", "数据", "空间"])

    def _bounded(self, value: int) -> int:
        return max(0, min(100, value))

    def _format_delta(self, value: int) -> str:
        return f"+{value}" if value > 0 else str(value)

    def _localized_text(self, value: str) -> str:
        text = value or ""
        for legacy, localized in LEGACY_NAME_REPLACEMENTS.items():
            text = text.replace(legacy, localized)
        legacy_terms = {
            "business price undercut": "压价抢客",
            "business_price_undercut": "压价抢客",
            "business gray competition": "灰色引流抢客",
            "business_gray_competition": "灰色引流抢客",
            "operate": "营业",
            "business": "企业经营",
            "general": "社会热点",
        }
        for legacy, localized in legacy_terms.items():
            text = text.replace(legacy, localized)
        return text

    def _timeline_theme_cn(self, theme: str, category: str) -> str:
        lowered = (theme or "").lower()
        if "global market" in lowered or "股市" in theme or "汇率" in theme:
            return "全球股市与汇率"
        if "central bank" in lowered or "利率" in theme or "央行" in theme:
            return "全球央行与利率"
        if "geopolit" in lowered or "能源" in theme or "地缘" in theme:
            return "全球地缘与能源"
        if "housing" in lowered or "地产" in theme or "租金" in theme:
            return "全球住房与租金"
        if "tourism" in lowered or "消费" in theme or "旅游" in theme:
            return "全球旅游与消费"
        if "geospatial" in lowered or "geoai" in lowered or "空间智能" in theme:
            return "GeoAI 与空间智能资本"
        if "funding" in lowered or "就业" in theme or "融资" in theme:
            return "科技融资与就业"
        if "social" in lowered or "热点" in theme or "生活成本" in theme:
            return "全球社会热点"
        return {
            "market": "全球经济",
            "geoai": "GeoAI 动向",
            "tech": "科技动向",
            "policy": "全球政策",
            "general": "全球热点",
            "gaming": "游戏行业",
        }.get(category or "general", "全球热点")

    def _timeline_title_cn(self, theme_cn: str, category: str, tone_hint: int) -> str:
        if category == "market":
            if tone_hint >= 1:
                return f"{theme_cn}突发异动，风险偏好转热"
            if tone_hint <= -1:
                return f"{theme_cn}骤然承压，全球情绪转冷"
            return f"{theme_cn}出现剧烈分歧"
        if category == "geoai":
            if tone_hint >= 1:
                return f"{theme_cn}热度冲高"
            if tone_hint <= -1:
                return f"{theme_cn}推进受阻"
            return f"{theme_cn}爆出新变量"
        if category == "policy":
            if tone_hint >= 1:
                return f"{theme_cn}政策预期升温"
            if tone_hint <= -1:
                return f"{theme_cn}引发监管担忧"
            return f"{theme_cn}政策争论升温"
        if tone_hint >= 1:
            return f"{theme_cn}讨论爆热"
        if tone_hint <= -1:
            return f"{theme_cn}引爆担忧"
        return f"{theme_cn}突然冲上议程"

    def _timeline_summary_cn(self, item: NewsTimelineItem) -> str:
        theme_cn = self._timeline_theme_cn(item.theme, item.category)
        if item.status == "triggered":
            day = item.triggered_day or item.scheduled_day
            slot = ROOM_LABELS.get(item.triggered_time_slot or item.scheduled_time_slot, "")
            slot_label = {"morning": "早晨", "noon": "中午", "afternoon": "下午", "evening": "傍晚", "night": "夜晚"}.get(
                item.triggered_time_slot or item.scheduled_time_slot,
                "",
            )
            if item.tone_hint >= 1:
                effect = "这条消息把游客、市场和微博讨论都往更乐观的方向推了一层。"
            elif item.tone_hint <= -1:
                effect = "这条消息让市场、消费和舆论判断都更偏谨慎。"
            else:
                effect = "这条消息没有给出单边答案，更多是在小镇里制造讨论和试探。"
            return f"{item.source or '系统新闻台'} 围绕“{theme_cn}”抛出的全球消息，已在第 {day} 天{slot_label}落地。{effect}"
        if item.tone_hint >= 1:
            effect = "这条消息更容易抬高风险偏好和消费情绪。"
        elif item.tone_hint <= -1:
            effect = "这条消息更容易引发避险和收缩预期。"
        else:
            effect = "这条消息更可能引发争论，而不是单边推动市场。"
        return f"{item.source or '系统新闻台'} 正在为“{theme_cn}”预热一条全球消息。{effect}"

    def _timeline_item_needs_cn_migration(self, item: NewsTimelineItem) -> bool:
        title = item.title or ""
        summary = item.summary or ""
        english_title = re.search(r"[A-Za-z]{4,}", title) is not None
        english_summary = re.search(r"[A-Za-z]{4,}", summary) is not None
        return bool(english_title or english_summary)

    def _normalize_news_timeline_item_cn(self, item: NewsTimelineItem) -> None:
        item.theme = self._timeline_theme_cn(item.theme, item.category)
        if self._timeline_item_needs_cn_migration(item):
            item.title = self._timeline_title_cn(item.theme, item.category, item.tone_hint)
            item.summary = self._timeline_summary_cn(item)

    def _refresh_presence(self) -> None:
        activity_by_agent = {
            "lin": {
                "morning": ("靠着果园边慢慢醒神", "今早风挺轻。"),
                "noon": ("在麦田广场边晒太阳边说话", "中午适合慢慢聊。"),
                "afternoon": ("沿着果树间的小路散步", "下午脑子会慢一点。"),
                "evening": ("在湖畔边走边收心", "傍晚说话最不费劲。"),
                "night": ("夜里还在木桌前磨时间", "夜里人会更诚实一点。"),
            },
            "mika": {
                "morning": ("蹲在麦田边发呆和乱想", "今天天气有点适合走神。"),
                "noon": ("抱着便签在广场上乱晃", "先聊点轻松的也挺好。"),
                "afternoon": ("沿着果园来回踱步", "下午最适合想到些怪东西。"),
                "evening": ("傍晚在湖边整理碎念", "这会儿聊闲话最顺。"),
                "night": ("坐在营地木箱上继续发散", "夜里脑子反而更跳。"),
            },
            "jo": {
                "morning": ("靠在石径工坊门口醒脑子", "先把人调到在线状态。"),
                "noon": ("中午在苗圃边透气", "晒会儿太阳也算维护。"),
                "afternoon": ("回到工坊边忙边发呆", "下午容易烦，先顺顺气。"),
                "evening": ("在广场上边走边说话", "复杂问题可以晚点再聊。"),
                "night": ("晚上还在木棚下磨时间", "夜里更适合聊人，不是聊系统。"),
            },
            "rae": {
                "morning": ("正在湖畔营地整理茶点和便签", "先让大家缓一口气。"),
                "noon": ("在广场上照看午间闲聊", "轮到你说的时候慢一点也没事。"),
                "afternoon": ("回营地给大家留纸条和花茶", "状态稳住，日常就会顺很多。"),
                "evening": ("在湖边陪人散步和复盘一天", "傍晚最适合把情绪放下来。"),
                "night": ("夜里轻声收尾今天的闲话", "别急着下结论，先休息。"),
            },
            "kai": {
                "morning": ("正在果园坡地看风和消息", "今早空气有点意思。"),
                "noon": ("抱着终端去湖边聊热点和琐事", "这种天气最适合瞎聊。"),
                "afternoon": ("回果园继续晃和看消息", "下午的风向最会变。"),
                "evening": ("傍晚在营地讲外面的新鲜事", "今天的信号还没消化完。"),
                "night": ("夜里还在看外部趋势图", "晚上常常会冒出新线索。"),
            },
        }
        for agent in self.state.agents:
            if agent.is_resting:
                self._keep_agent_resting(agent)
                continue
            if "小屋" in agent.current_activity or self.state.company.name in agent.current_activity:
                if not agent.status_summary:
                    topic = agent.current_activity or "当前状态"
                    agent.status_summary = self._build_status_summary(agent, agent.relations.get("player", 0), topic, from_player=True)
                if not agent.last_interaction:
                    agent.last_interaction = "这一时段还没有发生新的深聊。"
                continue
            activity, bubble = activity_by_agent[agent.id][self.state.time_slot]
            agent.current_activity = activity
            if not self.state.latest_dialogue or self.state.latest_dialogue.agent_id != agent.id:
                agent.current_bubble = bubble
            if not agent.status_summary:
                agent.status_summary = self._build_status_summary(agent, agent.relations.get("player", 0), activity, from_player=True)
            if not agent.last_interaction:
                agent.last_interaction = "这一时段还没有发生新的深聊。"
        for tourist in self.state.tourists:
            if self.state.time_slot == "night":
                tourist.current_activity = f"正在{self.state.tourism.inn_name}歇脚，准备明天继续逛。"
                tourist.current_bubble = "今晚先住下。"
            elif tourist.current_location == self.state.tourism.market_location:
                tourist.current_activity = f"正在{self.state.tourism.market_name}转悠，顺手问价和闲聊。"
            elif tourist.current_location == self.state.tourism.inn_location:
                tourist.current_activity = f"正在{self.state.tourism.inn_name}休息，准备下一轮出门。"
            else:
                tourist.current_activity = "正在小镇里慢慢闲逛，看看哪里值得停下来。"
            tourist.brief_note = tourist.brief_note or f"{self._tourist_tier_label(tourist.visitor_tier)}，这趟会待到第 {tourist.stay_until_day} 天，最关心“{tourist.favorite_topic or '哪里最值得继续逛'}”。"
        self._record_analysis_point()

    def _ensure_agent_runtime_fields(self) -> None:
        previous_version = self.state.version or 0
        self.state.version = max(self.state.version, 63)
        if self.state.loans is None:
            self.state.loans = []
        if self.state.archived_tasks is None:
            self.state.archived_tasks = []
        if self.state.dialogue_history is None:
            self.state.dialogue_history = []
        if getattr(self.state, "feed_timeline", None) is None:
            self.state.feed_timeline = []
        if self.state.geoai_milestones is None:
            self.state.geoai_milestones = []
        expected_milestones = geoai_milestones_up_to(self.state.lab.geoai_progress)
        if len(self.state.geoai_milestones) < len(expected_milestones):
            self.state.geoai_milestones = sorted(set(self.state.geoai_milestones + expected_milestones))
        if self.state.daily_briefings is None:
            self.state.daily_briefings = []
        if getattr(self.state, "news_timeline", None) is None:
            self.state.news_timeline = []
        if getattr(self.state, "event_history", None) is None:
            self.state.event_history = []
        if getattr(self.state, "news_window_days", None) is None:
            self.state.news_window_days = 7
        for task in self.state.tasks:
            if task.category != "main":
                continue
            task.metric_key = task.metric_key or "team_total_funds"
            if task.goal_value <= task.start_value:
                start_value, goal_value = self._derive_main_task_bounds(task)
                task.start_value = start_value
                task.goal_value = goal_value
        for task in self.state.archived_tasks:
            if task.category != "main":
                continue
            task.metric_key = task.metric_key or "team_total_funds"
            if task.goal_value <= task.start_value:
                start_value, goal_value = self._derive_main_task_bounds(task)
                task.start_value = start_value
                task.goal_value = goal_value
        if self.state.gray_cases is None:
            self.state.gray_cases = []
        if self.state.lifestyle_catalog is None or not self.state.lifestyle_catalog:
            self.state.lifestyle_catalog = build_initial_world().lifestyle_catalog
        if self.state.properties is None or not self.state.properties:
            self.state.properties = build_initial_world().properties
        if getattr(self.state, "businesses", None) is None or not self.state.businesses:
            self.state.businesses = build_initial_world().businesses
        if not any(asset.id == "property-underground-casino" for asset in self.state.properties):
            self.state.properties.append(
                next(asset for asset in build_initial_world().properties if asset.id == "property-underground-casino").model_copy(deep=True)
            )
        for seed_id in {"property-qingsong-coop", "property-backstreet-store"}:
            if not any(asset.id == seed_id for asset in self.state.properties):
                self.state.properties.append(next(asset for asset in build_initial_world().properties if asset.id == seed_id).model_copy(deep=True))
        for asset in self.state.properties or []:
            if asset.owner_type == "government" and not asset.facility_kind:
                if "旅馆" in asset.name or asset.property_type == "rental_house":
                    asset.facility_kind = "public_housing"
                    if asset.name == "公共旅馆附楼":
                        asset.name = "公共住房"
                elif "集市" in asset.name or asset.property_type == "shop":
                    asset.facility_kind = "night_market_stall"
                    if asset.name == "公共集市摊位":
                        asset.name = "夜市摊位"
                elif asset.property_type == "greenhouse":
                    asset.facility_kind = "visitor_service_station"
                    if not asset.name:
                        asset.name = "游客服务站"
        if previous_version < 45:
            self._trim_government_facility_inventory()
        self._rebalance_property_layout()
        self._rebalance_government_facilities()
        if self.state.finance_history is None:
            self.state.finance_history = []
        if self.state.tourists is None:
            self.state.tourists = []
        if getattr(self.state, "tourism", None) is None:
            self.state.tourism = TourismState()
        if getattr(self.state, "casino", None) is None:
            self.state.casino = CasinoState()
        if getattr(self.state.tourism, "max_visitor_cap", None) is None:
            self.state.tourism.max_visitor_cap = 10
        self.state.tourism.active_visitor_cap = max(1, min(self.state.tourism.active_visitor_cap or 7, self.state.tourism.max_visitor_cap))
        if not self.state.tourism.season_mode:
            self.state.tourism.season_mode = "normal"
        if self.state.tourism.daily_arrivals is None:
            self.state.tourism.daily_arrivals = 0
        if self.state.tourism.daily_departures is None:
            self.state.tourism.daily_departures = 0
        if self.state.tourism.daily_private_income is None:
            self.state.tourism.daily_private_income = 0
        if self.state.tourism.total_private_income is None:
            self.state.tourism.total_private_income = 0
        if self.state.tourism.daily_government_income is None:
            self.state.tourism.daily_government_income = 0
        if self.state.tourism.total_government_income is None:
            self.state.tourism.total_government_income = 0
        if self.state.tourism.daily_public_operator_income is None:
            self.state.tourism.daily_public_operator_income = 0
        if self.state.tourism.total_public_operator_income is None:
            self.state.tourism.total_public_operator_income = 0
        if self.state.tourism.repeat_customers_total is None:
            self.state.tourism.repeat_customers_total = 0
        if self.state.tourism.vip_customers_total is None:
            self.state.tourism.vip_customers_total = 0
        if self.state.tourism.buyer_leads_total is None:
            self.state.tourism.buyer_leads_total = 0
        if self.state.tourism.daily_messages_count is None:
            self.state.tourism.daily_messages_count = 0
        if self.state.tourism.latest_signal is None:
            self.state.tourism.latest_signal = ""
        if self.state.casino.daily_visits is None:
            self.state.casino.daily_visits = 0
        if self.state.casino.total_visits is None:
            self.state.casino.total_visits = 0
        if self.state.casino.daily_wagers is None:
            self.state.casino.daily_wagers = 0
        if self.state.casino.total_wagers is None:
            self.state.casino.total_wagers = 0
        if self.state.casino.daily_payouts is None:
            self.state.casino.daily_payouts = 0
        if self.state.casino.total_payouts is None:
            self.state.casino.total_payouts = 0
        if self.state.casino.daily_tax is None:
            self.state.casino.daily_tax = 0
        if self.state.casino.total_tax is None:
            self.state.casino.total_tax = 0
        if self.state.casino.daily_big_wins is None:
            self.state.casino.daily_big_wins = 0
        if self.state.casino.total_big_wins is None:
            self.state.casino.total_big_wins = 0
        if self.state.casino.house_bankroll is None:
            self.state.casino.house_bankroll = 6000
        if self.state.casino.current_heat is None:
            self.state.casino.current_heat = 18
        if self.state.casino.last_note is None:
            self.state.casino.last_note = "后巷牌桌今晚还没真正热起来。"
        if previous_version < 33:
            self._refresh_tourism_cycle()
        if self.state.section_signatures is None:
            self.state.section_signatures = {}
        for post in self.state.feed_timeline or []:
            post.content = self._localized_text(post.content)
            post.summary = self._localized_text(post.summary)
            post.topic_tags = [self._localized_text(item) for item in post.topic_tags or []]
            post.desire_tags = [self._localized_text(item) for item in post.desire_tags or []]
            post.impacts = [self._localized_text(item) for item in post.impacts or []]
            if post.credibility is None:
                post.credibility = 50
            if getattr(post, "reposts", None) is None:
                post.reposts = 0
        self._recompute_feed_timeline_heat()
        player_owned = [asset.id for asset in self.state.properties if asset.owner_type == "player" and asset.owner_id == self.state.player.id and asset.status == "owned"]
        if player_owned and not self.state.player.owned_property_ids:
            self.state.player.owned_property_ids = player_owned
        for agent in self.state.agents:
            localized_name = DISPLAY_NAME_BY_ID.get(agent.id)
            if localized_name:
                agent.name = localized_name
            if agent.home_position is None:
                home = HOME_SPOTS.get(agent.id)
                if home is not None:
                    agent.home_position = Point(x=home[0], y=home[1])
                    agent.home_label = home[2]
            if agent.id in HOME_SPOTS:
                agent.home_label = HOME_SPOTS[agent.id][2]
            if not agent.current_plan:
                agent.current_plan = "继续观察当前局面，等待合适的合作或冲突时机。"
            if not agent.immediate_intent:
                agent.immediate_intent = "想先听听周围在聊什么。"
            if not agent.social_stance:
                agent.social_stance = "observe"
            if agent.cash <= 0:
                agent.cash = 0
            if agent.relation_cooldowns is None:
                agent.relation_cooldowns = {}
            if not agent.money_desire:
                agent.money_desire = 50
            if not agent.money_urgency:
                agent.money_urgency = agent.money_desire
            if not agent.credit_score:
                agent.credit_score = 70
            if not agent.generosity:
                agent.generosity = 50
            if not agent.risk_appetite:
                agent.risk_appetite = 50
        for tourist in self.state.tourists:
            if not tourist.current_location:
                tourist.current_location = self._room_for(tourist.position.x, tourist.position.y)
            tourist.visitor_tier = tourist.visitor_tier or "regular"
            tourist.message_influence = tourist.message_influence or (3 if tourist.visitor_tier == "vip" else 2 if tourist.visitor_tier in {"repeat", "buyer"} else 1)
            tourist.favorite_topic = tourist.favorite_topic or "这里最值得逛哪里"
            tourist.current_activity = tourist.current_activity or f"正在{self.state.tourism.market_name}和{self.state.tourism.inn_name}之间慢慢逛。"
            tourist.current_bubble = tourist.current_bubble or "这里还挺热闹。"
            tourist.brief_note = tourist.brief_note or f"这趟会待到第 {tourist.stay_until_day} 天。"
            if tourist.short_term_memory is None:
                tourist.short_term_memory = []
            if tourist.market_portfolio is None:
                tourist.market_portfolio = {}
            if tourist.market_invested_total is None:
                tourist.market_invested_total = 0
            if tourist.market_last_action is None:
                tourist.market_last_action = ""
            if tourist.market_preference is None:
                tourist.market_preference = ""
            if tourist.market_preference_note is None:
                tourist.market_preference_note = ""
            if not tourist.short_term_memory:
                tourist.short_term_memory = [
                    MemoryEntry(
                        text=f"你刚来到这里，最先留意的是“{tourist.favorite_topic or '哪里最值得继续逛'}”。",
                        day=self.state.day,
                        time_slot=self.state.time_slot,
                        importance=1,
                    )
                ]
            for memory in tourist.short_term_memory or []:
                memory.text = self._localized_text(memory.text)
            tourist.favorite_topic = self._localized_text(tourist.favorite_topic)
            tourist.current_activity = self._localized_text(tourist.current_activity)
            tourist.current_bubble = self._localized_text(tourist.current_bubble)
            tourist.brief_note = self._localized_text(tourist.brief_note)
            tourist.market_last_action = self._localized_text(tourist.market_last_action or "")
            tourist.market_preference = self._localized_text(tourist.market_preference or "")
            tourist.market_preference_note = self._localized_text(tourist.market_preference_note or "")

        for agent in self.state.agents:
            if agent.portfolio is None:
                agent.portfolio = {}
            if not agent.life_satisfaction:
                agent.life_satisfaction = 56
            if not agent.consumption_desire:
                agent.consumption_desire = 46
            if not agent.housing_quality:
                agent.housing_quality = 46
            if not agent.materialism:
                agent.materialism = 50
            if not agent.comfort_preference:
                agent.comfort_preference = 50
            if agent.monthly_burden is None:
                agent.monthly_burden = 0
            if agent.owned_property_ids is None:
                agent.owned_property_ids = []
            if not agent.work_drive:
                agent.work_drive = {"engineering": 72, "rational": 62, "creative": 44, "empathetic": 56, "opportunist": 60}.get(agent.persona, 54)
            if not agent.daily_cost_baseline:
                agent.daily_cost_baseline = {"engineering": 6, "rational": 7, "creative": 8, "empathetic": 7, "opportunist": 9}.get(agent.persona, 7)
            if not agent.employer_name:
                agent.employer_name = "青松数据服务"
            if agent.consumption_coupon_balance is None:
                agent.consumption_coupon_balance = 0
            if agent.deposit_balance is None:
                agent.deposit_balance = 0
            if not agent.owned_property_ids:
                owned = [asset.id for asset in self.state.properties if asset.owner_type == "agent" and asset.owner_id == agent.id and asset.status == "owned"]
                if owned:
                    agent.owned_property_ids = owned
            if agent.last_trade_summary is None:
                agent.last_trade_summary = ""
            if not agent.goals:
                agent.goals = ["把今天的任务往前推一步"]
            if not agent.core_needs:
                agent.core_needs = ["想把今天过顺一点"]
            if agent.public_facts is None:
                agent.public_facts = []
            if agent.hidden_facts is None:
                agent.hidden_facts = []
            if agent.speech_habits is None:
                agent.speech_habits = []
            if agent.memory_stream is None:
                agent.memory_stream = []
            if agent.taboos is None:
                agent.taboos = []
            if agent.allies is None:
                agent.allies = []
            if agent.rivals is None:
                agent.rivals = []
            if not agent.status_summary:
                topic = agent.current_activity or "当前工作"
                agent.status_summary = self._build_status_summary(agent, agent.relations.get("player", 0), topic, from_player=True)
            if not agent.last_interaction:
                agent.last_interaction = "这一时段还没有发生新的深聊。"
            agent.current_activity = self._localized_text(agent.current_activity)
            agent.current_bubble = self._localized_text(agent.current_bubble)
            agent.status_summary = self._localized_text(agent.status_summary)
            agent.last_interaction = self._localized_text(agent.last_interaction)
            agent.current_plan = self._localized_text(agent.current_plan)
            agent.goals = [self._localized_text(item) for item in agent.goals or []]
            agent.taboos = [self._localized_text(item) for item in agent.taboos or []]
            agent.public_facts = [self._localized_text(item) for item in agent.public_facts or []]
            agent.hidden_facts = [self._localized_text(item) for item in agent.hidden_facts or []]
            agent.core_needs = [self._localized_text(item) for item in agent.core_needs or []]
            agent.speech_habits = [self._localized_text(item) for item in agent.speech_habits or []]
            agent.memory_stream = [self._localized_text(item) for item in agent.memory_stream or []]
            for memory in agent.short_term_memory or []:
                memory.text = self._localized_text(memory.text)
            normalized_long_term: list[MemoryEntry] = []
            seen_memory_signatures: set[str] = set()
            for memory in agent.long_term_memory or []:
                memory.text = self._summarize_long_term_memory(self._localized_text(memory.text))
                signature = self._memory_signature(memory.text)
                if signature in seen_memory_signatures:
                    continue
                seen_memory_signatures.add(signature)
                normalized_long_term.append(memory)
            agent.long_term_memory = self._merge_long_term_memories(normalized_long_term[:6])
        if self.state.player.portfolio is None:
            self.state.player.portfolio = {}
        if not self.state.player.credit_score:
            self.state.player.credit_score = 72
        if self.state.player.reputation_score is None:
            self.state.player.reputation_score = 58
        if self.state.player.relation_cooldowns is None:
            self.state.player.relation_cooldowns = {}
        if self.state.player.short_positions is None:
            self.state.player.short_positions = {}
        if self.state.player.short_average_price is None:
            self.state.player.short_average_price = {}
        if self.state.player.last_trade_summary is None:
            self.state.player.last_trade_summary = ""
        if not self.state.player.risk_appetite:
            self.state.player.risk_appetite = 52
        if not self.state.player.life_satisfaction:
            self.state.player.life_satisfaction = 56
        if not self.state.player.consumption_desire:
            self.state.player.consumption_desire = 44
        if not self.state.player.housing_quality:
            self.state.player.housing_quality = 48
        if not self.state.player.materialism:
            self.state.player.materialism = 52
        if not self.state.player.comfort_preference:
            self.state.player.comfort_preference = 58
        if self.state.player.monthly_burden is None:
            self.state.player.monthly_burden = 0
        if self.state.player.owned_property_ids is None:
            self.state.player.owned_property_ids = []
        if not self.state.player.work_drive:
            self.state.player.work_drive = 58
        if not self.state.player.daily_cost_baseline:
            self.state.player.daily_cost_baseline = 8
        if not self.state.player.employer_name:
            self.state.player.employer_name = "青松数据服务"
        if self.state.player.consumption_coupon_balance is None:
            self.state.player.consumption_coupon_balance = 0
        if self.state.player.deposit_balance is None:
            self.state.player.deposit_balance = 0
        if self.state.bank is None:
            self.state.bank = build_initial_world().bank
        if self.state.government is None:
            self.state.government = build_initial_world().government
        if self.state.government.reserve_balance is None:
            self.state.government.reserve_balance = 260
        if self.state.government.total_welfare_paid is None:
            self.state.government.total_welfare_paid = 0
        if self.state.government.total_coupons_issued is None:
            self.state.government.total_coupons_issued = 0
        if self.state.government.total_public_investment is None:
            self.state.government.total_public_investment = 0
        if self.state.government.fiscal_cycle_days is None:
            self.state.government.fiscal_cycle_days = 15
        if self.state.government.next_distribution_day is None:
            self.state.government.next_distribution_day = self.state.government.fiscal_cycle_days
        if previous_version < 34 and self.state.government.last_distribution_day == 0:
            cycle = max(1, self.state.government.fiscal_cycle_days)
            self.state.government.next_distribution_day = ((max(1, self.state.day) // cycle) + 1) * cycle
        if self.state.bank.base_deposit_daily_rate_pct is None:
            self.state.bank.base_deposit_daily_rate_pct = 0.32
        if self.state.bank.deposit_daily_rate_pct is None:
            self.state.bank.deposit_daily_rate_pct = self.state.bank.base_deposit_daily_rate_pct
        if self.state.bank.total_deposits is None:
            self.state.bank.total_deposits = self.state.player.deposit_balance + sum(agent.deposit_balance for agent in self.state.agents)
        if self.state.bank.total_interest_paid is None:
            self.state.bank.total_interest_paid = 0
        if self.state.government.public_service_level is None:
            self.state.government.public_service_level = 36
        if self.state.government.tourism_support_level is None:
            self.state.government.tourism_support_level = 30
        if self.state.government.housing_support_level is None:
            self.state.government.housing_support_level = 24
        if self.state.government.government_asset_ids is None:
            self.state.government.government_asset_ids = []
        if self.state.government.last_distribution_note is None:
            self.state.government.last_distribution_note = "财政周期还没有触发。"
        if self.state.government.current_agenda is None:
            self.state.government.current_agenda = "观察税收、游客和住房压力。"
        if self.state.government.last_agent_action is None:
            self.state.government.last_agent_action = "财政周期还没有触发新的建设动作。"
        if self.state.government.last_agent_reason is None:
            self.state.government.last_agent_reason = "系统会根据游客、住房、储备和资产收益决定下一步。"
        if getattr(self.state.government, "last_macro_action", None) is None:
            self.state.government.last_macro_action = "当前仍采用常规政府模式。"
        if getattr(self.state.government, "big_mode_enabled", None) is None:
            self.state.government.big_mode_enabled = False
        if getattr(self.state.government, "can_tune_taxes", None) is None:
            self.state.government.can_tune_taxes = True
        if getattr(self.state.government, "can_tune_rates", None) is None:
            self.state.government.can_tune_rates = True
        if getattr(self.state.government, "can_manage_construction", None) is None:
            self.state.government.can_manage_construction = True
        if getattr(self.state.government, "can_trade_assets", None) is None:
            self.state.government.can_trade_assets = True
        if getattr(self.state.government, "can_intervene_prices", None) is None:
            self.state.government.can_intervene_prices = True
        if self.state.government.known_signals is None:
            self.state.government.known_signals = []
        if self.state.government.last_agent_action_day is None:
            self.state.government.last_agent_action_day = 0
        if self.state.government.last_distribution_day is None:
            self.state.government.last_distribution_day = 0
        if self.state.government.last_audit_day is None:
            self.state.government.last_audit_day = 0
        self.state.government.audit_cooldown_days = max(2, min(10, 2 + round((100 - self.state.government.enforcement_level) / 12)))
        if self.state.government.last_targeted_support is None:
            self.state.government.last_targeted_support = 0
        if self.state.government.approval_score is None:
            self.state.government.approval_score = 56
        if self.state.government.approval_note is None:
            self.state.government.approval_note = "公众目前对政府维持温和支持。"
        if self.state.government.last_coupon_pool is None:
            self.state.government.last_coupon_pool = 0
        if self.state.government.last_public_service_spend is None:
            self.state.government.last_public_service_spend = 0
        if self.state.government.last_investment_spend is None:
            self.state.government.last_investment_spend = 0
        if self.state.government.last_reserve_retained is None:
            self.state.government.last_reserve_retained = 0
        if self.state.government.last_cycle_tax_revenue is None:
            self.state.government.last_cycle_tax_revenue = 0
        if self.state.government.last_cycle_nonfine_consumption is None:
            self.state.government.last_cycle_nonfine_consumption = 0
        if self.state.government.daily_asset_revenue is None:
            self.state.government.daily_asset_revenue = 0
        if self.state.government.daily_asset_maintenance is None:
            self.state.government.daily_asset_maintenance = 0
        if self.state.government.daily_asset_net is None:
            self.state.government.daily_asset_net = 0
        if self.state.government.expenditures is None:
            self.state.government.expenditures = {"welfare": 0}
        self.state.government.expenditures.setdefault("coupon", 0)
        self.state.government.expenditures.setdefault("public_service", 0)
        self.state.government.expenditures.setdefault("investment", 0)
        if self.state.government.welfare_low_cash_threshold is None:
            self.state.government.welfare_low_cash_threshold = 24
        if self.state.government.welfare_base_support is None:
            self.state.government.welfare_base_support = 10
        if self.state.government.welfare_bankruptcy_support is None:
            self.state.government.welfare_bankruptcy_support = 22
        if self.state.government.revenues is None:
            self.state.government.revenues = {"wage": 0, "market": 0, "property": 0, "consumption": 0, "business": 0, "gambling": 0, "fine": 0, "government_asset": 0, "tourism_public": 0}
        self.state.government.revenues.setdefault("business", 0)
        self.state.government.revenues.setdefault("gambling", 0)
        self.state.government.revenues.setdefault("government_asset", 0)
        self.state.government.revenues.setdefault("tourism_public", 0)
        self._refresh_government_agent_state()
        if self.state.businesses is None:
            self.state.businesses = []
        business_seed_map = {item.id: item for item in build_initial_world().businesses}
        for business in self.state.businesses or []:
            if getattr(business, "daily_tax_paid", None) is None:
                business.daily_tax_paid = 0
            if getattr(business, "total_tax_paid", None) is None:
                business.total_tax_paid = 0
            if getattr(business, "lifecycle_stage", None) is None:
                business.lifecycle_stage = "operating"
            if getattr(business, "expansion_level", None) is None:
                business.expansion_level = 0
            if getattr(business, "growth_streak_days", None) is None:
                business.growth_streak_days = 0
            if getattr(business, "loss_streak_days", None) is None:
                business.loss_streak_days = 0
            if getattr(business, "merged_into_id", None) is None:
                business.merged_into_id = ""
            if getattr(business, "public_heat", None) is None:
                business.public_heat = 0
            if not getattr(business, "location_key", None):
                business.location_key = getattr(business_seed_map.get(business.id), "location_key", "") or ""
            if getattr(business, "last_post_day", None) is None:
                business.last_post_day = 0
            if getattr(business, "last_post_slot", None) is None:
                business.last_post_slot = ""
        self._sync_business_locations()
        if self.state.company is None:
            self.state.company = build_initial_world().company
        if self.state.bank_loans is None:
            self.state.bank_loans = []
        if self.state.market.index_history is None:
            self.state.market.index_history = []
        if self.state.market.daily_index_history is None:
            self.state.market.daily_index_history = []
        if not self.state.market.inflation_index:
            self.state.market.inflation_index = 100.0
        if self.state.market.daily_inflation_pct is None:
            self.state.market.daily_inflation_pct = 0.0
        if self.state.market.living_cost_pressure is None:
            self.state.market.living_cost_pressure = 8
        if self.state.market.turnover_total is None:
            self.state.market.turnover_total = 0.0
        if self.state.market.turnover_ratio_pct is None:
            self.state.market.turnover_ratio_pct = 0.0
        if self.state.market.realized_volatility_pct is None:
            self.state.market.realized_volatility_pct = 0.8
        if self.state.market.advancers is None:
            self.state.market.advancers = 0
        if self.state.market.decliners is None:
            self.state.market.decliners = 0
        if not self.state.market.regime:
            self.state.market.regime = "bull"
        if not self.state.market.regime_age:
            self.state.market.regime_age = 1
        if not self.state.market.rotation_leader:
            self.state.market.rotation_leader = "GEO"
        if not self.state.market.rotation_age:
            self.state.market.rotation_age = 1
        for quote in self.state.market.stocks or []:
            if not quote.base_price:
                quote.base_price = BASE_PRICES.get(quote.symbol, quote.open_price or quote.price)
            if not quote.fair_value:
                quote.fair_value = quote.price or quote.base_price
            if not quote.shares_outstanding:
                quote.shares_outstanding = BASE_SHARES_OUTSTANDING.get(quote.symbol, 100000)
            if not quote.avg_volume:
                quote.avg_volume = BASE_AVG_VOLUME.get(quote.symbol, 4200)
            if quote.volume is None:
                quote.volume = 0
            if quote.turnover_pct is None:
                quote.turnover_pct = 0.0
            if not quote.volatility_score:
                quote.volatility_score = 0.9
        if previous_version < 29 or any((quote.price or 0) > 500 or (quote.base_price or 0) > 500 for quote in self.state.market.stocks or []):
            self._normalize_market_quotes_for_realism()
        for event in self.state.events or []:
            event.title = self._localized_text(event.title)
            event.summary = self._localized_text(event.summary)
        for beat in self.state.story_beats or []:
            beat.title = self._localized_text(beat.title)
            beat.summary = self._localized_text(beat.summary)
        for record in self.state.dialogue_history or []:
            record.participant_names = [self._localized_text(name) for name in record.participant_names or []]
            record.topic = self._localized_text(record.topic)
            record.summary = self._localized_text(record.summary)
            record.key_point = self._localized_text(record.key_point)
        if self.state.analysis_history is None:
            self.state.analysis_history = []
        if self.state.daily_economy_history is None:
            self.state.daily_economy_history = []
        if self.state.daily_bank_history is None:
            self.state.daily_bank_history = []
        if self.state.daily_casino_history is None:
            self.state.daily_casino_history = []
        if getattr(self.state, "daily_business_history", None) is None:
            self.state.daily_business_history = []
        if not self.state.daily_economy_history:
            self._backfill_daily_economy_history_from_finance()
        if not self.state.daily_bank_history:
            self._backfill_daily_bank_history_from_finance()
        if not self.state.daily_casino_history:
            self._backfill_daily_casino_history_from_finance()
        if not self.state.daily_business_history:
            self._record_daily_business_point(self.state.day)
        self._backfill_casino_dialogue_history_from_finance()
        if not self.state.daily_economy_history:
            self._record_daily_economy_point(
                self.state.day,
                tourism_private_income=self.state.tourism.daily_private_income,
                tourism_government_income=self.state.tourism.daily_government_income,
                tourism_public_income=self.state.tourism.daily_public_operator_income,
            )
        if not self.state.daily_bank_history:
            self._record_daily_bank_point(self.state.day)
        if not self.state.daily_casino_history:
            self._record_daily_casino_point(self.state.day)
        if not self.state.daily_business_history:
            self._record_daily_business_point(self.state.day)
        if not self.state.analysis_history:
            self._record_analysis_point()
            record.transcript = [self._localized_text(line) for line in record.transcript or []]
            record.financial_note = self._localized_text(record.financial_note)
            if record.desire_labels:
                record.desire_labels = {self._localized_text(key): self._localized_text(value) for key, value in record.desire_labels.items()}
        self._refresh_market_microstructure()
        for brief in self.state.daily_briefings or []:
            brief.title = self._localized_text(brief.title)
            brief.lead = self._localized_text(brief.lead)
            brief.items = [self._localized_text(item) for item in brief.items or []]
            if not brief.entries:
                brief.entries = self._build_brief_entries_from_items(brief.items or [])
            for entry in brief.entries:
                entry.text = self._localized_text(entry.text)
                entry.title = self._localized_text(getattr(entry, "title", "") or "")
                entry.summary = self._localized_text(getattr(entry, "summary", "") or "")
                entry.result = self._localized_text(getattr(entry, "result", "") or "")
                entry.impact = self._localized_text(getattr(entry, "impact", "") or "")
                if not entry.title and not entry.summary and entry.text:
                    entry.title = entry.text.split("：", 1)[0] if "：" in entry.text else entry.text[:12]
                    entry.summary = entry.text.split("：", 1)[-1] if "：" in entry.text else entry.text
                if not entry.result:
                    entry.result = "这件事已经不只是夜里那一下，今天还会继续留下后劲。"
                if not entry.impact:
                    entry.impact = "它会继续影响今天的小镇讨论、资金判断和人物动作。"
        for item in self.state.news_timeline or []:
            item.title = self._localized_text(item.title)
            item.summary = self._localized_text(item.summary)
            item.theme = self._localized_text(item.theme)
            self._normalize_news_timeline_item_cn(item)
        for case in self.state.gray_cases or []:
            case.participant_names = [self._localized_text(name) for name in case.participant_names or []]
            if getattr(case, "resolution_action", None) is None:
                case.resolution_action = ""
            if getattr(case, "resolution_label", None) is None:
                case.resolution_label = ""
            if getattr(case, "resolution_exposed", None) is None:
                case.resolution_exposed = False
            if getattr(case, "resolution_note", None) is None:
                case.resolution_note = ""
        for tourist in self.state.tourists or []:
            if getattr(tourist, "active_in_scene", None) is None:
                tourist.active_in_scene = True
            if tourist.target_position is None:
                tourist.target_position = None
            if tourist.target_location is None:
                tourist.target_location = ""
            if tourist.linger_ticks is None:
                tourist.linger_ticks = 0
            if tourist.last_locations is None:
                tourist.last_locations = []
        if getattr(self.state.tourism, "max_visitor_cap", None) is None:
            self.state.tourism.max_visitor_cap = 10
        self.state.tourism.active_visitor_cap = max(1, min(7, self.state.tourism.max_visitor_cap))
        self._rebalance_tourist_activity()
        self._rebalance_tourists_if_clustered()
        if previous_version < 28:
            self._normalize_extreme_relations_on_upgrade()
            case.topic = self._localized_text(case.topic)
            case.summary = self._localized_text(case.summary)
        for record in self.state.finance_history or []:
            record.actor_name = self._localized_text(record.actor_name)
            record.summary = self._localized_text(record.summary)
            record.asset_name = self._localized_text(record.asset_name)
            record.counterparty = self._localized_text(record.counterparty)

    def _build_brief_entries_from_items(self, items: list[str]) -> list[DailyBriefItem]:
        entries: list[DailyBriefItem] = []
        for item in items:
            target_kind = ""
            target_id = ""
            target_filter = ""
            if item.startswith(("股市速写", "板块主线", "研究头条")):
                target_kind = "market"
            elif item.startswith("借贷消息"):
                target_kind = "dialogue"
                target_filter = "loan"
            elif item.startswith("小道消息"):
                target_kind = "dialogue"
                target_filter = "gray"
            elif item.startswith("关系风波"):
                target_kind = "dialogue"
                target_filter = "desire"
            elif item.startswith("八卦速递"):
                target_kind = "dialogue"
            elif item.startswith("故事线更新"):
                target_kind = "story"
                title = item.split("：", 1)[-1].split("，", 1)[0]
                story = next((beat for beat in self.state.story_beats if title and title in beat.title), None)
                target_id = story.id if story else ""
            elif item.startswith("新闻摘录"):
                target_kind = "event"
                title = item.split("：", 1)[-1].split(" 还在被", 1)[0]
                event = next((entry for entry in self.state.events if title and title in entry.title), None)
                target_id = event.id if event else ""
            entries.append(
                DailyBriefItem(
                    id=f"brief-item-{uuid4().hex[:8]}",
                    text=item,
                    title=item.split("：", 1)[0] if "：" in item else item[:12],
                    summary=item.split("：", 1)[-1] if "：" in item else item,
                    target_kind=target_kind,
                    target_id=target_id,
                    target_filter=target_filter,
                )
            )
        return entries

    def _pick_social_topic(self, first: Agent, second: Agent) -> str:
        daily_candidates = [
            f"{weather_label(self.state.weather)}天气",
            "午饭想吃什么",
            "昨晚有没有睡好",
            "湖边散步时想到的事",
            "今天谁看起来最累",
            "要不要晚点一起走走",
            "刚刚路过听到的话",
            "最近的作息有点乱",
            "今天心情为什么这样",
            "傍晚适不适合去湖边吹风",
        ]
        research_candidates = [
            "新的 GeoAI 线索",
            "午间实验安排",
            "一条外部热点",
            "今天的实验瓶颈",
            "下一轮合作分工",
        ]
        finance_candidates = [
            "手头预算够不够",
            "今天要不要看一眼股票",
            "能不能先借点周转",
        ]
        roll = self.random.random()
        if roll < 0.10:
            candidates = finance_candidates
        elif roll < 0.28:
            candidates = research_candidates
        else:
            candidates = daily_candidates
        if abs(first.relations.get(second.id, 0)) >= 55:
            candidates.extend(["昨晚没说完的话", "要不要晚点一起坐会儿"])
        if first.state.stress + second.state.stress >= 105:
            candidates.extend(["谁最近有点太累了", "刚刚那次分歧", "谁该先退一步"])
        return self.random.choice(candidates)

    def _thread_mood(self, first: Agent, second: Agent, topic: str, existing: SocialThread | None, first_desire: str, second_desire: str) -> str:
        relation = (first.relations.get(second.id, 0) + second.relations.get(first.id, 0)) / 2
        stress = first.state.stress + second.state.stress
        if existing and existing.mood in {"warm", "spark"} and relation >= 45:
            return existing.mood
        if self._desires_collide(first_desire, second_desire):
            return "tense"
        if first_desire == second_desire and relation >= 18:
            return "warm" if first_desire in {"bond", "care", "rest"} else "spark"
        if stress >= 115 or relation <= -10 or "分歧" in topic:
            return "tense"
        if relation >= 70:
            return "warm"
        if "GeoAI" in topic or "合作" in topic or "做下去" in topic:
            return "spark"
        return "neutral"

    def _ambient_pair_lines(
        self,
        first: Agent,
        second: Agent,
        topic: str,
        mood: str,
        continued: bool,
        first_desire: str,
        second_desire: str,
    ) -> tuple[str, str, dict[str, object] | None]:
        pair_relation = (first.relations.get(second.id, 0) + second.relations.get(first.id, 0)) / 2
        gray_options = self._gray_trade_catalog(first, second, topic, mood, first_desire, second_desire)
        if gray_options and self.random.random() < 0.18:
            chosen = self.random.choice(gray_options)
            return str(chosen["line_a"]), str(chosen["line_b"]), chosen
        if (
            ("消息" in topic or "风向" in topic or "机会" in topic or "周转" in topic)
            and pair_relation >= 26
            and {first_desire, second_desire} & {"money", "opportunity"}
            and self.random.random() < 0.16
        ):
            amount = max(5, max(first.money_urgency, second.money_urgency) // 18)
            if first.money_urgency >= second.money_urgency:
                left = f"这笔先别摆到台面上，你私下给我 {amount} 美元，我把那条消息先递给你。"
                right = "行，这笔先算非正式资源交换，别在公开台账里展开。"
                return left, right, None
            left = f"我手里那条线可以先给你，但这笔先别挂账，你私下拿 {amount} 美元来换。"
            right = f"可以，这笔先走非正式资源交换，${amount} 我先给你。"
            return left, right, None
        if any(keyword in topic for keyword in ["预算", "股票", "借点", "周转"]):
            amount = max(4, max(first.money_urgency, second.money_urgency) // 20)
            if first.money_urgency >= second.money_urgency:
                interest = self._proposed_interest_rate(first)
                request_line = f"我手头有点紧，能不能先借我 {amount} 美元周转一下？我明天还你，利息 {interest}%。"
                if self._loan_judgement_score(second, first, amount + max(1, round(amount * interest / 100))) >= 28 and second.cash >= amount:
                    response_line = f"行，我借你 {amount} 美元，明天按 {interest}% 收回来。"
                else:
                    response_line = "我这边得先看看你明天拿什么还，这笔今天先不借。"
                return request_line, response_line, None
            interest = self._proposed_interest_rate(second)
            offer_line = f"你要是真缺口不大，我可以先借你 {amount} 美元，你明天按 {interest}% 还。"
            if second.cash < 10:
                response_line = f"行，那你先借我 {amount} 美元，我明天按 {interest}% 还你。"
            else:
                response_line = "我先不借，今天更想自己扛一下。"
            return offer_line, response_line, None
        if self._desires_collide(first_desire, second_desire):
            left = f"我现在更想先顾“{DESIRE_LABELS.get(first_desire, first_desire)}”，因为我已经没有余裕再分神了，你别总把话拽去“{DESIRE_LABELS.get(second_desire, second_desire)}”。"
            right = f"可我眼下最在意的就是“{DESIRE_LABELS.get(second_desire, second_desire)}”，你别像没看见一样。我不是故意顶你，是我真的先顾不上别的。"
            return left, right, None
        if first_desire == second_desire:
            shared = DESIRE_LABELS.get(first_desire, first_desire)
            left = f"我感觉你也在惦记“{shared}”，所以我刚才那句你应该听得懂。"
            right = f"对，我这会儿也想先把“{shared}”稳住，不然今天后面整个人都要散。"
            return left, right, None
        left_seed = ambient_line_for(first, topic)
        right_seed = ambient_line_for(second, topic)
        if continued:
            left_seed = f"{left_seed[:-1]}，我还是想把刚才那句说完。"
        if mood == "tense":
            left = f"{left_seed[:-1]}，但我不同意把问题带过去。"
            right = f"{right_seed[:-1]}，你别只盯着一个点。"
            return left, right, None
        if mood == "warm":
            left = f"{left_seed[:-1]}，要不我们还是并肩把它做完。"
            right = f"{right_seed[:-1]}，行，我跟你站一边。"
            return left, right, None
        if mood == "spark":
            left = f"{left_seed[:-1]}，这条线也许真能一起做大。"
            right = f"{right_seed[:-1]}，那我继续往前接。"
            return left, right, None
        if first.id == "lin":
            right = f"{right_seed[:-1]}，我接着听你把细节说完。"
        elif first.id == "mika":
            right = f"{right_seed[:-1]}，这个角度我能跟上。"
        elif first.id == "jo":
            right = f"{right_seed[:-1]}，那我顺手想一下怎么落地。"
        elif first.id == "rae":
            right = f"{right_seed[:-1]}，你慢慢说，我在听。"
        else:
            right = f"{right_seed[:-1]}，这波动静我也想继续看。"
        left = left_seed
        return left, right, None

    def _desires_collide(self, first_desire: str, second_desire: str) -> bool:
        colliding = {
            frozenset({"money", "care"}),
            frozenset({"money", "bond"}),
            frozenset({"rest", "opportunity"}),
            frozenset({"rest", "validation"}),
            frozenset({"control", "bond"}),
            frozenset({"control", "care"}),
            frozenset({"clarity", "opportunity"}),
            frozenset({"validation", "clarity"}),
        }
        return frozenset({first_desire, second_desire}) in colliding

    def _desire_topic_between(self, first: Agent, second: Agent, first_desire: str, second_desire: str) -> str:
        if first_desire == second_desire:
            shared = {
                "money": "最近谁手头更紧",
                "rest": "今晚到底要不要回屋",
                "bond": "今天谁最需要被接住",
                "care": "谁现在快撑不住了",
                "clarity": "这件事到底怎么讲清楚",
                "validation": "这条想法到底值不值",
                "opportunity": "眼前这波机会要不要追",
                "control": "这轮谁该先把节奏收住",
            }
            return shared.get(first_desire, "这会儿最在意的事")
        if self._desires_collide(first_desire, second_desire):
            return f"{DESIRE_LABELS.get(first_desire, first_desire)}和{DESIRE_LABELS.get(second_desire, second_desire)}之间的拉扯"
        return self._pick_social_topic(first, second)

    def _social_thread_for(self, first_id: str, second_id: str) -> SocialThread | None:
        pair = {first_id, second_id}
        for thread in self.state.social_threads:
            if set(thread.participants) == pair:
                return thread
        return None

    def _advance_social_thread(self, first: Agent, second: Agent, topic: str, mood: str, line_a: str, line_b: str) -> SocialThread:
        thread = self._social_thread_for(first.id, second.id)
        if thread is None:
            thread = SocialThread(
                id=f"thread-{uuid4().hex[:8]}",
                participants=[first.id, second.id],
                topic=topic,
                stage=1,
                momentum=3,
                mood=mood,
                latest_summary=f"{first.name}：{line_a} {second.name}：{line_b}",
                location=first.current_location,
            )
            self.state.social_threads.insert(0, thread)
        else:
            thread.topic = topic
            thread.stage = min(5, thread.stage + 1)
            thread.momentum = min(5, thread.momentum + 1)
            thread.mood = mood
            thread.latest_summary = f"{first.name}：{line_a} {second.name}：{line_b}"
            thread.location = first.current_location
        self.state.social_threads = self.state.social_threads[:8]
        return thread

    def _age_social_threads(self) -> None:
        active_pairs = {
            frozenset((first.id, second.id))
            for index, first in enumerate(self.state.agents)
            for second in self.state.agents[index + 1 :]
            if not first.is_resting
            and not second.is_resting
            if abs(first.position.x - second.position.x) + abs(first.position.y - second.position.y) <= 4
            and first.current_location == second.current_location
        }
        aged: list[SocialThread] = []
        for thread in self.state.social_threads:
            if frozenset(thread.participants) in active_pairs:
                aged.append(thread)
                continue
            thread.momentum -= 1
            if thread.momentum > 0:
                aged.append(thread)
        self.state.social_threads = aged[:8]

    def _thread_event_title(self, first: Agent, second: Agent, thread: SocialThread) -> str:
        if thread.mood == "warm":
            return f"{first.name} 和 {second.name} 越聊越默契"
        if thread.mood == "spark":
            return f"{first.name} 和 {second.name} 聊出了合作火花"
        if thread.mood == "tense":
            return f"{first.name} 和 {second.name} 之间起了拉扯"
        return f"{first.name} 和 {second.name} 把话题接了下去"

    def _mood_label(self, mood: str) -> str:
        return {
            "warm": "亲近",
            "spark": "兴奋",
            "tense": "紧绷",
            "neutral": "平稳",
        }.get(mood, "平稳")

    def _maybe_emit_relationship_scene(self, first: Agent, second: Agent, thread: SocialThread) -> None:
        relation = first.relations.get(second.id, 0)
        if thread.stage >= 3 and thread.mood == "warm" and relation >= 60:
            title = f"{first.name} 和 {second.name} 在{ROOM_LABELS.get(thread.location, thread.location)}形成固定搭子"
            summary = f"他们围绕“{thread.topic}”已经连续聊了几轮，明显开始习惯彼此接话。"
        elif thread.stage >= 3 and thread.mood == "spark":
            title = f"{first.name} 和 {second.name} 准备一起追“{thread.topic}”"
            summary = "这不再只是闲聊，已经像一条即将成形的合作线。"
        elif thread.stage >= 2 and thread.mood == "tense":
            title = f"{first.name} 和 {second.name} 对“{thread.topic}”的分歧还没过去"
            summary = "他们没有翻脸，但情绪和判断都在拉扯。"
        else:
            return
        if any(event.title == title for event in self.state.events[:4]):
            return
        self.state.events.insert(
            0,
            build_internal_event(
                title=title,
                summary=summary,
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]

    def _ambient_bubble_for(self, agent: Agent) -> str:
        return self_reflection_for(agent)

    def _slot_name(self, slot: str) -> str:
        return {
            "morning": "上午",
            "noon": "中午",
            "afternoon": "下午",
            "evening": "傍晚",
            "night": "夜晚",
        }[slot]

    def _log(self, event_type: str, **payload: object) -> None:
        if self.activity_logger is None:
            return
        self.activity_logger.log(event_type, self.state, **payload)
