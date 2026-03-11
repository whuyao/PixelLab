from __future__ import annotations

from app.models import Task


def apply_task_progress(tasks: list[Task], focus: str) -> None:
    for task in tasks:
        if task.category == "main":
            task.progress = min(task.target, task.progress + 6)
        elif focus == "dialogue" and task.category == "social":
            task.progress = min(task.target, task.progress + 14)
        elif focus == "news" and task.category == "external":
            task.progress = min(task.target, task.progress + 40)
        elif focus == "rest" and task.category == "daily":
            task.progress = min(task.target, task.progress + 8)
