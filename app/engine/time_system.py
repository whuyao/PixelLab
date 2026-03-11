from __future__ import annotations

from app.models import TimeSlot

TIME_SLOTS: list[TimeSlot] = ["morning", "noon", "afternoon", "evening", "night"]

LIGHTING_BY_SLOT: dict[TimeSlot, str] = {
    "morning": "#f7d89b",
    "noon": "#efe6b8",
    "afternoon": "#e6c48e",
    "evening": "#b97c5e",
    "night": "#4e5475",
}

LABEL_BY_SLOT: dict[TimeSlot, str] = {
    "morning": "Morning",
    "noon": "Noon",
    "afternoon": "Afternoon",
    "evening": "Evening",
    "night": "Night",
}


def advance_time(day: int, slot: TimeSlot) -> tuple[int, TimeSlot]:
    index = TIME_SLOTS.index(slot)
    if index == len(TIME_SLOTS) - 1:
        return day + 1, TIME_SLOTS[0]
    return day, TIME_SLOTS[index + 1]
