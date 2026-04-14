from __future__ import annotations

from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def load_sources(config_dir: Path) -> list[dict]:
    data = load_yaml(config_dir / "sources.yml")
    return data.get("sources", [])


def load_themes(config_dir: Path) -> list[str]:
    data = load_yaml(config_dir / "themes.yml")
    return data.get("themes", [])
