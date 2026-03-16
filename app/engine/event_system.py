from __future__ import annotations

import uuid

from app.models import EventCategory, LabEvent, TimeSlot


def build_internal_event(
    title: str,
    summary: str,
    slot: TimeSlot,
    category: EventCategory = "general",
    market_target: str = "broad",
    market_strength: int = 2,
    tone_hint: int = 0,
) -> LabEvent:
    return LabEvent(
        id=f"event-{uuid.uuid4().hex[:8]}",
        category=category,
        title=title,
        summary=summary,
        source="lab",
        time_slot=slot,
        impacts={},
        participants=[],
        market_target=market_target,
        market_strength=market_strength,
        tone_hint=tone_hint,
    )
