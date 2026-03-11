from __future__ import annotations

import uuid

from app.models import EventCategory, LabEvent, TimeSlot


def build_internal_event(title: str, summary: str, slot: TimeSlot, category: EventCategory = "general") -> LabEvent:
    return LabEvent(
        id=f"event-{uuid.uuid4().hex[:8]}",
        category=category,
        title=title,
        summary=summary,
        source="lab",
        time_slot=slot,
        impacts={},
        participants=[],
    )
