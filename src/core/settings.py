from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Settings:
    spreadsheet_id: str
    service_account_file: str
    main_range: str
    timezone: str
    schedule_day: str
    schedule_hour: int
    lookback_days: int
    relevance_threshold: int
    discovery_enabled: bool
    discovery_max_new_sources_per_run: int
    reddit_access_mode: str
    dry_run: bool
    log_level: str


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings() -> Settings:
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)

    return Settings(
        spreadsheet_id=os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", ""),
        service_account_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", ""),
        main_range=os.getenv("GOOGLE_SHEETS_MAIN_RANGE", "Sheet1!A:AF"),
        timezone=os.getenv("AGENT_TIMEZONE", "Europe/London"),
        schedule_day=os.getenv("AGENT_SCHEDULE_DAY", "FR"),
        schedule_hour=int(os.getenv("AGENT_SCHEDULE_HOUR", "8")),
        lookback_days=int(os.getenv("AGENT_LOOKBACK_DAYS", "10")),
        relevance_threshold=int(os.getenv("AGENT_RELEVANCE_THRESHOLD", "40")),
        discovery_enabled=_get_bool("DISCOVERY_ENABLED", True),
        discovery_max_new_sources_per_run=int(os.getenv("DISCOVERY_MAX_NEW_SOURCES_PER_RUN", "25")),
        reddit_access_mode=os.getenv("REDDIT_ACCESS_MODE", "public_page"),
        dry_run=_get_bool("AGENT_DRY_RUN", True),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
