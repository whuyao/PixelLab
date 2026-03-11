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
    cash: int = 100
    risk_appetite: int = 52
    portfolio: dict[str, int] = Field(default_factory=dict)
    last_trade_summary: str = ""
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
    cash: int = 100
    money_desire: int = 50
    generosity: int = 50
    money_urgency: int = 0
    credit_score: int = 72
    risk_appetite: int = 50
    portfolio: dict[str, int] = Field(default_factory=dict)
    last_trade_summary: str = ""
    home_position: Point | None = None
    home_label: str = ""
    is_resting: bool = False
    rest_until_day: int | None = None
    core_needs: list[str] = Field(default_factory=list)
    public_facts: list[str] = Field(default_factory=list)
    hidden_facts: list[str] = Field(default_factory=list)
    speech_habits: list[str] = Field(default_factory=list)
    immediate_intent: str = ""
    memory_stream: list[str] = Field(default_factory=list)


class Task(BaseModel):
    id: str
    title: str
    category: TaskCategory
    description: str
    progress: int = 0
    target: int = 100
    participants: list[str] = Field(default_factory=list)
    rewards: dict[str, int] = Field(default_factory=dict)
    completed_day: int | None = None
    archived_note: str = ""


class LabEvent(BaseModel):
    id: str
    category: EventCategory
    title: str
    summary: str
    source: str | None = None
    time_slot: TimeSlot
    impacts: dict[str, int] = Field(default_factory=dict)
    participants: list[str] = Field(default_factory=list)
    tone_hint: int = 0
    market_target: str = "broad"
    market_strength: int = 2


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


class LoanRecord(BaseModel):
    id: str
    lender_id: str
    borrower_id: str
    principal: int
    interest_rate: int
    amount_due: int
    start_day: int
    due_day: int
    status: str = "active"
    reason: str = ""


class IndexCandle(BaseModel):
    day: int
    open: float
    high: float
    low: float
    close: float
    limit_state: str = "normal"


class StockQuote(BaseModel):
    symbol: str
    name: str
    sector: str
    price: float
    open_price: float
    change_pct: float = 0.0
    day_change_pct: float = 0.0
    last_reason: str = ""


class MarketState(BaseModel):
    name: str = "Pixel Exchange"
    is_open: bool = True
    sentiment: int = 0
    tick: int = 0
    index_value: float = 100.0
    stocks: list[StockQuote] = Field(default_factory=list)
    index_history: list[IndexCandle] = Field(default_factory=list)
    daily_index_history: list[IndexCandle] = Field(default_factory=list)


class WorldState(BaseModel):
    version: int = 15
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
    market: MarketState
    latest_dialogue: DialogueOutcome | None = None
    archived_tasks: list[Task] = Field(default_factory=list)
    ambient_dialogues: list[DialogueOutcome] = Field(default_factory=list)
    social_threads: list[SocialThread] = Field(default_factory=list)
    story_beats: list[StoryBeat] = Field(default_factory=list)
    loans: list[LoanRecord] = Field(default_factory=list)


class MoveRequest(BaseModel):
    dx: int
    dy: int


class NewsRequest(BaseModel):
    topic: str
    category: EventCategory = "general"


class MacroNewsRequest(BaseModel):
    title: str
    summary: str = ""
    category: EventCategory = "market"
    tone: Literal["bullish", "bearish", "volatile"] = "bullish"
    strength: int = 3
    target: Literal["broad", "GEO", "AGR", "SIG"] = "broad"


class AdvanceRequest(BaseModel):
    reason: str = "reflect"


class SpeakRequest(BaseModel):
    text: str


class TradeRequest(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    shares: int = 1
