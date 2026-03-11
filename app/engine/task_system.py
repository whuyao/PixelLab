from __future__ import annotations

from app.models import Task


def apply_task_progress(tasks: list[Task], focus: str) -> None:
    for task in tasks:
        if focus == "dialogue" and task.category == "social":
            task.progress = min(task.target, task.progress + 14)
        elif focus == "news" and task.category == "external":
            task.progress = min(task.target, task.progress + 24)
        elif focus == "rest" and task.category == "daily":
            task.progress = min(task.target, task.progress + 8)
