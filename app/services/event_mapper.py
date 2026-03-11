from __future__ import annotations

import uuid

from app.models import EventCategory, LabEvent, TimeSlot


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
    )
