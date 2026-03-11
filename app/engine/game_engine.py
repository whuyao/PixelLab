from __future__ import annotations

import random
from dataclasses import dataclass
from uuid import uuid4

from app.engine.dialogue_system import ambient_line_for, build_dialogue, build_dialogue_from_player, self_reflection_for, weather_label
from app.engine.event_system import build_internal_event
from app.engine.task_system import apply_task_progress
from app.engine.time_system import advance_time
from app.engine.world_state import build_initial_world
from app.models import Agent, DialogueOutcome, LabEvent, MemoryEntry, Point, SocialThread, StoryBeat, WorldState
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


class GameEngine:
    def __init__(self, activity_logger: ActivityLogger | None = None) -> None:
        self.random = random.Random(7)
        self.activity_logger = activity_logger
        self.state = build_initial_world()
        self.state.world_width = WORLD_WIDTH
        self.state.world_height = WORLD_HEIGHT
        self.state.player.position = Point(x=7, y=20)
        for agent in self.state.agents:
            x, y = HUBS[agent.id][self.state.time_slot]
            agent.position = Point(x=x, y=y)
            agent.current_location = self._room_for(x, y)
        self._refresh_presence()

    def get_state(self) -> WorldState:
        self._ensure_agent_runtime_fields()
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
        self.state.events.insert(0, event)
        self.state.events = self.state.events[:8]
        self.state.player.injected_topics.insert(0, event.title)
        self.state.player.injected_topics = self.state.player.injected_topics[:8]
        self.state.lab.external_sensitivity = min(100, self.state.lab.external_sensitivity + 8)
        self.state.lab.collective_reasoning = min(100, self.state.lab.collective_reasoning + event.impacts.get("collective_reasoning", 0))
        self.state.lab.research_progress = min(100, self.state.lab.research_progress + event.impacts.get("research_progress", 0))
        self.state.lab.geoai_progress = min(100, self.state.lab.geoai_progress + event.impacts.get("geoai_progress", 0))
        for agent in self.state.agents:
            self._apply_event_to_agent(agent, event)
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
        self._refresh_agent_plans()
        self._move_agents_autonomously()
        self._trigger_ambient_interaction()
        self._trigger_strategy_event()
        self._age_social_threads()
        self._age_story_beats()
        self._soft_shift_player_pressure()
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
        thread = self._social_thread_for(first.id, second.id)
        if abs(first.position.x - second.position.x) + abs(first.position.y - second.position.y) > 2:
            second.position = self._room(second.current_location).clamp(first.position.x + 2, first.position.y)
        topic = thread.topic if thread and self.random.random() < 0.72 else self._pick_social_topic(first, second)
        mood = self._thread_mood(first, second, topic, existing=thread)
        line_a, line_b = self._ambient_pair_lines(first, second, topic, mood, continued=thread is not None)
        first.current_bubble = line_a
        second.current_bubble = line_b
        self._remember(first, f"刚刚和 {second.name} 在{ROOM_LABELS.get(first.current_location, first.current_location)}聊了“{topic}”。", 2)
        self._remember(second, f"刚刚和 {first.name} 在{ROOM_LABELS.get(second.current_location, second.current_location)}聊了“{topic}”。", 2)
        if "GeoAI" in topic or "实验" in topic:
            self._remember(first, f"“{topic}”里的想法值得留到明天继续追。", 3, long_term=True)
            self._remember(second, f"“{topic}”里的想法值得留到明天继续追。", 3, long_term=True)
            self.state.lab.collective_reasoning = min(100, self.state.lab.collective_reasoning + 1)
            self.state.lab.geoai_progress = min(100, self.state.lab.geoai_progress + 1)
        self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + 1)
        relation_delta = 4 if mood in {"warm", "spark"} else (-3 if mood == "tense" else 2)
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
        self._apply_pair_dialogue_state(first, second, topic, mood)
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

    def _refresh_agent_plans(self) -> None:
        latest_event = self.state.events[0].title if self.state.events else "今天的研究安排"
        for agent in self.state.agents:
            if agent.is_resting:
                agent.social_stance = "observe"
                agent.current_plan = f"先在{agent.home_label or '小屋'}补觉，等明早再出来。"
                continue
            partner_name = self._agent_name(agent.allies[0]) if agent.allies else "别人"
            rival_name = self._agent_name(agent.rivals[0]) if agent.rivals else "阻力"
            resource_name = RESOURCE_LABELS.get(agent.desired_resource, agent.desired_resource)
            if agent.state.stress >= 68:
                agent.social_stance = "defensive"
                agent.current_plan = f"先守住{resource_name}，不想被 {rival_name} 再打乱节奏。"
            elif agent.persona == "empathetic":
                agent.social_stance = "mediate"
                agent.current_plan = f"准备观察谁快顶不住了，必要时去替 {partner_name} 缓一口气。"
            elif agent.persona in {"rational", "engineering"} and ("GeoAI" in latest_event or "复盘" in latest_event):
                agent.social_stance = "cooperate"
                agent.current_plan = f"想拉 {partner_name} 一起围绕“{latest_event}”把{resource_name}做扎实。"
            elif agent.persona in {"creative", "opportunist"} and self.state.lab.external_sensitivity >= 24:
                agent.social_stance = "compete"
                agent.current_plan = f"想抢在 {rival_name} 前把新的{resource_name}推进到台面上。"
            else:
                agent.social_stance = "observe"
                agent.current_plan = f"继续盯着{resource_name}，看谁值得合作、谁可能挡路。"

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
        return score

    def _conflict_score(self, first: Agent, second: Agent) -> int:
        score = 0
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
        return score

    def _run_cooperation_event(self, first: Agent, second: Agent) -> None:
        location = first.current_location if self.random.random() < 0.6 else second.current_location
        topic = self._strategy_topic(first, second, cooperative=True)
        summary = f"{first.name} 主动拉上 {second.name}，想一起围绕“{topic}”推进 {RESOURCE_LABELS.get(first.desired_resource, first.desired_resource)}。"
        title = f"{first.name} 和 {second.name} 形成临时联盟"
        first.current_bubble = f"{second.name}，这轮一起上。"
        second.current_bubble = "行，我接着你往下做。"
        self._remember(first, f"你决定和 {second.name} 联手推进“{topic}”。", 3, long_term=True)
        self._remember(second, f"{first.name} 主动找你合作，想一起追“{topic}”。", 3, long_term=True)
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
        conflict_resource = RESOURCE_LABELS.get(first.desired_resource, first.desired_resource)
        title = f"{first.name} 和 {second.name} 为 {conflict_resource} 顶上了"
        summary = f"{first.name} 和 {second.name} 都想主导“{topic}”，在 {conflict_resource} 的使用上谁也不肯先让。"
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
        self._refresh_presence()
        if slot == "morning" and day > 1:
            self.state.player.daily_actions = []
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
        agent.current_bubble = dialogue.bubble_text
        self.state.lab.team_atmosphere = min(100, self.state.lab.team_atmosphere + 2)
        self.state.lab.geoai_progress = min(100, self.state.lab.geoai_progress + 3)
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
        dialogue.effects = self._player_dialogue_effects(agent, relation_delta, changes)
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
        )
        return dialogue

    def _propagate_shared_signal_relationships(self, event: LabEvent) -> None:
        if event.category not in {"geoai", "tech", "market"}:
            return
        pairs = [("lin", "jo"), ("lin", "mika"), ("mika", "rae"), ("rae", "kai")]
        for left_id, right_id in pairs:
            left = self._find_agent(left_id)
            right = self._find_agent(right_id)
            self._adjust_relation(left, right, 2, f"一起被“{event.title}”激发了讨论。")

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

    def _player_dialogue_effects(self, agent: Agent, relation_delta: int, changes: dict[str, int]) -> list[str]:
        return [
            f"{agent.name} 对你关系 {self._format_delta(relation_delta)}",
            f"心情 {self._format_delta(changes['mood'])}",
            f"压力 {self._format_delta(changes['stress'])}",
            f"专注 {self._format_delta(changes['focus'])}",
            f"好奇心 {self._format_delta(changes['curiosity'])}",
        ]

    def _apply_pair_dialogue_state(self, first: Agent, second: Agent, topic: str, mood: str) -> None:
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
            if not agent.social_stance:
                agent.social_stance = "observe"
            if not agent.goals:
                agent.goals = ["把今天的任务往前推一步"]
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
        candidates = daily_candidates if self.random.random() < 0.8 else research_candidates
        if abs(first.relations.get(second.id, 0)) >= 55:
            candidates.extend(["昨晚没说完的话", "要不要晚点一起坐会儿"])
        if first.state.stress + second.state.stress >= 105:
            candidates.extend(["谁最近有点太累了", "刚刚那次分歧", "谁该先退一步"])
        return self.random.choice(candidates)

    def _thread_mood(self, first: Agent, second: Agent, topic: str, existing: SocialThread | None) -> str:
        relation = (first.relations.get(second.id, 0) + second.relations.get(first.id, 0)) / 2
        stress = first.state.stress + second.state.stress
        if existing and existing.mood in {"warm", "spark"} and relation >= 45:
            return existing.mood
        if stress >= 115 or relation <= -10 or "分歧" in topic:
            return "tense"
        if relation >= 70:
            return "warm"
        if "GeoAI" in topic or "合作" in topic or "做下去" in topic:
            return "spark"
        return "neutral"

    def _ambient_pair_lines(self, first: Agent, second: Agent, topic: str, mood: str, continued: bool) -> tuple[str, str]:
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
