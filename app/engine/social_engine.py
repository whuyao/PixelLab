from __future__ import annotations

from typing import TYPE_CHECKING

from app.engine.dialogue_system import build_dialogue, build_dialogue_from_player
from app.models import DialogueOutcome, LabEvent, WorldState

if TYPE_CHECKING:
    from app.engine.game_engine import GameEngine


class SocialEngine:
    def __init__(self, host: "GameEngine") -> None:
        self.host = host

    def prepare_view(self) -> WorldState:
        self.host._refresh_agent_plans()
        self.host._refresh_memory_streams()
        return self.host.state

    def handle_event(self, event: LabEvent) -> WorldState:
        for agent in self.host.state.agents:
            self.host._apply_event_to_agent(agent, event)
        self.host._propagate_shared_signal_relationships(event)
        return self.host.state

    def run_tick(self) -> WorldState:
        self.host._trigger_ambient_interaction()
        self.host._trigger_strategy_event()
        self.host._age_social_threads()
        self.host._age_story_beats()
        self.host._refresh_memory_streams()
        return self.host.state

    def interact_with_agent(self, agent_id: str) -> DialogueOutcome:
        agent = self.host._find_agent(agent_id)
        dialogue = build_dialogue(self.host.state, agent)
        return self.host._commit_dialogue(agent, dialogue, reason="和玩家单独聊了一次。")

    def speak_to_agent(self, agent_id: str, player_text: str) -> DialogueOutcome:
        agent = self.host._find_agent(agent_id)
        distance = abs(agent.position.x - self.host.state.player.position.x) + abs(agent.position.y - self.host.state.player.position.y)
        if distance > 2:
            raise ValueError(f"{agent.name} 离你有点远，先靠近再聊天。")
        text = player_text.strip()
        if not text:
            raise ValueError("先输入一句你想说的话。")
        dialogue = build_dialogue_from_player(self.host.state, agent, text)
        return self.host._commit_dialogue(agent, dialogue, reason=f"玩家主动说了：{text}")

    def speak_to_agent_observer(self, agent_id: str, player_text: str) -> DialogueOutcome:
        agent = self.host._find_agent(agent_id)
        distance = abs(agent.position.x - self.host.state.player.position.x) + abs(agent.position.y - self.host.state.player.position.y)
        if distance > 2:
            raise ValueError(f"{agent.name} 离你有点远，先靠近再聊天。")
        text = player_text.strip()
        if not text:
            raise ValueError("先输入一句你想说的话。")
        dialogue = build_dialogue_from_player(self.host.state, agent, text)
        return self.host._commit_dialogue(agent, dialogue, reason=f"观察模式下你和 {agent.name} 随口聊了几句。", mode="observer")

    def commit_external_dialogue(self, agent_id: str, dialogue: DialogueOutcome, player_text: str) -> DialogueOutcome:
        agent = self.host._find_agent(agent_id)
        distance = abs(agent.position.x - self.host.state.player.position.x) + abs(agent.position.y - self.host.state.player.position.y)
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
        return self.host._commit_dialogue(agent, dialogue, reason=f"玩家主动说了：{text}")

    def commit_observer_dialogue(self, agent_id: str, dialogue: DialogueOutcome, player_text: str) -> DialogueOutcome:
        agent = self.host._find_agent(agent_id)
        distance = abs(agent.position.x - self.host.state.player.position.x) + abs(agent.position.y - self.host.state.player.position.y)
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
        return self.host._commit_dialogue(agent, dialogue, reason=f"观察模式下你和 {agent.name} 随口聊了几句。", mode="observer")

    def run_new_day_briefing(self, previous_day: int) -> WorldState:
        self.host._refresh_agents_for_new_day()
        self.host._generate_lab_daily(previous_day)
        return self.host.state
