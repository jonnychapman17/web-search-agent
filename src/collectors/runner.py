from __future__ import annotations

import logging
from dataclasses import dataclass
from collections import defaultdict

from src.collectors.base import RawItem
from src.collectors.community import CommunityCollector
from src.collectors.official import OfficialCollector
from src.collectors.registry import StaticRegistryCollector

LOGGER = logging.getLogger(__name__)


@dataclass
class CollectionResult:
    items: list[RawItem]
    errors: list[str]


class CollectionRunner:
    def __init__(self) -> None:
        self.official_collector = OfficialCollector()
        self.community_collector = CommunityCollector()
        self.placeholder_collector = StaticRegistryCollector()

    def collect(self, sources: list[dict], discovered_date: str) -> CollectionResult:
        items: list[RawItem] = []
        items_by_source: dict[str, int] = defaultdict(int)
        errors: list[str] = []

        for source in sources:
            if not source.get("active", False):
                continue
            source_items, source_errors = self._collect_source(source, discovered_date)
            items.extend(source_items)
            items_by_source[source["source_name"]] += len(source_items)
            errors.extend(source_errors)

        for source_name, count in items_by_source.items():
            LOGGER.info("Collected %s items from %s", count, source_name)

        return CollectionResult(items=items, errors=errors)

    def _collect_source(self, source: dict, discovered_date: str) -> tuple[list[RawItem], list[str]]:
        try:
            if source["audience"] == "official":
                items = self.official_collector.collect(source, discovered_date)
            else:
                items = self.community_collector.collect(source, discovered_date)
            if items:
                return items, []
            return [], [f"No items collected from {source['source_name']}"]
        except Exception as exc:  # pragma: no cover - resilience path
            LOGGER.warning("Collector failed for %s: %s", source["source_name"], exc)
            return self.placeholder_collector.collect([source], discovered_date), [
                f"Collector failed for {source['source_name']}: {exc}"
            ]
