from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


TimeSlot = Literal["morning", "noon", "afternoon", "evening", "night"]
TaskCategory = Literal["main", "daily", "social", "external"]
EventCategory = Literal["geoai", "tech", "market", "gaming", "general", "policy"]
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
    metric_key: str = ""
    start_value: int = 0
    goal_value: int = 0
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


class FeedPost(BaseModel):
    id: str
    author_type: Literal["player", "agent", "tourist", "government", "system"]
    author_id: str
    author_name: str
    day: int
    time_slot: TimeSlot
    category: Literal["daily", "mood", "research", "market", "property", "tourism", "policy", "gossip"] = "daily"
    mood: Literal["neutral", "warm", "spark", "tense", "cool"] = "neutral"
    content: str
    topic_tags: list[str] = Field(default_factory=list)
    desire_tags: list[str] = Field(default_factory=list)
    reply_to_post_id: str | None = None
    quote_post_id: str | None = None
    likes: int = 0
    reposts: int = 0
    views: int = 0
    heat: int = 0
    credibility: int = 50
    summary: str = ""
    impacts: list[str] = Field(default_factory=list)
    llm_refined: bool = False


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
    short_term_memory: list[MemoryEntry] = Field(default_factory=list)
    market_portfolio: dict[str, int] = Field(default_factory=dict)
    market_invested_total: int = 0
    market_last_action: str = ""
    target_position: Point | None = None
    target_location: str = ""
    linger_ticks: int = 0
    last_locations: list[str] = Field(default_factory=list)


class TourismState(BaseModel):
    inn_name: str = "湖畔旅馆"
    inn_position: Point = Field(default_factory=lambda: Point(x=35, y=14))
    inn_location: str = "lounge"
    market_name: str = "林间集市"
    market_position: Point = Field(default_factory=lambda: Point(x=7, y=16))
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
    daily_private_income: int = 0
    total_private_income: int = 0
    daily_government_income: int = 0
    total_government_income: int = 0
    daily_public_operator_income: int = 0
    total_public_operator_income: int = 0
    repeat_customers_total: int = 0
    vip_customers_total: int = 0
    buyer_leads_total: int = 0
    daily_messages_count: int = 0
    latest_signal: str = ""
    last_note: str = "暂时还没有游客消息。"


