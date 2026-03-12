from __future__ import annotations

from contextlib import asynccontextmanager
import hashlib
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings, load_settings
from app.engine.game_engine import GameEngine
from app.models import AdvanceRequest, BankBorrowRequest, BankDepositRequest, BankRepayRequest, BankWithdrawRequest, ConsumeRequest, GrayCaseActionRequest, LabEvent, MacroNewsRequest, MoveRequest, NewsRequest, NewsTimelineRequest, PropertyFinanceRequest, SpeakRequest, StateDiffRequest, StateDiffResponse, TaxPolicyRequest, TimeSlot, TradeRequest, WorldState
from app.services.activity_logger import ActivityLogger
from app.services.openai_dialogue_service import OpenAIDialogueError, OpenAIDialogueService
from app.services.brave_service import BraveSearchError, BraveService
from app.services.event_mapper import map_macro_news_to_event, map_search_result_to_event
from app.storage.repository import SnapshotRepository


class AppContext:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.activity_logger = ActivityLogger(settings.log_path)
        self.repository = SnapshotRepository(settings.save_path)
        saved_state = self.repository.load()
        self.engine = GameEngine(state=saved_state, activity_logger=self.activity_logger)
        if saved_state:
            self.engine.log_world_snapshot("snapshot_loaded", details={"source": str(settings.save_path)})
        self.brave = BraveService(settings.brave_api_key)
        self.dialogue = OpenAIDialogueService(
            settings.llm_api_key,
            settings.llm_model,
            settings.llm_base_url,
            provider=settings.llm_provider,
        )
        self.engine.log_world_snapshot("app_boot", details={"log_path": str(settings.log_path)})


settings = load_settings()
context = AppContext(settings)


@asynccontextmanager
async def lifespan(_: FastAPI):
    context.repository.save(context.engine.get_state())
    yield
    context.repository.save(context.engine.get_state())


app = FastAPI(title="LocalFarmer", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "static"), name="static")


def _persist_and_return_state() -> WorldState:
    state = context.engine.get_state()
    context.repository.save(state)
    return state


def _pick_preferred_brave_result(results: list[dict[str, str]]) -> dict[str, str]:
    if not results:
        return {}
    def score(item: dict[str, str]) -> tuple[int, int]:
        source = f"{item.get('profile_name', '')} {item.get('url', '')}".lower()
        penalty = 0
        if "wikipedia.org" in source:
            penalty += 3
        if "travelandtourworld" in source:
            penalty += 2
        if "tradingeconomics" in source:
            penalty += 1
        freshness = 0 if item.get("age") else 1
        return penalty, freshness
    return sorted(results, key=score)[0]


def _build_synthetic_timeline_event(spec: dict[str, str], slot: TimeSlot, world: WorldState) -> LabEvent:
    banks = {
        "宏观消费": [
            ("消费券刺激带动本地零售回暖", "周边片区的餐饮和轻消费出现回暖迹象，市场预期居民支出意愿短期修复。", 1, "AGR", 3),
            ("居民储蓄倾向抬头压制即期消费", "更多家庭把新增收入留在存款里，消费恢复节奏比预期更慢。", -1, "AGR", 2),
        ],
        "监管与税务": [
            ("地方监管释放温和规范信号", "市场判断短期不会出现更猛烈的收紧，合规成本仍在但可预期。", 1, "broad", 2),
            ("税务核查风声让交易情绪转谨慎", "部分经营者开始担心抽查频率和报表压力，盘面风险偏好略降。", -1, "SIG", 3),
        ],
        "地产与住房": [
            ("租住需求回升支撑园区地产预期", "短住与租住需求抬升，让地产相关收入和估值预期略有改善。", 1, "AGR", 2),
            ("住房观望情绪拖慢成交节奏", "潜在购房者继续观望，挂牌资产的消化速度有所放缓。", -1, "AGR", 2),
        ],
        "游客与文旅": [
            ("节庆客流预期抬升本地文旅信心", "活动日带动的游客预期升温，旅馆和集市可能迎来一轮额外消费。", 1, "AGR", 3),
            ("游客预算偏谨慎压低夜间消费", "虽然到访人数稳定，但游客单次消费额有收缩迹象。", -1, "AGR", 2),
        ],
        "GeoAI 与空间智能": [
            ("空间智能合作订单传闻升温", "外部客户开始试探 GeoAI 能力采购，市场把相关能力视为增长线索。", 1, "GEO", 4),
            ("GeoAI 项目审批节奏放慢", "几笔潜在合作需要更久评估，短期推进感减弱。", -1, "GEO", 3),
        ],
        "就业与劳动": [
            ("服务业用工需求回升", "短期劳动需求增加，让本地打工收入和现金流预期略有改善。", 1, "broad", 2),
            ("工资兑现周期拉长", "部分服务业订单回款慢，市场开始担心劳动收入兑现延后。", -1, "SIG", 2),
        ],
    }
    choices = banks.get(spec["theme"], [("系统新闻台发来一条市场消息", "这条消息会让系统短期重新评估风险偏好。", 0, "broad", 2)])
    digest = hashlib.sha1(f"{spec['theme']}-{world.day}-{world.time_slot}".encode("utf-8")).hexdigest()
    idx = int(digest[:2], 16) % len(choices)
    title, summary, tone, target, strength = choices[idx]
    impacts = {
        "geoai_progress": 5 if spec["category"] == "geoai" and tone >= 0 else 2,
        "collective_reasoning": 4 if spec["category"] in {"geoai", "tech"} else 2,
        "research_progress": 4 if spec["category"] != "gaming" else 1,
    }
    return LabEvent(
        id=f"event-synth-{digest[:8]}",
        category=spec["category"],
        title=title,
        summary=summary,
        source="系统新闻台",
        time_slot=slot,
        impacts=impacts,
        participants=[],
        tone_hint=tone,
        market_target=target,
        market_strength=strength,
    )


