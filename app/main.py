from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings, load_settings
from app.engine.game_engine import GameEngine
from app.models import AdvanceRequest, MacroNewsRequest, MoveRequest, NewsRequest, SpeakRequest, TradeRequest, WorldState
from app.services.activity_logger import ActivityLogger
from app.services.openai_dialogue_service import OpenAIDialogueError, OpenAIDialogueService
from app.services.brave_service import BraveSearchError, BraveService
from app.services.event_mapper import map_macro_news_to_event, map_search_result_to_event
from app.storage.repository import SnapshotRepository


class AppContext:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.activity_logger = ActivityLogger(settings.log_path)
        self.engine = GameEngine(activity_logger=self.activity_logger)
        self.repository = SnapshotRepository(settings.save_path)
        saved_state = self.repository.load()
        if saved_state:
            self.engine.state = saved_state
            self.engine.log_world_snapshot("snapshot_loaded", details={"source": str(settings.save_path)})
        self.brave = BraveService(settings.brave_api_key)
        self.dialogue = OpenAIDialogueService(settings.openai_api_key, settings.openai_model)
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


async def _apply_ai_player_dialogue(agent_id: str, text: str) -> None:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("先输入一句你想说的话。")
    dialogue = None
    if context.dialogue.enabled:
        agent = context.engine.get_agent(agent_id)
        try:
            dialogue = await context.dialogue.build_player_dialogue(context.engine.get_state(), agent, cleaned)
        except OpenAIDialogueError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    if dialogue is not None:
        context.engine.commit_external_dialogue(agent_id, dialogue, cleaned)
    else:
        context.engine.speak_to_agent(agent_id, cleaned)


@app.get("/")
async def root() -> FileResponse:
    return FileResponse(Path(__file__).parent.parent / "static/index.html")


@app.get("/api/state", response_model=WorldState)
async def get_state() -> WorldState:
    return context.engine.get_state()


@app.post("/api/move", response_model=WorldState)
async def move_player(payload: MoveRequest) -> WorldState:
    try:
        state = context.engine.move_player(payload.dx, payload.dy)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    context.repository.save(state)
    return state


@app.post("/api/interact/{agent_id}", response_model=WorldState)
async def interact(agent_id: str) -> WorldState:
    try:
        context.engine.interact_with_agent(agent_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    state = context.engine.get_state()
    context.repository.save(state)
    return state


@app.post("/api/speak/{agent_id}", response_model=WorldState)
async def speak(agent_id: str, payload: SpeakRequest) -> WorldState:
    try:
        await _apply_ai_player_dialogue(agent_id, payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    state = context.engine.get_state()
    context.repository.save(state)
    return state


@app.post("/api/auto-speak/{agent_id}", response_model=WorldState)
async def auto_speak(agent_id: str, payload: SpeakRequest) -> WorldState:
    try:
        await _apply_ai_player_dialogue(agent_id, payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    state = context.engine.get_state()
    context.repository.save(state)
    return state


@app.post("/api/advance", response_model=WorldState)
async def advance(payload: AdvanceRequest) -> WorldState:
    state = context.engine.advance_for_reflection(payload.reason)
    context.repository.save(state)
    return state


@app.post("/api/simulate", response_model=WorldState)
async def simulate() -> WorldState:
    state = context.engine.simulate_world()
    context.repository.save(state)
    return state


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
    event = map_search_result_to_event(results[0], payload.topic, context.engine.get_state().time_slot, payload.category)
    state = context.engine.inject_event(event)
    context.repository.save(state)
    return state


@app.post("/api/macro-news", response_model=WorldState)
async def inject_macro_news(payload: MacroNewsRequest) -> WorldState:
    try:
        event = map_macro_news_to_event(payload, context.engine.get_state().time_slot)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    state = context.engine.inject_event(event)
    context.repository.save(state)
    return state


@app.post("/api/player/trade", response_model=WorldState)
async def player_trade(payload: TradeRequest) -> WorldState:
    try:
        state = context.engine.player_trade(payload.symbol, payload.side, payload.shares)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    context.repository.save(state)
    return state


@app.post("/api/player/auto-trade", response_model=WorldState)
async def player_auto_trade() -> WorldState:
    state = context.engine.auto_trade_player()
    context.repository.save(state)
    return state
