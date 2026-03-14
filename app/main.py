from __future__ import annotations

from contextlib import asynccontextmanager
import hashlib
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings, load_settings
from app.engine.game_engine import GameEngine
from app.models import AdvanceRequest, BankBorrowRequest, BankDepositRequest, BankRepayRequest, BankWithdrawRequest, ConsumeRequest, FeedPostRequest, FeedReactionRequest, GovernmentCapabilityRequest, GovernmentModeRequest, GrayCaseActionRequest, LLMProviderRequest, LabEvent, MacroNewsRequest, MoveRequest, NewsRequest, NewsTimelinePolicyRequest, NewsTimelineRequest, PropertyFinanceRequest, SpeakRequest, StateDiffRequest, StateDiffResponse, TaxPolicyRequest, TimeSlot, TradeRequest, WorldState
from app.services.activity_logger import ActivityLogger
from app.services.openai_dialogue_service import OpenAIDialogueError, OpenAIDialogueService
from app.services.brave_service import BraveSearchError, BraveService
from app.services.public_hotspot_service import PublicHotspotError, PublicHotspotService
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
        self.hotspots = PublicHotspotService()
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


def _upsert_secret_file(path: Path, updates: dict[str, str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    kept: list[str] = []
    seen: set[str] = set()
    for raw in lines:
        if "=" not in raw:
            kept.append(raw)
            continue
        key = raw.split("=", 1)[0].strip()
        if key in updates:
            if key not in seen:
                kept.append(f"{key}={updates[key]}")
                seen.add(key)
            continue
        kept.append(raw)
    for key, value in updates.items():
        if key not in seen:
            kept.append(f"{key}={value}")
    path.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8")


def _reload_dialogue_from_settings(settings_obj: Settings) -> None:
    context.settings = settings_obj
    context.dialogue = OpenAIDialogueService(
        settings_obj.llm_api_key,
        settings_obj.llm_model,
        settings_obj.llm_base_url,
        provider=settings_obj.llm_provider,
    )


def _dialogue_status() -> dict[str, object]:
    return {
        "provider": context.settings.llm_provider,
        "model": context.settings.llm_model,
        "base_url": context.settings.llm_base_url,
        "enabled": context.dialogue.enabled,
        "secret_file": str(context.settings.secret_file),
    }


def _feed_author_profile(post) -> str:
    world = context.engine.get_state()
    if post.author_type == "agent":
        agent = context.engine.get_agent(post.author_id)
        persona_map = {
            "lin": "林澈：说话冷静、爱追证据、讨厌口号先跑在事实前面。",
            "mika": "米遥：情绪灵、跳、敏感，容易被一句话刺到，也会突然被某个细节打动。",
            "jo": "周铖：直、硬、落地，先问谁掏钱、谁干活、谁背锅。",
            "rae": "芮宁：会接住人的情绪，关心谁会先被压垮，不爱空安慰。",
            "kai": "凯川：风向感强，爱盯信号、趋势和谁会被卷进去。",
        }
        return (
            persona_map.get(agent.id, f"{agent.name}：公开发言有自己的脾气。")
            + f" 角色：{agent.role}；专长：{agent.specialty}；当前地点：{agent.current_location}；当前计划：{agent.current_plan or '暂无'}。"
        )
    if post.author_type == "tourist":
        tourist = next((item for item in world.tourists if item.id == post.author_id), None)
        if tourist is None:
            return "游客：路过、体验、会把直观感受说出来。"
        tier_map = {
            "normal": "普通游客：更在意舒不舒服、值不值得留下。",
            "repeat": "回头客：会拿这次和上次比较，容易看出这里是不是只剩套路。",
            "vip": "高消费客户：花钱挑剔，讨厌被当提款机。",
            "buyer": "潜在购房者：对住房、租住和生活成本很敏感。",
        }
        return f"{tier_map.get(tourist.visitor_tier, '游客：说话直接。')} 当前地点：{tourist.current_location}；最近兴趣：{tourist.favorite_topic or '逛逛看'}。"
    if post.author_type == "government":
        gov = world.government
        return (
            "园区财政与监管局：公开表达偏短句公告风，但也会直接回应质疑。"
            f" 当前议程：{gov.current_agenda or '暂无'}；最近动作：{gov.last_agent_action or '暂无'}；监管强度：{gov.enforcement_level}。"
        )
    return "系统账号：负责播报和提醒。"


async def _refine_recent_feed_posts(limit: int = 4) -> None:
    if not context.dialogue.enabled:
        return
    world = context.engine.get_state()
    candidates = []
    for post in world.feed_timeline[:20]:
        if post.llm_refined:
            continue
        if post.author_type not in {"agent", "tourist", "government"}:
            continue
        if post.day < world.day - 1:
            continue
        candidates.append(post)
    for post in reversed(candidates[:limit]):
        target_post = None
        if post.reply_to_post_id:
            target_post = next((item for item in world.feed_timeline if item.id == post.reply_to_post_id), None)
        elif post.quote_post_id:
            target_post = next((item for item in world.feed_timeline if item.id == post.quote_post_id), None)
        try:
            rewritten = await context.dialogue.build_feed_post(
                world,
                author_name=post.author_name,
                author_profile=_feed_author_profile(post),
                category=post.category,
                draft_content=post.content,
                target_author=target_post.author_name if target_post else "",
                target_content=target_post.content if target_post else "",
                is_reply=bool(target_post),
            )
        except OpenAIDialogueError:
            post.llm_refined = True
            continue
        post.content = context.engine._clean_feed_text(rewritten["content"])
        post.summary = rewritten["summary"] or post.summary
        post.credibility = context.engine._feed_credibility_for_post(post)
        post.heat = context.engine._compute_feed_heat(post)
        post.llm_refined = True


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
        "社会热点": [
            ("社交平台热议年轻人消费降级", "互联网讨论把焦点拉回到生活成本、收入预期和日常消费取舍。", -1, "AGR", 3),
            ("一线城市周边短途疗愈游突然走红", "社交平台上的体验分享让文旅与短住市场被重新关注。", 1, "AGR", 3),
            ("平台热帖争论住房到底该先买还是先租", "围绕住房焦虑、现金流和长期生活感的讨论持续升温。", 0, "AGR", 3),
            ("社交平台疯传夜市会把本地生活彻底带贵", "传闻把夜市、房租、游客和生活成本绑在一起，引发一轮关于谁在承受代价的争论。", -1, "AGR", 4),
            ("有人热议这里会不会变成新的‘躺平避难地’", "围绕工作节奏、生活压力和消费选择的讨论突然升温，很多人开始重新评估什么才算舒服的生活。", 0, "broad", 3),
            ("短视频在传这里可能冒出下一波文旅黑马", "关于回头客、房价和游客消费的讨论迅速发酵，外部关注开始明显抬头。", 1, "AGR", 4),
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
        {"theme": "社会热点", "query": "China social media hot topics youth lifestyle housing consumption latest", "category": "general"},
    ]
    social_spec = next(spec for spec in specs if spec["theme"] == "社会热点")
    core_specs = [spec for spec in specs if spec["theme"] != "社会热点"]
    world = context.engine.get_state()
    context.engine.state.news_timeline = [item for item in context.engine.state.news_timeline if item.status != "scheduled"]
    created = 0
    window_days = max(3, min(14, int(getattr(context.engine.state, "news_window_days", 7) or 7)))
    sample_bounds = {
        3: (1, 2),
        7: (2, 4),
        14: (4, 6),
    }.get(window_days, (2, 4))
    min_items, max_items = sample_bounds
    sample_size = min(len(core_specs), context.engine.random.randint(min_items, max_items))
    chosen_specs = context.engine.random.sample(core_specs, sample_size)
    social_probability = {3: 0.35, 7: 1.0, 14: 1.0}.get(window_days, 1.0)
    if context.engine.random.random() < social_probability:
        chosen_specs.append(social_spec)
    horizon_slots = window_days * 5
    offsets = sorted(context.engine.random.sample(range(1, horizon_slots + 1), len(chosen_specs)))
    for offset, spec in zip(offsets, chosen_specs, strict=True):
        event = None
        if context.brave.api_key:
            try:
                results = await context.brave.search(spec["query"])
                if results:
                    event = map_search_result_to_event(_pick_preferred_brave_result(results), spec["query"], world.time_slot, spec["category"])
            except Exception:
                event = None
        if event is None:
            try:
                results = await context.hotspots.search(spec["query"], count=5)
                if results:
                    event = map_search_result_to_event(_pick_preferred_brave_result(results), spec["query"], world.time_slot, spec["category"])
            except (PublicHotspotError, Exception):
                event = None
        if event is None:
            event = _build_synthetic_timeline_event(spec, world.time_slot, world)
        event.market_strength = max(4, event.market_strength)
        if event.category == "market":
            event.market_strength = 5
        if event.tone_hint == 0:
            event.tone_hint = 1 if context.engine.random.random() < 0.5 else -1
        scheduled_day, scheduled_slot = context.engine.slot_after(offset)
        context.engine.schedule_news_timeline_item(event, spec["query"], spec["theme"], scheduled_day, scheduled_slot)
        created += 1
    has_social = any(
        item.status == "scheduled"
        and item.theme == "社会热点"
        and item.scheduled_day <= context.engine.state.day + window_days
        for item in context.engine.state.news_timeline
    )
    if not has_social and window_days >= 7:
        fallback_event = _build_synthetic_timeline_event(social_spec, world.time_slot, world)
        fallback_event.market_strength = max(4, fallback_event.market_strength)
        fallback_offset = max(1, min(horizon_slots, context.engine.random.randint(2, max(2, horizon_slots // 2))))
        scheduled_day, scheduled_slot = context.engine.slot_after(fallback_offset)
        context.engine.schedule_news_timeline_item(
            fallback_event,
            social_spec["query"],
            social_spec["theme"],
            scheduled_day,
            scheduled_slot,
        )
        created += 1
    context.engine.state.tourism.last_note = f"系统刚自动排好了未来 {window_days} 天内的 {created} 条主线新闻。"


async def _maybe_refresh_news_timeline() -> None:
    window_days = max(3, min(14, int(getattr(context.engine.state, "news_window_days", 7) or 7)))
    min_items, max_items = {
        3: (1, 2),
        7: (2, 4),
        14: (4, 6),
    }.get(window_days, (2, 4))
    scheduled = [
        item
        for item in context.engine.state.news_timeline
        if item.status == "scheduled" and item.scheduled_day <= context.engine.state.day + window_days
    ]
    needs_rebuild = any((item.market_strength or 0) < 4 for item in scheduled)
    if min_items <= len(scheduled) <= max_items and not needs_rebuild:
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


@app.get("/api/llm/status")
async def llm_status() -> dict[str, object]:
    return _dialogue_status()


@app.post("/api/llm/provider")
async def switch_llm_provider(payload: LLMProviderRequest) -> dict[str, object]:
    updates = {"LLM_PROVIDER": payload.provider}
    if payload.provider == "qwen":
        if payload.model:
            updates["QWEN_MODEL"] = payload.model
        if payload.base_url:
            updates["QWEN_BASE_URL"] = payload.base_url
    else:
        if payload.model:
            updates["OPENAI_MODEL"] = payload.model
        if payload.base_url:
            updates["OPENAI_BASE_URL"] = payload.base_url
    _upsert_secret_file(context.settings.secret_file, updates)
    for key, value in updates.items():
        os.environ[key] = value
    new_settings = load_settings()
    _reload_dialogue_from_settings(new_settings)
    return _dialogue_status()


@app.post("/api/feed/post", response_model=WorldState)
async def create_feed_post(payload: FeedPostRequest) -> WorldState:
    try:
        context.engine.create_player_feed_post(payload.content, payload.category, payload.reply_to_post_id, payload.quote_post_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await _refine_recent_feed_posts(limit=2)
    return _persist_and_return_state()


@app.post("/api/feed/react", response_model=WorldState)
async def react_feed_post(payload: FeedReactionRequest) -> WorldState:
    try:
        context.engine.react_to_feed_post(payload.post_id, payload.action)
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
    await _refine_recent_feed_posts(limit=4)
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


@app.post("/api/news/policy", response_model=WorldState)
async def update_news_timeline_policy(payload: NewsTimelinePolicyRequest) -> WorldState:
    context.engine.state.news_window_days = int(payload.window_days)
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


@app.post("/api/government/mode", response_model=WorldState)
async def update_government_mode(payload: GovernmentModeRequest) -> WorldState:
    context.engine.set_big_government_mode(payload.enabled)
    return _persist_and_return_state()


@app.post("/api/government/capabilities", response_model=WorldState)
async def update_government_capabilities(payload: GovernmentCapabilityRequest) -> WorldState:
    context.engine.update_government_capabilities(payload.model_dump(exclude_none=True))
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