async def _rebuild_news_timeline() -> None:
    specs = [
        {"theme": "宏观消费", "query": "China consumption stimulus retail sales policy market latest", "category": "market"},
        {"theme": "监管与税务", "query": "China regulation tax oversight market real estate latest", "category": "market"},
        {"theme": "地产与住房", "query": "China housing property market tourism rentals latest", "category": "market"},
        {"theme": "游客与文旅", "query": "China tourism domestic travel spending cultural market latest", "category": "general"},
        {"theme": "GeoAI 与空间智能", "query": "geospatial AI GeoAI spatial intelligence mapping funding latest", "category": "geoai"},
        {"theme": "就业与劳动", "query": "China employment wages labor services income latest", "category": "general"},
    ]
    world = context.engine.get_state()
    context.engine.state.news_timeline = [item for item in context.engine.state.news_timeline if item.status != "scheduled"]
    created = 0
    for offset, spec in enumerate(specs, start=1):
        event = None
        if context.brave.api_key:
            try:
                results = await context.brave.search(spec["query"])
                if results:
                    event = map_search_result_to_event(_pick_preferred_brave_result(results), spec["query"], world.time_slot, spec["category"])
            except Exception:
                event = None
        if event is None:
            event = _build_synthetic_timeline_event(spec, world.time_slot, world)
        scheduled_day, scheduled_slot = context.engine.slot_after(offset)
        context.engine.schedule_news_timeline_item(event, spec["query"], spec["theme"], scheduled_day, scheduled_slot)
        created += 1
    context.engine.state.tourism.last_note = f"系统刚自动排好了 {created} 条主线新闻时间线。"


async def _maybe_refresh_news_timeline() -> None:
    scheduled = [item for item in context.engine.state.news_timeline if item.status == "scheduled"]
    if len(scheduled) >= 3:
        return
    await _rebuild_news_timeline()


async def _apply_ai_player_dialogue(agent_id: str, text: str, observer_mode: bool = False) -> None:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("先输入一句你想说的话。")
    if context.engine.has_tourist(agent_id):
        context.engine.speak_to_tourist(agent_id, cleaned, observer=observer_mode)
        return
    dialogue = None
    if context.dialogue.enabled:
        agent = context.engine.get_agent(agent_id)
        try:
            dialogue = await context.dialogue.build_player_dialogue(context.engine.get_state(), agent, cleaned)
        except OpenAIDialogueError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    if dialogue is not None:
        if observer_mode:
            context.engine.social_engine.commit_observer_dialogue(agent_id, dialogue, cleaned)
        else:
            context.engine.commit_external_dialogue(agent_id, dialogue, cleaned)
    else:
        if observer_mode:
            context.engine.social_engine.speak_to_agent_observer(agent_id, cleaned)
        else:
            context.engine.speak_to_agent(agent_id, cleaned)


@app.get("/")
async def root() -> FileResponse:
    return FileResponse(Path(__file__).parent.parent / "static/index.html")


@app.get("/api/state", response_model=WorldState)
async def get_state() -> WorldState:
    await _maybe_refresh_news_timeline()
    return _persist_and_return_state()


@app.post("/api/state/diff", response_model=StateDiffResponse)
async def get_state_diff(payload: StateDiffRequest) -> StateDiffResponse:
    await _maybe_refresh_news_timeline()
    return context.engine.get_state_diff(payload.signatures)


@app.post("/api/move", response_model=WorldState)
async def move_player(payload: MoveRequest) -> WorldState:
    try:
        state = context.engine.move_player(payload.dx, payload.dy)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/interact/{agent_id}", response_model=WorldState)
