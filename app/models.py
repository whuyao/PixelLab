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
    credit_score: int = 72
    reputation_score: int = 58
    risk_appetite: int = 52
    portfolio: dict[str, int] = Field(default_factory=dict)
    short_positions: dict[str, int] = Field(default_factory=dict)
    short_average_price: dict[str, float] = Field(default_factory=dict)
    last_trade_summary: str = ""
    injected_topics: list[str] = Field(default_factory=list)
    social_links: dict[str, int] = Field(default_factory=dict)
    relation_cooldowns: dict[str, int] = Field(default_factory=dict)
    daily_actions: list[str] = Field(default_factory=list)
    life_satisfaction: int = 56
    consumption_desire: int = 44
    housing_quality: int = 48
    materialism: int = 52
    comfort_preference: int = 58
    monthly_burden: int = 0
    owned_property_ids: list[str] = Field(default_factory=list)
    work_drive: int = 58
    daily_cost_baseline: int = 8
    employer_name: str = "青松数据服务"
    consumption_coupon_balance: int = 0
    deposit_balance: int = 0


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
    relation_cooldowns: dict[str, int] = Field(default_factory=dict)
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
    life_satisfaction: int = 56
    consumption_desire: int = 46
    housing_quality: int = 46
    materialism: int = 50
    comfort_preference: int = 50
    monthly_burden: int = 0
    owned_property_ids: list[str] = Field(default_factory=list)
    work_drive: int = 52
    daily_cost_baseline: int = 7
    employer_name: str = "青松数据服务"
    consumption_coupon_balance: int = 0
    deposit_balance: int = 0


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


class DialogueRecord(BaseModel):
    id: str
    kind: str
    day: int
    time_slot: TimeSlot
    participants: list[str] = Field(default_factory=list)
    participant_names: list[str] = Field(default_factory=list)
    topic: str = ""
    summary: str
    key_point: str = ""
    transcript: list[str] = Field(default_factory=list)
    desire_labels: dict[str, str] = Field(default_factory=dict)
    mood: str = ""
    financial_note: str = ""
    interest_rate: int | None = None
    gray_trade: bool = False
    gray_trade_type: str = ""
    gray_trade_severity: int = 0


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


class BankLoanRecord(BaseModel):
    id: str
    borrower_type: Literal["player", "agent"]
    borrower_id: str
    borrower_name: str
    principal: int
    daily_rate_pct: float
    total_rate_pct: float
    amount_due: int
    start_day: int
    due_day: int
    term_days: int = 1
    status: str = "active"
    reason: str = ""


class BankState(BaseModel):
    name: str = "青松合作银行"
    liquidity: int = 1800
    base_daily_rate_pct: float = 2.0
    base_deposit_daily_rate_pct: float = 0.32
    deposit_daily_rate_pct: float = 0.32
    risk_spread_pct: float = 0.0
    total_issued: int = 0
    total_repaid: int = 0
    total_deposits: int = 0
    total_interest_paid: int = 0
    defaults_count: int = 0


class CompanyState(BaseModel):
    name: str = "青松数据服务"
    location_label: str = "石径工坊"
    position: Point = Field(default_factory=lambda: Point(x=22, y=6))
    low_cash_threshold: int = 50
    base_pay_per_shift: int = 10
    pay_per_energy: int = 3
    pay_skill_multiplier: float = 0.08
    total_wages_paid: int = 0
    total_work_sessions: int = 0


class TouristAgent(BaseModel):
    id: str
    name: str
    archetype: str
    visitor_tier: Literal["regular", "repeat", "vip", "buyer"] = "regular"
    is_returning: bool = False
    property_interest: bool = False
    message_influence: int = 1
    favorite_topic: str = ""
    position: Point
    current_location: str
    cash: int = 40
    budget: int = 18
    mood: int = 58
    spending_desire: int = 56
    stay_until_day: int = 1
    current_activity: str = ""
    current_bubble: str = ""
    brief_note: str = ""
    target_position: Point | None = None
    target_location: str = ""
    linger_ticks: int = 0
    last_locations: list[str] = Field(default_factory=list)


