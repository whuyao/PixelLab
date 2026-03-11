from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip()


@dataclass(slots=True)
class Settings:
    brave_api_key: str | None
    openai_api_key: str | None
    openai_model: str
    save_path: Path
    log_path: Path
    secret_file: Path


def load_settings() -> Settings:
    secret_file = Path(os.environ.get("LOCALFARMER_ENV_FILE", "/tmp/localfarmer.env"))
    _load_env_file(secret_file)
    save_path = Path(os.environ.get("SAVE_PATH", "save/localfarmer.db"))
    log_path = Path(os.environ.get("LOG_PATH", "logs/activity.jsonl"))
    return Settings(
        brave_api_key=os.environ.get("BRAVE_API_KEY"),
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        openai_model=os.environ.get("OPENAI_MODEL", "gpt-5-mini"),
        save_path=save_path,
        log_path=log_path,
        secret_file=secret_file,
    )
