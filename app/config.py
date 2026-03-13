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
    llm_provider: str
    llm_api_key: str | None
    llm_model: str
    llm_base_url: str
    save_path: Path
    log_path: Path
    secret_file: Path


def load_settings() -> Settings:
    secret_file = Path(os.environ.get("LOCALFARMER_ENV_FILE", "/tmp/localfarmer.env"))
    _load_env_file(secret_file)
    save_path = Path(os.environ.get("SAVE_PATH", "save/localfarmer.db"))
    log_path = Path(os.environ.get("LOG_PATH", "logs/activity.jsonl"))
    provider = os.environ.get("LLM_PROVIDER", "openai").strip().lower() or "openai"
    openai_base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").strip() or "https://api.openai.com/v1"
    qwen_base_url = os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1").strip() or "https://dashscope.aliyuncs.com/compatible-mode/v1"

    if provider == "qwen":
        llm_api_key = os.environ.get("QWEN_API_KEY") or os.environ.get("OPENAI_API_KEY")
        llm_model = os.environ.get("QWEN_MODEL", os.environ.get("OPENAI_MODEL", "qwen3.5-flash"))
        llm_base_url = os.environ.get("LLM_BASE_URL", qwen_base_url)
    else:
        provider = "openai"
        llm_api_key = os.environ.get("OPENAI_API_KEY")
        llm_model = os.environ.get("OPENAI_MODEL", "gpt-5-mini")
        llm_base_url = os.environ.get("LLM_BASE_URL", openai_base_url)

    return Settings(
        brave_api_key=os.environ.get("BRAVE_API_KEY"),
        llm_provider=provider,
        llm_api_key=llm_api_key,
        llm_model=llm_model,
        llm_base_url=llm_base_url,
        save_path=save_path,
        log_path=log_path,
        secret_file=secret_file,
    )
