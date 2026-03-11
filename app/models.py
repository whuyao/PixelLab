from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


TimeSlot = Literal["morning", "noon", "afternoon", "evening", "night"]
TaskCategory = Literal["main", "daily", "social", "external"]
EventCategory = Literal["geoai", "tech", "market", "gaming", "general"]
WeatherKind = Literal["sunny", "breezy", "cloudy", "drizzle"]


class Point(BaseModel):
    x: int
    y: int


class Player(BaseModel):
    id: str
    name: str
    position: Point
    injected_topics: list[str] = Field(default_factory=list)
    social_links: dict[str, int] = Field(default_factory=dict)
    daily_actions: list[str] = Field(default_factory=list)


class AgentState(BaseModel):
    mood: int
    stress: int
    focus: int
    energy: int
    curiosity: int
    research_skill: int
    geo_reasoning_skill: int


class MemoryEntry(BaseModel):
    text: str
    day: int
    time_slot: TimeSlot
    importance: int = 1


class Agent(BaseModel):
    id: str
    name: str
    role: str
    persona: str
    specialty: str
    current_task: str | None = None
    current_location: str
    position: Point
    state: AgentState
    relations: dict[str, int] = Field(default_factory=dict)
    short_term_memory: list[MemoryEntry] = Field(default_factory=list)
    long_term_memory: list[MemoryEntry] = Field(default_factory=list)
    current_activity: str = ""
    current_bubble: str = ""
    status_summary: str = ""
    last_interaction: str = ""
    goals: list[str] = Field(default_factory=list)
    taboos: list[str] = Field(default_factory=list)
    allies: list[str] = Field(default_factory=list)
    rivals: list[str] = Field(default_factory=list)
    desired_resource: str = ""
    current_plan: str = ""
    social_stance: str = "observe"
    sprite_style: str = "scientist_a"
    home_position: Point | None = None
    home_label: str = ""
    is_resting: bool = False
    rest_until_day: int | None = None


class Task(BaseModel):
    id: str
    title: str
    category: TaskCategory
    description: str
    progress: int = 0
    target: int = 100
    participants: list[str] = Field(default_factory=list)
    rewards: dict[str, int] = Field(default_factory=dict)


class LabEvent(BaseModel):
    id: str
    category: EventCategory
    title: str
    summary: str
    source: str | None = None
    time_slot: TimeSlot
    impacts: dict[str, int] = Field(default_factory=dict)
    participants: list[str] = Field(default_factory=list)


class LabMetrics(BaseModel):
    reputation: int
    knowledge_base: int
    team_atmosphere: int
    collective_reasoning: int
    research_progress: int
    external_sensitivity: int
    geoai_progress: int


class DialogueOutcome(BaseModel):
    agent_id: str
    agent_name: str
    player_text: str = ""
    line: str
    topic: str
    bubble_text: str = ""
    effects: list[str] = Field(default_factory=list)


class SocialThread(BaseModel):
    id: str
    participants: list[str] = Field(default_factory=list)
    topic: str
    stage: int = 1
    momentum: int = 1
    mood: str = "neutral"
    latest_summary: str = ""
    location: str = ""


class StoryBeat(BaseModel):
    id: str
    title: str
    summary: str
    kind: str
    participants: list[str] = Field(default_factory=list)
    stage: int = 1
    momentum: int = 1
    location: str = ""


class WorldState(BaseModel):
    version: int = 8
    world_width: int = 44
    world_height: int = 26
    day: int
    time_slot: TimeSlot
    weather: WeatherKind = "sunny"
    player: Player
    agents: list[Agent]
    tasks: list[Task]
    events: list[LabEvent]
    lab: LabMetrics
    latest_dialogue: DialogueOutcome | None = None
    ambient_dialogues: list[DialogueOutcome] = Field(default_factory=list)
    social_threads: list[SocialThread] = Field(default_factory=list)
    story_beats: list[StoryBeat] = Field(default_factory=list)


class MoveRequest(BaseModel):
    dx: int
    dy: int


class NewsRequest(BaseModel):
    topic: str
    category: EventCategory = "general"


class AdvanceRequest(BaseModel):
    reason: str = "reflect"


class SpeakRequest(BaseModel):
    text: str
