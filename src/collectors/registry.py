from __future__ import annotations

from typing import Iterable

from src.collectors.base import RawItem


class StaticRegistryCollector:
    """Temporary collector that turns source config into placeholder findings for dry-run validation."""

    def collect(self, sources: Iterable[dict], discovered_date: str) -> list[RawItem]:
        items: list[RawItem] = []
        for source in sources:
            if not source.get("active", False):
                continue
            items.append(
                RawItem(
                    source_name=source["source_name"],
                    source_type=source["source_type"],
                    source_audience=source["audience"],
                    title=f"Collector placeholder for {source['source_name']}",
                    url=source["base_url"],
                    published_date="",
                    updated_date="",
                    discovered_date=discovered_date,
                    text=source.get("notes", ""),
                    notes="Placeholder item generated during scaffold phase.",
                )
            )
        return items
