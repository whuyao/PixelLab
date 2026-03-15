from __future__ import annotations

import re
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

THEME_CN_HINTS = {
    "global markets": "全球市场",
    "central bank": "央行与利率",
    "geopolitics": "地缘与能源",
    "housing": "全球住房",
    "tourism": "全球旅游与消费",
    "geospatial ai": "GeoAI 与空间智能",
    "funding": "科技融资与就业",
    "social media": "社会热点",
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
        if re.search(rf"(?<![a-z]){re.escape(keyword)}(?![a-z])", topic_lower):
            return category
    return default


def _theme_hint_cn(topic: str) -> str:
    lowered = topic.lower()
    for keyword, label in THEME_CN_HINTS.items():
        if keyword in lowered:
            return label
    return {
        "market": "全球经济",
        "geoai": "GeoAI 动向",
        "tech": "科技动向",
        "general": "全球热点",
        "gaming": "游戏行业",
    }.get(infer_category(topic, "general"), "全球热点")


def _tone_label(tone_hint: int, category: EventCategory) -> tuple[str, str]:
    if tone_hint >= 1:
        return (
            "偏利好" if category in {"market", "geoai", "tech"} else "偏热",
            "这条消息更容易被理解成提振预期，可能放大乐观和冒险倾向。",
        )
    if tone_hint <= -1:
        return (
            "偏利空" if category in {"market", "geoai", "tech"} else "偏紧张",
            "这条消息更容易被理解成风险信号，可能压低消费、情绪和市场偏好。",
        )
    return ("高不确定", "这条消息并不单边，大家更可能围绕它争论和反复试探。")


def _headline_phrase(theme_hint: str, tone_hint: int, category: EventCategory) -> str:
    if category == "market":
        if tone_hint >= 1:
            return f"{theme_hint}突发利好"
        if tone_hint <= -1:
            return f"{theme_hint}再起波澜"
        return f"{theme_hint}出现分歧信号"
    if category == "geoai":
        if tone_hint >= 1:
            return f"{theme_hint}热度升温"
        if tone_hint <= -1:
            return f"{theme_hint}推进承压"
        return f"{theme_hint}出现新变量"
    if tone_hint >= 1:
        return f"{theme_hint}讨论升温"
    if tone_hint <= -1:
        return f"{theme_hint}引发担忧"
    return f"{theme_hint}突然冲上议程"


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
    market_strength = 4
    if abs(raw_tone) >= 2:
        market_strength = 5
    impacts = {
        "geoai_progress": 6 if category == "geoai" else 2,
        "collective_reasoning": 5 if category in {"geoai", "tech"} else 2,
        "research_progress": 4 if category != "gaming" else 1,
    }
    theme_hint = _theme_hint_cn(topic)
    tone_label, tone_effect = _tone_label(tone_hint, category)
    source = item.get("profile_name") or item.get("url") or "Brave Search"
    title = _headline_phrase(theme_hint, tone_hint, category)
    summary = f"{source} 捕捉到一条围绕“{theme_hint}”的全球经济消息。{tone_effect}"
    return LabEvent(
        id=f"event-{uuid.uuid4().hex[:8]}",
        category=category,
        title=title,
        summary=summary,
        source=source,
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
