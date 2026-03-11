from __future__ import annotations

import random
import re
from dataclasses import dataclass
from uuid import uuid4

from app.engine.dialogue_system import (
    DESIRE_LABELS,
    ambient_line_for,
    build_dialogue,
    build_dialogue_from_player,
    desire_label_for_agent,
    dominant_desire_for_agent,
    self_reflection_for,
    weather_label,
)
from app.engine.event_system import build_internal_event
from app.engine.task_system import apply_task_progress
from app.engine.time_system import advance_time
from app.engine.world_state import build_initial_world
from app.models import Agent, DialogueOutcome, DialogueRecord, IndexCandle, LabEvent, LoanRecord, MemoryEntry, Point, SocialThread, StoryBeat, WorldState
from app.services.activity_logger import ActivityLogger


WORLD_WIDTH = 44
WORLD_HEIGHT = 26


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
    Room("pond", 30, 15, 34, 18),
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
    "lin": (9, 3, "Lin 的木屋"),
    "mika": (11, 23, "Mika 的木屋"),
    "jo": (21, 3, "Jo 的木屋"),
    "rae": (29, 23, "Rae 的木屋"),
    "kai": (38, 3, "Kai 的木屋"),
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
GEOAI_MILESTONES = [50, 100, 180, 260, 360, 500, 700, 950]


