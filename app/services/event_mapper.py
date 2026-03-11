from __future__ import annotations

import uuid

from app.models import EventCategory, LabEvent, MacroNewsRequest, TimeSlot


KEYWORD_CATEGORY_MAP: dict[str, EventCategory] = {
    "geo": "geoai",
    "spatial": "geoai",
    "mapping": "geoai",
    "llm": "tech",
    "ai": "tech",
    "chip": "tech",
    "market": "market",
    "stock": "market",
    "game": "gaming",
    "steam": "gaming",
}


def infer_category(topic: str, default: EventCategory) -> EventCategory:
    topic_lower = topic.lower()
    for keyword, category in KEYWORD_CATEGORY_MAP.items():
        if keyword in topic_lower:
            return category
    return default


def map_search_result_to_event(item: dict[str, str], topic: str, slot: TimeSlot, default_category: EventCategory) -> LabEvent:
    category = infer_category(topic, default_category)
    tone_hint = 1 if category in {"geoai", "tech", "market"} else 0
    impacts = {
        "geoai_progress": 6 if category == "geoai" else 2,
        "collective_reasoning": 5 if category in {"geoai", "tech"} else 2,
        "research_progress": 4 if category != "gaming" else 1,
    }
    summary = item.get("description") or item.get("age") or "Fresh signal imported through the lab terminal."
    return LabEvent(
        id=f"event-{uuid.uuid4().hex[:8]}",
        category=category,
        title=item.get("title", topic.title()),
        summary=summary,
        source=item.get("profile_name") or item.get("url") or "Brave Search",
        time_slot=slot,
        impacts=impacts,
        participants=[],
        tone_hint=tone_hint,
        market_target="broad",
        market_strength=2,
    )


def map_macro_news_to_event(payload: MacroNewsRequest, slot: TimeSlot) -> LabEvent:
    tone_hint = {"bullish": 2, "bearish": -2, "volatile": 0}[payload.tone]
    intensity = max(1, min(5, payload.strength))
    title = payload.title.strip()
    summary = payload.summary.strip()
    if not title:
        raise ValueError("先写一个你要发布的新闻标题。")
    if not summary:
        summary = {
            "bullish": "你发布了一条偏利好的宏观消息，市场开始提高风险偏好。",
            "bearish": "你发布了一条偏利空的宏观消息，市场开始主动避险。",
            "volatile": "你发布了一条高不确定性的宏观消息，市场开始剧烈摇摆。",
        }[payload.tone]
    impacts = {
        "geoai_progress": 3 if payload.category == "geoai" and tone_hint > 0 else 0,
        "collective_reasoning": 2 if payload.category in {"geoai", "tech"} else 1,
        "research_progress": 2 if payload.category != "gaming" else 0,
    }
    return LabEvent(
        id=f"event-{uuid.uuid4().hex[:8]}",
        category=payload.category,
        title=title,
        summary=summary,
        source="玩家宏观调控",
        time_slot=slot,
        impacts=impacts,
        participants=["player"],
        tone_hint=tone_hint,
        market_target=payload.target,
        market_strength=intensity,
    )