async def interact(agent_id: str) -> WorldState:
    try:
        context.engine.interact_with_agent(agent_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/speak/{agent_id}", response_model=WorldState)
async def speak(agent_id: str, payload: SpeakRequest) -> WorldState:
    try:
        await _apply_ai_player_dialogue(agent_id, payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/auto-speak/{agent_id}", response_model=WorldState)
async def auto_speak(agent_id: str, payload: SpeakRequest) -> WorldState:
    try:
        await _apply_ai_player_dialogue(agent_id, payload.text, observer_mode=True)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/advance", response_model=WorldState)
async def advance(payload: AdvanceRequest) -> WorldState:
    context.engine.advance_for_reflection(payload.reason)
    return _persist_and_return_state()


@app.post("/api/simulate", response_model=WorldState)
async def simulate() -> WorldState:
    context.engine.simulate_world()
    return _persist_and_return_state()


@app.post("/api/news", response_model=WorldState)
async def inject_news(payload: NewsRequest) -> WorldState:
    query = payload.topic.strip()
    if payload.category in {"market", "general"}:
        query = f"{query} economy markets macro policy stocks latest"
    elif payload.category == "tech":
        query = f"{query} technology chip cloud ai market latest"
    elif payload.category == "geoai":
        query = f"{query} geospatial mapping spatial ai latest"
    try:
        results = await context.brave.search(query)
    except BraveSearchError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - network failure path
        raise HTTPException(status_code=502, detail=f"Brave search failed: {exc}") from exc
    if not results:
        raise HTTPException(status_code=404, detail="No Brave results found for this topic.")
    event = map_search_result_to_event(_pick_preferred_brave_result(results), payload.topic, context.engine.get_state().time_slot, payload.category)
    context.engine.inject_event(event)
    return _persist_and_return_state()


@app.post("/api/news/timeline", response_model=WorldState)
async def refresh_news_timeline(payload: NewsTimelineRequest) -> WorldState:
    await _rebuild_news_timeline()
    return _persist_and_return_state()


@app.post("/api/macro-news", response_model=WorldState)
async def inject_macro_news(payload: MacroNewsRequest) -> WorldState:
    try:
        event = map_macro_news_to_event(payload, context.engine.get_state().time_slot)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    context.engine.inject_event(event)
    return _persist_and_return_state()


@app.post("/api/government/policy", response_model=WorldState)
async def update_tax_policy(payload: TaxPolicyRequest) -> WorldState:
    context.engine.update_tax_policy(payload.model_dump())
    return _persist_and_return_state()


@app.post("/api/player/trade", response_model=WorldState)
async def player_trade(payload: TradeRequest) -> WorldState:
    try:
        state = context.engine.player_trade(payload.symbol, payload.side, payload.shares)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/player/auto-trade", response_model=WorldState)
async def player_auto_trade() -> WorldState:
    context.engine.auto_trade_player()
    return _persist_and_return_state()


@app.post("/api/lifestyle/consume", response_model=WorldState)
async def player_consume(payload: ConsumeRequest) -> WorldState:
    try:
        state = context.engine.player_consume_item(payload.item_id, payload.recipient_id, financed=payload.financed)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/properties/{property_id}/buy", response_model=WorldState)
async def player_buy_property(property_id: str, payload: PropertyFinanceRequest) -> WorldState:
    try:
        state = context.engine.player_buy_property(property_id, financed=payload.financed)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/properties/{property_id}/sell", response_model=WorldState)
async def player_sell_property(property_id: str) -> WorldState:
    try:
        state = context.engine.player_sell_property(property_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/bank/borrow", response_model=WorldState)
async def bank_borrow(payload: BankBorrowRequest) -> WorldState:
    try:
        state = context.engine.player_bank_borrow(payload.amount, payload.term_days)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/bank/repay/{loan_id}", response_model=WorldState)
async def bank_repay(loan_id: str, payload: BankRepayRequest) -> WorldState:
    try:
        state = context.engine.player_bank_repay(loan_id, payload.amount)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/bank/deposit", response_model=WorldState)
async def bank_deposit(payload: BankDepositRequest) -> WorldState:
    try:
        state = context.engine.player_bank_deposit(payload.amount)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/bank/withdraw", response_model=WorldState)
async def bank_withdraw(payload: BankWithdrawRequest) -> WorldState:
    try:
        state = context.engine.player_bank_withdraw(payload.amount)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _persist_and_return_state()


@app.post("/api/gray-cases/{case_id}/action", response_model=WorldState)
async def gray_case_action(case_id: str, payload: GrayCaseActionRequest) -> WorldState:
    try:
        state = context.engine.resolve_gray_case_action(case_id, payload.action)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _persist_and_return_state()