class GovernmentState(BaseModel):
    name: str = "园区财政与监管局"
    approval_score: int = 56
    approval_note: str = "公众目前对政府维持温和支持。"
    big_mode_enabled: bool = False
    can_tune_taxes: bool = True
    can_tune_rates: bool = True
    can_manage_construction: bool = True
    can_trade_assets: bool = True
    can_intervene_prices: bool = True
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
    current_agenda: str = "观察税收、游客和住房压力。"
    last_agent_action: str = "财政周期还没有触发新的建设动作。"
    last_agent_reason: str = "系统会根据游客、住房、储备和资产收益决定下一步。"
    last_macro_action: str = "当前仍采用常规政府模式。"
    known_signals: list[str] = Field(default_factory=list)
    last_agent_action_day: int = 0
    daily_asset_revenue: int = 0
    daily_asset_maintenance: int = 0
    daily_asset_net: int = 0
    revenues: dict[str, int] = Field(
        default_factory=lambda: {
            "wage": 0,
            "market": 0,
            "property": 0,
            "consumption": 0,
            "fine": 0,
            "government_asset": 0,
            "tourism_public": 0,
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
    property_type: Literal["home_upgrade", "farm_plot", "rental_house", "shop", "greenhouse", "casino"]
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
    facility_kind: str = ""
    anchor_slot: str = ""
    project_stage: str = ""
    project_due_day: int = 0
    description: str = ""


class FinanceRecord(BaseModel):
    id: str
    day: int
    time_slot: TimeSlot
    actor_id: str
    actor_name: str
    category: Literal["market", "consume", "property", "bank", "loan", "work", "gray", "tax", "welfare", "tourism", "government", "casino"]
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
    resolution_action: str = ""
    resolution_label: str = ""
    resolution_exposed: bool = False
    resolution_note: str = ""


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


class NewsTimelineItem(BaseModel):
    id: str
    title: str
    summary: str
    source: str = ""
    query: str = ""
    theme: str = ""
    category: EventCategory = "general"
    scheduled_day: int
    scheduled_time_slot: TimeSlot
    mood: Literal["neutral", "warm", "spark", "tense", "cool"] = "neutral"
    tone_hint: int = 0
    market_target: str = "broad"
    market_strength: int = 2
    impacts: dict[str, int] = Field(default_factory=dict)
    status: Literal["scheduled", "triggered", "expired"] = "scheduled"
    triggered_day: int | None = None
    triggered_time_slot: TimeSlot | None = None


class AnalysisPoint(BaseModel):
    day: int
    time_slot: TimeSlot
    team_cash: int = 0
    team_assets: int = 0
    team_deposits: int = 0
    player_cash: int = 0
    player_assets: int = 0
    reputation: int = 0
    market_index: float = 0.0
    inflation_index: float = 100.0
    avg_stress: float = 0.0
    avg_satisfaction: float = 0.0
    avg_credit: float = 0.0
    active_events: int = 0
    active_gray_cases: int = 0
    tourists_active: int = 0
    tourist_revenue_daily: int = 0
    government_reserve: int = 0
    casino_heat: int = 0
    casino_daily_visits: int = 0
    casino_daily_wagers: int = 0
    casino_daily_tax: int = 0


class DailyEconomyPoint(BaseModel):
    day: int
    resident_consumption: int = 0
    tourist_consumption: int = 0
    tourism_private_income: int = 0
    tourism_government_income: int = 0
    tourism_public_income: int = 0
    government_asset_income: int = 0


class DailyBankPoint(BaseModel):
    day: int
    loans_issued: int = 0
    loans_repaid: int = 0
    deposits_in: int = 0
    deposits_out: int = 0
    outstanding_balance: int = 0
    total_deposits: int = 0


class DailyCasinoPoint(BaseModel):
    day: int
    visits: int = 0
    wagers: int = 0
    payouts: int = 0
    tax: int = 0
    big_wins: int = 0
    heat: int = 0


class CasinoState(BaseModel):
    name: str = "后巷地下赌场"
    daily_visits: int = 0
    total_visits: int = 0
    daily_wagers: int = 0
    total_wagers: int = 0
    daily_payouts: int = 0
    total_payouts: int = 0
    daily_tax: int = 0
    total_tax: int = 0
    daily_big_wins: int = 0
    total_big_wins: int = 0
    house_bankroll: int = 6000
    current_heat: int = 18
    last_note: str = "后巷牌桌今晚还没真正热起来。"


class WorldState(BaseModel):
    version: int = 59
    world_width: int = 44
    world_height: int = 26
    day: int
    time_slot: TimeSlot
    weather: WeatherKind = "sunny"
    player: Player
    agents: list[Agent]
    tasks: list[Task]
    events: list[LabEvent]
    event_history: list[LabEvent] = Field(default_factory=list)
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
    feed_timeline: list[FeedPost] = Field(default_factory=list)
    geoai_milestones: list[int] = Field(default_factory=list)
    daily_briefings: list[DailyBriefing] = Field(default_factory=list)
    news_timeline: list[NewsTimelineItem] = Field(default_factory=list)
    news_window_days: int = 7
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
    daily_economy_history: list[DailyEconomyPoint] = Field(default_factory=list)
    daily_bank_history: list[DailyBankPoint] = Field(default_factory=list)
    daily_casino_history: list[DailyCasinoPoint] = Field(default_factory=list)
    casino: CasinoState = Field(default_factory=CasinoState)
    section_signatures: dict[str, str] = Field(default_factory=dict)


class MoveRequest(BaseModel):
    dx: int
    dy: int


class NewsRequest(BaseModel):
    topic: str
    category: EventCategory = "general"


class NewsTimelineRequest(BaseModel):
    horizon_slots: int = 6


class NewsTimelinePolicyRequest(BaseModel):
    window_days: Literal[3, 7, 14]


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


class LLMProviderRequest(BaseModel):
    provider: Literal["openai", "qwen"]
    model: str | None = None
    base_url: str | None = None


class FeedPostRequest(BaseModel):
    content: str
    category: Literal["daily", "mood", "research", "market", "property", "tourism", "policy", "gossip"] = "daily"
    mood: Literal["neutral", "warm", "spark", "tense", "cool"] = "neutral"
    reply_to_post_id: str | None = None
    quote_post_id: str | None = None


class FeedReactionRequest(BaseModel):
    post_id: str
    action: Literal["like", "repost", "watch"]


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


class GambleRequest(BaseModel):
    amount: int = 20


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


class GovernmentModeRequest(BaseModel):
    enabled: bool


class GovernmentCapabilityRequest(BaseModel):
    can_tune_taxes: bool | None = None
    can_tune_rates: bool | None = None
    can_manage_construction: bool | None = None
    can_trade_assets: bool | None = None
    can_intervene_prices: bool | None = None


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