class GameEngine:
    def __init__(self, state: WorldState | None = None, activity_logger: ActivityLogger | None = None) -> None:
        self.random = random.Random(7)
        self.activity_logger = activity_logger
        is_new_world = state is None
        self.state = state or build_initial_world()
        self.state.world_width = WORLD_WIDTH
        self.state.world_height = WORLD_HEIGHT
        if is_new_world:
            self.state.player.position = Point(x=7, y=20)
            for agent in self.state.agents:
                x, y = HUBS[agent.id][self.state.time_slot]
                agent.position = Point(x=x, y=y)
                agent.current_location = self._room_for(x, y)
        self._refresh_presence()

    def get_state(self) -> WorldState:
        self._ensure_agent_runtime_fields()
        self._sync_market_clock()
        self._refresh_market_regime(force_roll=False)
        self._refresh_sector_rotation(force_roll=False)
        self._update_index_history(append=False)
        self._update_daily_index_history()
        self._refresh_tasks()
        self._refresh_agent_plans()
        self._refresh_memory_streams()
        return self.state

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
        agent = self._find_agent(agent_id)
        dialogue = build_dialogue(self.state, agent)
        return self._commit_dialogue(agent, dialogue, reason="和玩家单独聊了一次。")

    def player_trade(self, symbol: str, side: str, shares: int) -> WorldState:
        self._sync_market_clock()
        if not self.state.market.is_open:
            raise ValueError("现在已经收盘了，等白天再交易。")
        self._execute_trade_for_player(symbol.upper(), side, shares, manual=True)
        self._refresh_tasks()
        return self.state

    def auto_trade_player(self) -> WorldState:
        self._sync_market_clock()
        if not self.state.market.is_open:
            return self.state
        symbol, side, shares, reason = self._decide_player_trade()
        self._execute_trade_for_player(symbol, side, shares, manual=False, reason=reason)
        self._refresh_tasks()
        return self.state

    def speak_to_agent(self, agent_id: str, player_text: str) -> DialogueOutcome:
        agent = self._find_agent(agent_id)
        distance = abs(agent.position.x - self.state.player.position.x) + abs(agent.position.y - self.state.player.position.y)
        if distance > 2:
            raise ValueError(f"{agent.name} 离你有点远，先靠近再聊天。")
        text = player_text.strip()
        if not text:
            raise ValueError("先输入一句你想说的话。")
        dialogue = build_dialogue_from_player(self.state, agent, text)
        return self._commit_dialogue(agent, dialogue, reason=f"玩家主动说了：{text}")

    def commit_external_dialogue(self, agent_id: str, dialogue: DialogueOutcome, player_text: str) -> DialogueOutcome:
        agent = self._find_agent(agent_id)
        distance = abs(agent.position.x - self.state.player.position.x) + abs(agent.position.y - self.state.player.position.y)
        if distance > 2:
            raise ValueError(f"{agent.name} 离你有点远，先靠近再聊天。")
        text = player_text.strip()
        if not text:
            raise ValueError("先输入一句你想说的话。")
        dialogue.player_text = text
        dialogue.agent_id = agent.id
        dialogue.agent_name = agent.name
        if not dialogue.topic:
            dialogue.topic = text[:36]
        if not dialogue.bubble_text:
            dialogue.bubble_text = dialogue.line[:18]
        if not dialogue.effects:
            dialogue.effects = [
                f"{agent.name} 好感 +6",
                "GeoAI 进度 +3",
                "知识库 +2",
            ]
        return self._commit_dialogue(agent, dialogue, reason=f"玩家主动说了：{text}")

    def get_agent(self, agent_id: str) -> Agent:
        return self._find_agent(agent_id)

    def inject_event(self, event: LabEvent) -> WorldState:
        return self._ingest_event(event, player_injected=True)

    def _ingest_event(self, event: LabEvent, player_injected: bool) -> WorldState:
        self.state.events.insert(0, event)
        self.state.events = self.state.events[:8]
        if player_injected:
            self.state.player.injected_topics.insert(0, event.title)
            self.state.player.injected_topics = self.state.player.injected_topics[:8]
        self.state.lab.external_sensitivity = min(100, self.state.lab.external_sensitivity + 8)
        self.state.lab.collective_reasoning = min(100, self.state.lab.collective_reasoning + event.impacts.get("collective_reasoning", 0))
        self.state.lab.research_progress = min(100, self.state.lab.research_progress + event.impacts.get("research_progress", 0))
        self._advance_geoai_progress(event.impacts.get("geoai_progress", 0), reason=event.title)
        for agent in self.state.agents:
            self._apply_event_to_agent(agent, event)
        self._apply_event_to_market(event)
        apply_task_progress(self.state.tasks, "news")
        self._propagate_shared_signal_relationships(event)
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
        self._sync_market_clock()
        self._refresh_agent_plans()
        self._update_market_intraday()
        self._maybe_generate_system_news()
        self._move_agents_autonomously()
        self._trigger_market_activity()
        self._trigger_ambient_interaction()
        self._trigger_strategy_event()
        self._settle_due_loans()
        self._age_social_threads()
        self._age_story_beats()
        self._soft_shift_player_pressure()
        self._refresh_tasks()
        self._refresh_memory_streams()
        self._log("world_simulation_tick")
        return self.state

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
            room = self._room(agent.current_location)
            target_x = hub_x + self.random.randint(-2, 2)
            target_y = hub_y + self.random.randint(-1, 1)
            target = self._nearest_walkable(room.clamp(target_x, target_y), room)
            step_x = 0 if target.x == agent.position.x else (1 if target.x > agent.position.x else -1)
            step_y = 0 if target.y == agent.position.y else (1 if target.y > agent.position.y else -1)
            prefer_x = abs(target.x - agent.position.x) >= abs(target.y - agent.position.y)
            options: list[tuple[int, int]] = []
            if step_x != 0 or step_y != 0:
                if prefer_x:
                    options.extend([(step_x, 0), (0, step_y), (step_x, step_y)])
                else:
                    options.extend([(0, step_y), (step_x, 0), (step_x, step_y)])
            options.extend(
                [
                    (step_x, 0),
                    (0, step_y),
                    (0, 0),
                ]
            )
            agent.position = self._move_in_room(agent.position, room, options)
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
        line_a, line_b = self._ambient_pair_lines(first, second, topic, mood, continued=thread is not None, first_desire=first_desire, second_desire=second_desire)
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
        financial_outcome = self._apply_pair_dialogue_state(first, second, topic, mood)
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
                summary=f"{first.name} 和 {second.name} 在{ROOM_LABELS.get(first.current_location, first.current_location)}围绕“{topic}”接了一轮，整体气氛偏{self._mood_label(mood)}。",
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
                summary=f"他们在{ROOM_LABELS.get(first.current_location, first.current_location)}围绕“{topic}”继续聊。当前气氛偏{self._mood_label(mood)}。",
                slot=self.state.time_slot,
                category="general",
            ),
        )
        self.state.events = self.state.events[:8]
        self._maybe_emit_relationship_scene(first, second, thread)

    def _soft_shift_player_pressure(self) -> None:
        if self.random.random() < 0.22:
            self.state.lab.research_progress = min(100, self.state.lab.research_progress + 1)
        if self.random.random() < 0.16:
            self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + 1)
        for thread in self.state.social_threads[:]:
            if thread.momentum <= 0:
                self.state.social_threads.remove(thread)

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
        if agent.cash < 10:
            pressure = max(pressure, 96)
        elif agent.cash < 25:
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
        return agent.cash + holdings_value

    def _team_net_worth(self) -> int:
        return sum(self._agent_net_worth(agent) for agent in self.state.agents)

    def _team_cash_total(self) -> int:
        return sum(agent.cash for agent in self.state.agents)

    def _market_index_from_quotes(self) -> float:
        if not self.state.market.stocks:
            return self.state.market.index_value
        ratio = sum(quote.price / quote.open_price for quote in self.state.market.stocks) / len(self.state.market.stocks)
        value = 100.0 * ratio + (self.state.market.sentiment / 12)
        return round(max(40.0, value), 2)

    def _update_index_history(self, limit_state: str = "normal", append: bool = True) -> None:
        value = self._market_index_from_quotes()
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
        value = self._market_index_from_quotes()
        history = self.state.market.daily_index_history or []
        if not history:
            self.state.market.daily_index_history = [IndexCandle(day=self.state.day, open=value, high=value, low=value, close=value, limit_state=limit_state)]
            return
        candle = history[-1]
        if candle.day != self.state.day:
            self.state.market.daily_index_history.append(
                IndexCandle(day=self.state.day, open=value, high=value, low=value, close=value, limit_state=limit_state)
            )
            self.state.market.daily_index_history = self.state.market.daily_index_history[-30:]
            return
        candle.close = value
        candle.high = max(candle.high, value)
        candle.low = min(candle.low, value)
        if limit_state != "normal":
            candle.limit_state = limit_state

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
        team_cash = self._team_cash_total()
        baseline = 500
        target_total = 650
        for task in self.state.tasks:
            if task.id == "task-geo-baseline":
                progress = int(max(0, min(100, ((team_cash - baseline) / max(1, target_total - baseline)) * 100)))
                task.progress = progress
                task.description = f"把团队总现金从 $500 慢慢推到 $650。当前团队现金约 ${team_cash}，重点靠明确借贷回款、白天兑现收益和稳健协作。"
            elif task.id == "task-news":
                task.description = "注入一条真正会影响市场或团队情绪的外部信息，让股价和大家的判断发生波动。"
        self._archive_completed_tasks()

    def _archive_completed_tasks(self) -> None:
        active: list = []
        for task in self.state.tasks:
            if task.progress < task.target:
                active.append(task)
                continue
            if task.completed_day is None:
                task.completed_day = self.state.day
                task.archived_note = f"第 {self.state.day} 天完成，已转入归档。"
                self.state.events.insert(
                    0,
                    build_internal_event(
                        title=f"任务完成：{task.title}",
                        summary=f"{task.title} 已达成，现已归档。",
                        slot=self.state.time_slot,
                        category="general",
                    ),
                )
                self.state.events = self.state.events[:8]
            if not any(existing.id == task.id for existing in self.state.archived_tasks):
                self.state.archived_tasks.insert(0, task.model_copy(deep=True))
        self.state.archived_tasks = self.state.archived_tasks[:12]
        self.state.tasks = active

    def _refresh_agents_for_new_day(self) -> None:
        weather_bonus = {"sunny": 3, "breezy": 2, "cloudy": 0, "drizzle": -1}[self.state.weather]
        for agent in self.state.agents:
            if agent.is_resting:
                continue
            loan_load = sum(1 for loan in self.state.loans if loan.status in {"active", "overdue"} and loan.borrower_id == agent.id)
            agent.state.mood = self._bounded(agent.state.mood + weather_bonus + (1 if agent.credit_score >= 75 else -2 if agent.credit_score <= 35 else 0))
            agent.state.stress = self._bounded(agent.state.stress - 4 + loan_load * 2)
            agent.state.focus = self._bounded(agent.state.focus + 2 - (2 if loan_load else 0))
            agent.state.curiosity = self._bounded(agent.state.curiosity + (2 if self.state.market.is_open else 0))
            agent.current_bubble = "新一天开始了。"
            agent.last_interaction = f"第 {self.state.day} 天开始，正在重新判断今天该靠近谁。"
            self._remember(agent, f"第 {self.state.day} 天开始了。天气是{weather_label(self.state.weather)}，你在重新判断今天的节奏。", 2)
        self._log("daily_agent_refresh", day=self.state.day, weather=self.state.weather)

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
        team_support = 0.22 if self._team_net_worth() <= 620 else 0.0
        regime_bias = {
            "bull": {"base": 0.34, "down_chance": 0.08, "down_range": (-1.8, -0.6), "up_chance": 0.22, "up_range": (1.1, 2.8)},
            "sideways": {"base": 0.04, "down_chance": 0.12, "down_range": (-1.9, -0.7), "up_chance": 0.16, "up_range": (0.9, 2.0)},
            "risk": {"base": -0.22, "down_chance": 0.22, "down_range": (-2.7, -1.1), "up_chance": 0.08, "up_range": (0.7, 1.8)},
        }[regime]
        base_sentiment = regime_bias["base"] + (self.state.market.sentiment / 85) + team_support
        weather_bias = {"sunny": 0.10, "breezy": 0.04, "cloudy": -0.06, "drizzle": -0.16}[self.state.weather]
        shock_roll = self.random.random()
        if shock_roll < regime_bias["down_chance"]:
            market_shock = self.random.uniform(*regime_bias["down_range"])
        elif shock_roll > 1 - regime_bias["up_chance"]:
            market_shock = self.random.uniform(*regime_bias["up_range"])
        else:
            market_shock = 0.0
        for quote in self.state.market.stocks:
            sector_bias = {
                "GEO": 0.28 if self.state.lab.geoai_progress >= 30 else 0.04,
                "AGR": 0.26 if self.state.weather in {"sunny", "breezy"} else -0.08,
                "SIG": 0.24 if self.state.lab.external_sensitivity >= 25 else 0.02,
            }.get(quote.symbol, 0.0)
            rotation_bias = 0.62 if quote.symbol == leader else -0.18
            if regime == "risk" and quote.symbol == "AGR":
                rotation_bias += 0.22
            if regime == "bull" and quote.symbol == "SIG" and leader != "SIG":
                rotation_bias += 0.08
            mean_reversion = -(quote.day_change_pct / 2.6)
            extension_pull = 0.0
            if quote.day_change_pct >= 5.5:
                extension_pull -= self.random.uniform(1.0, 2.2)
            elif quote.day_change_pct <= -5.5:
                extension_pull += self.random.uniform(1.1, 2.4)
            support_bid = 0.0
            if self.state.market.index_value < 99:
                support_bid += 0.35
            if quote.day_change_pct <= -4.5:
                support_bid += 0.95
            regime_pull = 0.22 if regime == "bull" else (-0.28 if regime == "risk" else 0.0)
            drift = self.random.uniform(-1.8, 1.55) + market_shock + base_sentiment + weather_bias + sector_bias + rotation_bias + mean_reversion + extension_pull + support_bid + regime_pull
            self._apply_quote_move(quote.symbol, max(-4.2, min(4.2, drift)), "白天盘中波动")
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
        self._update_index_history(limit_state=limit_state)
        self._update_daily_index_history(limit_state=limit_state)

    def _trigger_market_activity(self) -> None:
        if not self.state.market.is_open:
            return
        for agent in self.state.agents:
            if agent.is_resting or self.random.random() >= 0.10:
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
            preferred_symbol = max(self.state.market.stocks, key=lambda quote: quote.change_pct).symbol
        quote = self._quote(preferred_symbol) or self.state.market.stocks[0]
        held = agent.portfolio.get(quote.symbol, 0)
        signal = quote.change_pct + (self.state.market.sentiment / 28) + ((agent.risk_appetite - 50) / 40)
        if held > 0 and (quote.change_pct <= -1.6 or (pressure >= 80 and agent.cash < 25) or quote.day_change_pct >= 3.8):
            return (quote.symbol, "sell", min(held, max(1, 1 + held // 2)), "走势不稳，或者得先把现金留出来。")
        if signal <= 0.35 or agent.cash < quote.price:
            return None
        budget = max(quote.price, min(agent.cash, 12 + agent.risk_appetite // 4 + pressure // 6))
        shares = int(budget // quote.price)
        shares = max(1, min(3, shares))
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
        self._shift_agent_state(agent, mood=1 if side == "buy" else 0, stress=1 if side == "buy" else -1, curiosity=1)
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
        self._refresh_tasks()
        return True

    def _decide_player_trade(self) -> tuple[str, str, int, str]:
        if not self.state.market.stocks:
            return ("GEO", "buy", 0, "暂无盘面")
        preferred = max(self.state.market.stocks, key=lambda quote: quote.change_pct + quote.day_change_pct * 0.4)
        held = self.state.player.portfolio.get(preferred.symbol, 0)
        if held > 0 and (preferred.day_change_pct >= 4.8 or preferred.change_pct <= -2.0):
            return (preferred.symbol, "sell", min(held, 2), "观察模式下先做一次止盈或止损。")
        if self.state.player.cash >= preferred.price:
            budget = min(self.state.player.cash, 18 + self.state.player.risk_appetite // 3)
            shares = max(1, min(3, int(budget // preferred.price)))
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
            if agent.short_term_memory:
                items.append(f"刚记住：{agent.short_term_memory[0].text}")
            if agent.long_term_memory:
                items.append(f"长线挂念：{agent.long_term_memory[0].text}")
            thread = next((thread for thread in self.state.social_threads if agent.id in thread.participants), None)
            if thread:
                items.append(f"最近对话线：{thread.latest_summary}")
            else:
                items.append(f"外部场景：{latest_event}")
            if agent.current_plan:
                items.append(f"当前打算：{agent.current_plan}")
            agent.memory_stream = items[:6]

    def _trigger_strategy_event(self) -> None:
        if self.random.random() > 0.58:
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
        day, slot = advance_time(self.state.day, self.state.time_slot)
        self.state.day = day
        self.state.time_slot = slot
        self.state.weather = self._roll_weather()
        self._sync_market_clock()
        if slot == "morning":
            self.state.market.sentiment = int(self.state.market.sentiment * 0.6)
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
        self._refresh_presence()
        self._refresh_memory_streams()
        self._refresh_tasks()
        if slot == "morning" and day > 1:
            self.state.player.daily_actions = []
            self._refresh_agents_for_new_day()
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

    def _find_agent(self, agent_id: str) -> Agent:
        for agent in self.state.agents:
            if agent.id == agent_id:
                return agent
        raise KeyError(f"未知角色：{agent_id}")

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
            self._remember(agent, f"“{event.title}”可能改变实验室接下来的讨论方向。", importance=3, long_term=True)
        event_bubble = {
            "geoai": "这条信息值得继续推演。",
            "tech": "也许要调整实验方案。",
            "market": "这条外部波动会影响大家情绪。",
            "gaming": "休息区今晚肯定会聊这个。",
            "general": "这消息能带来一点新鲜空气。",
        }
        agent.current_bubble = event_bubble.get(event.category, "这条消息值得留意。")

    def _commit_dialogue(self, agent: Agent, dialogue: DialogueOutcome, reason: str) -> DialogueOutcome:
        self.state.latest_dialogue = dialogue
        self.state.ambient_dialogues.insert(0, dialogue)
        self.state.ambient_dialogues = self.state.ambient_dialogues[:6]
        relation_delta, changes = self._apply_player_dialogue_impact(agent, dialogue)
        self._adjust_player_relation(agent, relation_delta, reason)
        money_effects = self._resolve_player_money_exchange(agent, dialogue, relation_delta)
        agent.current_bubble = dialogue.bubble_text
        self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + 2)
        self._advance_geoai_progress(3, reason=dialogue.topic or "玩家对话")
        self.state.lab.knowledge_base = min(100, self.state.lab.knowledge_base + 2)
        topic = dialogue.topic or "今天的聊天"
        self._remember(agent, f"你在{self._slot_name(self.state.time_slot)}和玩家聊了“{topic}”。", importance=2)
        if dialogue.player_text:
            self._remember(agent, f"玩家刚刚说：“{dialogue.player_text}”", importance=2)
        self._remember(agent, f"你刚刚回复玩家：“{dialogue.line[:72]}”", importance=2)
        if agent.persona in {"rational", "creative"}:
            self._remember(agent, f"关于“{topic}”的讨论值得继续追。", importance=3, long_term=True)
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
        dialogue.effects = self._player_dialogue_effects(agent, relation_delta, changes) + money_effects
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
                summary=f"你先抛出“{dialogue.player_text or '一段试探'}”，{agent.name} 的回应是：“{dialogue.line}”",
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
        self.state.dialogue_history = self.state.dialogue_history[:200]

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
        crossed = [threshold for threshold in GEOAI_MILESTONES if previous < threshold <= current and threshold not in self.state.geoai_milestones]
        if not crossed:
            return
        for threshold in crossed:
            self.state.geoai_milestones.append(threshold)
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
        if financial_note:
            return f"这轮话已经落成了资源动作：{financial_note}"
        if mood == "tense":
            return f"{first_name} 更受“{first_desire}”驱动，{second_name} 更受“{second_desire}”驱动，分歧已经摆到明面上。"
        if mood in {"warm", "spark"} and first_desire == second_desire:
            return f"两个人都在惦记“{first_desire}”，所以这轮更容易迅速站到一边。"
        if mood in {"warm", "spark"}:
            return f"他们虽然各有侧重，但都愿意继续接“{topic}”这条线。"
        return f"这轮主要是在摸彼此对“{topic}”的真实取向。"

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

    def _is_blocked(self, x: int, y: int) -> bool:
        return any(obstacle.contains(x, y) for obstacle in OBSTACLES)

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
            agent.long_term_memory.insert(0, entry)
            agent.long_term_memory = agent.long_term_memory[:5]

    def _adjust_relation(self, first: Agent, second: Agent, delta: int, reason: str) -> None:
        previous = first.relations.get(second.id, 0)
        updated = max(-100, min(100, previous + delta))
        first.relations[second.id] = updated
        second.relations[first.id] = max(-100, min(100, second.relations.get(first.id, 0) + delta))
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

    def _adjust_player_relation(self, agent: Agent, delta: int, reason: str) -> None:
        previous = agent.relations.get("player", 0)
        updated = max(-100, min(100, previous + delta))
        agent.relations["player"] = updated
        self.state.player.social_links[agent.id] = updated
        if previous < 40 <= updated:
            self._remember(agent, f"你对玩家的好感明显提高了。原因是{reason}", 3, long_term=True)
        if previous < 65 <= updated:
            self._remember(agent, f"你开始期待下一次和玩家单独聊天。", 4, long_term=True)

    def _apply_player_dialogue_impact(self, agent: Agent, dialogue: DialogueOutcome) -> tuple[int, dict[str, int]]:
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
        changes = {
            "mood": max(-9, min(8, resonance + support + constructive - pressure * 2 - hostility * 3 - dominance)),
            "stress": max(-6, min(9, pressure * 2 + hostility * 3 + dominance - support - (1 if constructive > 0 else 0))),
            "focus": max(-5, min(6, inquiry + (1 if agent.persona in {"rational", "engineering"} else 0) - hostility - (1 if support > inquiry + 1 else 0))),
            "energy": max(-4, min(3, -1 + support + constructive - pressure - hostility * 2)),
            "curiosity": max(-4, min(7, resonance + inquiry + constructive - hostility)),
            "geo_reasoning_skill": 1 if self._is_geoai_topic(player_text) and hostility == 0 else 0,
        }
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
    ) -> dict[str, object] | None:
        explicit_gray_request = any(token in request_line for token in ["私下", "别挂到账", "别摆到台面", "灰色", "非正式"])
        explicit_gray_offer = any(token in response_line for token in ["私下给你", "先别挂账", "这笔先不摆到台面", "非正式资源交换", "别往外说"])
        if explicit_gray_request and explicit_gray_offer and donor.cash > 0:
            amount = self._extract_money_amount(f"{request_line}{response_line}") or max(5, requester.money_urgency // 18)
            relation = (donor.relations.get(requester.id, 0) + requester.relations.get(donor.id, 0)) / 2
            judgement = self._loan_judgement_score(donor, requester, amount) + int(relation // 3)
            if mood == "tense":
                judgement -= 8
            if judgement < 34 or relation < 18:
                return None
            amount = min(amount, donor.cash)
            if amount <= 0:
                return None
            donor.cash -= amount
            requester.cash += amount
            self._remember(requester, f"{donor.name} 刚私下塞给你 ${amount}，算一笔不公开的资源交换。", 2)
            self._remember(donor, f"你刚私下给了 {requester.name} ${amount}，这笔没有摆到公开台面上。", 2)
            self._adjust_relation(requester, donor, 1, f"围绕“{topic}”完成了一次不公开的资源交换。")
            self._log(
                "agent_gray_trade",
                trade={"from": donor.id, "to": requester.id, "amount": amount, "topic": topic},
            )
            return {"note": f"{donor.name} 和 {requester.name} 做了一笔非正式资源交换 ${amount}", "interest_rate": None, "gray_trade": True}
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

    def _apply_pair_dialogue_state(self, first: Agent, second: Agent, topic: str, mood: str) -> dict[str, object] | None:
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
        transferred = self._resolve_pair_money_exchange(first, second, topic, mood)
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

    def _resolve_pair_money_exchange(self, first: Agent, second: Agent, topic: str, mood: str) -> dict[str, object] | None:
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
        first_to_second = self._ambient_money_exchange(first, second, left_line, right_line, topic, mood)
        if first_to_second is not None:
            return first_to_second
        second_to_first = self._ambient_money_exchange(second, first, right_line, left_line, topic, mood)
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
            if "小屋" in agent.current_activity:
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

    def _ensure_agent_runtime_fields(self) -> None:
        if self.state.loans is None:
            self.state.loans = []
        if self.state.archived_tasks is None:
            self.state.archived_tasks = []
        if self.state.dialogue_history is None:
            self.state.dialogue_history = []
        if self.state.geoai_milestones is None:
            self.state.geoai_milestones = []
        for agent in self.state.agents:
            if agent.home_position is None:
                home = HOME_SPOTS.get(agent.id)
                if home is not None:
                    agent.home_position = Point(x=home[0], y=home[1])
                    agent.home_label = home[2]
            if not agent.home_label and agent.id in HOME_SPOTS:
                agent.home_label = HOME_SPOTS[agent.id][2]
            if not agent.current_plan:
                agent.current_plan = "继续观察当前局面，等待合适的合作或冲突时机。"
            if not agent.immediate_intent:
                agent.immediate_intent = "想先听听周围在聊什么。"
            if not agent.social_stance:
                agent.social_stance = "observe"
            if agent.cash <= 0:
                agent.cash = 0
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
            if agent.portfolio is None:
                agent.portfolio = {}
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
        if self.state.player.portfolio is None:
            self.state.player.portfolio = {}
        if self.state.player.last_trade_summary is None:
            self.state.player.last_trade_summary = ""
        if not self.state.player.risk_appetite:
            self.state.player.risk_appetite = 52
        if self.state.market.index_history is None:
            self.state.market.index_history = []
        if self.state.market.daily_index_history is None:
            self.state.market.daily_index_history = []
        if not self.state.market.regime:
            self.state.market.regime = "bull"
        if not self.state.market.regime_age:
            self.state.market.regime_age = 1
        if not self.state.market.rotation_leader:
            self.state.market.rotation_leader = "GEO"
        if not self.state.market.rotation_age:
            self.state.market.rotation_age = 1

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

    def _ambient_pair_lines(self, first: Agent, second: Agent, topic: str, mood: str, continued: bool, first_desire: str, second_desire: str) -> tuple[str, str]:
        pair_relation = (first.relations.get(second.id, 0) + second.relations.get(first.id, 0)) / 2
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
                return left, right
            left = f"我手里那条线可以先给你，但这笔先别挂账，你私下拿 {amount} 美元来换。"
            right = f"可以，这笔先走非正式资源交换，${amount} 我先给你。"
            return left, right
        if any(keyword in topic for keyword in ["预算", "股票", "借点", "周转"]):
            amount = max(4, max(first.money_urgency, second.money_urgency) // 20)
            if first.money_urgency >= second.money_urgency:
                interest = self._proposed_interest_rate(first)
                request_line = f"我手头有点紧，能不能先借我 {amount} 美元周转一下？我明天还你，利息 {interest}%。"
                if self._loan_judgement_score(second, first, amount + max(1, round(amount * interest / 100))) >= 28 and second.cash >= amount:
                    response_line = f"行，我借你 {amount} 美元，明天按 {interest}% 收回来。"
                else:
                    response_line = "我这边得先看看你明天拿什么还，这笔今天先不借。"
                return request_line, response_line
            interest = self._proposed_interest_rate(second)
            offer_line = f"你要是真缺口不大，我可以先借你 {amount} 美元，你明天按 {interest}% 还。"
            if second.cash < 10:
                response_line = f"行，那你先借我 {amount} 美元，我明天按 {interest}% 还你。"
            else:
                response_line = "我先不借，今天更想自己扛一下。"
            return offer_line, response_line
        if self._desires_collide(first_desire, second_desire):
            left = f"我现在更想先顾“{DESIRE_LABELS.get(first_desire, first_desire)}”，因为我已经没有余裕再分神了，你别总把话拽去“{DESIRE_LABELS.get(second_desire, second_desire)}”。"
            right = f"可我眼下最在意的就是“{DESIRE_LABELS.get(second_desire, second_desire)}”，你别像没看见一样。我不是故意顶你，是我真的先顾不上别的。"
            return left, right
        if first_desire == second_desire:
            shared = DESIRE_LABELS.get(first_desire, first_desire)
            left = f"我感觉你也在惦记“{shared}”，所以我刚才那句你应该听得懂。"
            right = f"对，我这会儿也想先把“{shared}”稳住，不然今天后面整个人都要散。"
            return left, right
        left_seed = ambient_line_for(first, topic)
        right_seed = ambient_line_for(second, topic)
        if continued:
            left_seed = f"{left_seed[:-1]}，我还是想把刚才那句说完。"
        if mood == "tense":
            left = f"{left_seed[:-1]}，但我不同意把问题带过去。"
            right = f"{right_seed[:-1]}，你别只盯着一个点。"
            return left, right
        if mood == "warm":
            left = f"{left_seed[:-1]}，要不我们还是并肩把它做完。"
            right = f"{right_seed[:-1]}，行，我跟你站一边。"
            return left, right
        if mood == "spark":
            left = f"{left_seed[:-1]}，这条线也许真能一起做大。"
            right = f"{right_seed[:-1]}，那我继续往前接。"
            return left, right
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
        return left, right

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
