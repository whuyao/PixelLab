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

POSITIVE_MARKET_WORDS = ["增长", "回暖", "提振", "利好", "宽松", "支持", "修复", "上调", "复苏", "融资"]
NEGATIVE_MARKET_WORDS = ["衰退", "收紧", "下滑", "风险", "抛售", "暴跌", "违约", "裁员", "承压", "监管"]
TARGET_KEYWORDS = {
    "GEO": ["geoai", "spatial", "mapping", "地图", "推理"],
    "AGR": ["agri", "food", "farm", "消费", "农业", "天气"],
    "SIG": ["signal", "chip", "tech", "cloud", "算力", "科技", "芯片"],
}


def infer_category(topic: str, default: EventCategory) -> EventCategory:
    topic_lower = topic.lower()
    for keyword, category in KEYWORD_CATEGORY_MAP.items():
        if keyword in topic_lower:
            return category
    return default


def map_search_result_to_event(item: dict[str, str], topic: str, slot: TimeSlot, default_category: EventCategory) -> LabEvent:
    category = infer_category(topic, default_category)
    combined_text = f"{topic} {item.get('title', '')} {item.get('description', '')}".lower()
    positive_hits = sum(1 for keyword in POSITIVE_MARKET_WORDS if keyword in combined_text)
    negative_hits = sum(1 for keyword in NEGATIVE_MARKET_WORDS if keyword in combined_text)
    raw_tone = positive_hits - negative_hits
    tone_hint = max(-2, min(2, raw_tone))
    if tone_hint == 0 and category in {"geoai", "tech", "market"}:
        tone_hint = 1
    market_target = "broad"
    for symbol, keywords in TARGET_KEYWORDS.items():
        if any(keyword in combined_text for keyword in keywords):
            market_target = symbol
            break
    market_strength = 2
    if abs(raw_tone) >= 2:
        market_strength = 4
    elif positive_hits or negative_hits:
        market_strength = 3
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
        market_target=market_target,
        market_strength=market_strength,
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