class TourismState(BaseModel):
    inn_name: str = "湖畔旅馆"
    inn_position: Point = Field(default_factory=lambda: Point(x=36, y=22))
    inn_location: str = "lounge"
    market_name: str = "林间集市"
    market_position: Point = Field(default_factory=lambda: Point(x=6, y=14))
    market_location: str = "foyer"
    active_visitor_cap: int = 5
    season_mode: Literal["off", "normal", "peak", "festival"] = "normal"
    event_day_title: str = ""
    total_arrivals: int = 0
    total_departures: int = 0
    daily_arrivals: int = 0
    daily_departures: int = 0
    daily_revenue: int = 0
    total_revenue: int = 0
    repeat_customers_total: int = 0
    vip_customers_total: int = 0
    buyer_leads_total: int = 0
    daily_messages_count: int = 0
    latest_signal: str = ""
    last_note: str = "暂时还没有游客消息。"


class GovernmentState(BaseModel):
    name: str = "园区财政与监管局"
    wage_tax_rate_pct: float = 8.0
    securities_tax_rate_pct: float = 1.2
    property_transfer_tax_rate_pct: float = 4.0
    property_holding_tax_rate_pct: float = 6.0
    consumption_tax_rate_pct: float = 5.0
    luxury_tax_rate_pct: float = 8.0
    enforcement_level: int = 54
    welfare_low_cash_threshold: int = 24
    welfare_base_support: int = 10
    welfare_bankruptcy_support: int = 22
    fiscal_cycle_days: int = 15
    next_distribution_day: int = 15
    public_service_level: int = 36
    tourism_support_level: int = 30
    housing_support_level: int = 24
    government_asset_ids: list[str] = Field(default_factory=list)
    last_distribution_day: int = 0
    last_distribution_note: str = "财政周期还没有触发。"
    last_targeted_support: int = 0
    last_coupon_pool: int = 0
    last_public_service_spend: int = 0
    last_investment_spend: int = 0
    last_reserve_retained: int = 0
    last_cycle_tax_revenue: int = 0
    last_cycle_nonfine_consumption: int = 0
    total_revenue: int = 0
    reserve_balance: int = 260
    total_welfare_paid: int = 0
    total_coupons_issued: int = 0
    total_public_investment: int = 0
    last_audit_day: int = 0
    audit_cooldown_days: int = 4
    revenues: dict[str, int] = Field(
        default_factory=lambda: {
            "wage": 0,
            "market": 0,
            "property": 0,
            "consumption": 0,
            "fine": 0,
            "government_asset": 0,
        }
    )
    expenditures: dict[str, int] = Field(
        default_factory=lambda: {
            "welfare": 0,
            "coupon": 0,
            "public_service": 0,
            "investment": 0,
        }
    )
    last_policy_note: str = "维持默认税率。"


class ConsumableItem(BaseModel):
    id: str
    name: str
    category: Literal["food", "gift", "comfort", "tool"]
    price: int
    description: str = ""
    satisfaction_gain: int = 0
    mood_gain: int = 0
    energy_gain: int = 0
    relation_bonus: int = 0
    comfort_gain: int = 0
    debt_eligible: bool = False
    giftable: bool = False


class PropertyAsset(BaseModel):
    id: str
    owner_type: Literal["player", "agent", "market", "government"]
    owner_id: str
    property_type: Literal["home_upgrade", "farm_plot", "rental_house", "shop", "greenhouse"]
    name: str
    position: Point
    width: int = 2
    height: int = 2
    purchase_price: int
    estimated_value: int
    daily_income: int = 0
    daily_maintenance: int = 0
    comfort_bonus: int = 0
    social_bonus: int = 0
    debt_eligible: bool = True
    buildable: bool = False
    listed: bool = False
    built: bool = True
    status: str = "owned"
    description: str = ""


class FinanceRecord(BaseModel):
    id: str
    day: int
    time_slot: TimeSlot
    actor_id: str
    actor_name: str
    category: Literal["market", "consume", "property", "bank", "loan", "work", "gray", "tax", "welfare", "tourism", "government"]
    action: str
    summary: str
    amount: int = 0
    asset_name: str = ""
    counterparty: str = ""
    interest_rate: float | None = None
    financed: bool = False


class GrayCase(BaseModel):
    id: str
    case_type: str
    participants: list[str] = Field(default_factory=list)
    participant_names: list[str] = Field(default_factory=list)
    topic: str = ""
    summary: str = ""
    amount: int = 0
    severity: int = 1
    start_day: int = 1
    due_day: int | None = None
    exposure_risk: int = 20
    status: str = "active"


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
    base_price: float = 0.0
    fair_value: float = 0.0
    shares_outstanding: int = 0
    avg_volume: int = 0
    volume: int = 0
    turnover_pct: float = 0.0
    volatility_score: float = 0.9
    change_pct: float = 0.0
    day_change_pct: float = 0.0
    last_reason: str = ""


class MarketState(BaseModel):
    name: str = "Pixel Exchange"
    is_open: bool = True
    sentiment: int = 0
    tick: int = 0
    regime: str = "bull"
    regime_age: int = 1
    rotation_leader: str = "GEO"
    rotation_age: int = 1
    index_value: float = 100.0
    inflation_index: float = 100.0
    daily_inflation_pct: float = 0.0
    living_cost_pressure: int = 0
    turnover_total: float = 0.0
    turnover_ratio_pct: float = 0.0
    realized_volatility_pct: float = 0.8
    advancers: int = 0
    decliners: int = 0
    stocks: list[StockQuote] = Field(default_factory=list)
    index_history: list[IndexCandle] = Field(default_factory=list)
    daily_index_history: list[IndexCandle] = Field(default_factory=list)


class DailyBriefing(BaseModel):
    id: str
    day: int
    title: str
    lead: str = ""
    items: list[str] = Field(default_factory=list)
    entries: list["DailyBriefItem"] = Field(default_factory=list)


class DailyBriefItem(BaseModel):
    id: str
    text: str
    target_kind: str = ""
    target_id: str = ""
    target_filter: str = ""


class AnalysisPoint(BaseModel):
    day: int
    time_slot: TimeSlot
    team_cash: int = 0
    player_cash: int = 0
    reputation: int = 0
    market_index: float = 0.0
    inflation_index: float = 100.0
    avg_stress: float = 0.0
    avg_credit: float = 0.0
    active_events: int = 0
    active_gray_cases: int = 0


class WorldState(BaseModel):
    version: int = 36
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
    company: CompanyState = Field(default_factory=CompanyState)
    tourists: list[TouristAgent] = Field(default_factory=list)
    tourism: TourismState = Field(default_factory=TourismState)
    government: GovernmentState = Field(default_factory=GovernmentState)
    latest_dialogue: DialogueOutcome | None = None
    archived_tasks: list[Task] = Field(default_factory=list)
    ambient_dialogues: list[DialogueOutcome] = Field(default_factory=list)
    dialogue_history: list[DialogueRecord] = Field(default_factory=list)
    geoai_milestones: list[int] = Field(default_factory=list)
    daily_briefings: list[DailyBriefing] = Field(default_factory=list)
    social_threads: list[SocialThread] = Field(default_factory=list)
    story_beats: list[StoryBeat] = Field(default_factory=list)
    loans: list[LoanRecord] = Field(default_factory=list)
    bank: BankState = Field(default_factory=BankState)
    bank_loans: list[BankLoanRecord] = Field(default_factory=list)
    gray_cases: list[GrayCase] = Field(default_factory=list)
    lifestyle_catalog: list[ConsumableItem] = Field(default_factory=list)
    properties: list[PropertyAsset] = Field(default_factory=list)
    finance_history: list[FinanceRecord] = Field(default_factory=list)
    analysis_history: list[AnalysisPoint] = Field(default_factory=list)
    section_signatures: dict[str, str] = Field(default_factory=dict)


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


class BankBorrowRequest(BaseModel):
    amount: int
    term_days: Literal[1, 2, 3]


class BankRepayRequest(BaseModel):
    amount: int | None = None


class BankDepositRequest(BaseModel):
    amount: int


class BankWithdrawRequest(BaseModel):
    amount: int


class GrayCaseActionRequest(BaseModel):
    action: Literal["suppress", "report", "mediate", "short"]


class TaxPolicyRequest(BaseModel):
    wage_tax_rate_pct: float | None = None
    securities_tax_rate_pct: float | None = None
    property_transfer_tax_rate_pct: float | None = None
    property_holding_tax_rate_pct: float | None = None
    consumption_tax_rate_pct: float | None = None
    luxury_tax_rate_pct: float | None = None
    enforcement_level: int | None = None
    welfare_low_cash_threshold: int | None = None
    welfare_base_support: int | None = None
    welfare_bankruptcy_support: int | None = None
    note: str = ""


class StateDiffRequest(BaseModel):
    signatures: dict[str, str] = Field(default_factory=dict)


class StateDiffResponse(BaseModel):
    version: int
    signatures: dict[str, str] = Field(default_factory=dict)
    changed: list[str] = Field(default_factory=list)
    sections: dict[str, object] = Field(default_factory=dict)


class ConsumeRequest(BaseModel):
    item_id: str
    recipient_id: str = "player"
    financed: bool = False


class PropertyFinanceRequest(BaseModel):
    financed: bool = False
