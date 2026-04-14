from __future__ import annotations

from dataclasses import dataclass

UNIFIED_HEADERS = [
    "record_type",
    "run_date",
    "run_timestamp",
    "jurisdiction",
    "audience",
    "category",
    "theme",
    "source_name",
    "source_type",
    "title",
    "url",
    "published_date",
    "discovered_date",
    "summary",
    "why_relevant",
    "confidence",
    "priority_score",
    "duplicate_key",
    "access_method",
    "status",
    "active",
    "notes",
    "sources_checked",
    "items_fetched",
    "items_relevant",
    "items_written",
    "new_sources_written",
    "errors",
]


def _build_unified_row(values: dict[str, str]) -> list[str]:
    return [str(values.get(header, "")) for header in UNIFIED_HEADERS]


@dataclass
class Finding:
    run_date: str
    run_timestamp: str
    jurisdiction: str
    audience: str
    category: str
    theme: str
    source_name: str
    source_type: str
    title: str
    url: str
    published_date: str
    discovered_date: str
    summary: str
    why_relevant: str
    confidence: float
    priority_score: int
    duplicate_key: str

    def to_row(self) -> list[str]:
        return _build_unified_row(
            {
                "record_type": "finding",
                "run_date": self.run_date,
                "run_timestamp": self.run_timestamp,
                "jurisdiction": self.jurisdiction,
                "audience": self.audience,
                "category": self.category,
                "theme": self.theme,
                "source_name": self.source_name,
                "source_type": self.source_type,
                "title": self.title,
                "url": self.url,
                "published_date": self.published_date,
                "discovered_date": self.discovered_date,
                "summary": self.summary,
                "why_relevant": self.why_relevant,
                "confidence": f"{self.confidence:.2f}",
                "priority_score": str(self.priority_score),
                "duplicate_key": self.duplicate_key,
            }
        )


@dataclass
class WeeklySummary:
    run_date: str
    official_updates_summary: str
    landlord_concerns_summary: str
    tenant_concerns_summary: str
    top_themes: str
    new_sources_found: str

    def to_row(self) -> list[str]:
        return _build_unified_row(
            {
                "record_type": "weekly_summary",
                "run_date": self.run_date,
                "summary": self.official_updates_summary,
                "why_relevant": self.landlord_concerns_summary,
                "notes": self.tenant_concerns_summary,
                "items_written": self.top_themes,
                "new_sources_written": self.new_sources_found,
            }
        )


@dataclass
class SourceRecord:
    source_name: str
    base_url: str
    source_type: str
    jurisdiction: str
    audience: str
    access_method: str
    discovery_date: str
    status: str
    active: bool
    notes: str

    def to_row(self) -> list[str]:
        return _build_unified_row(
            {
                "record_type": "source_candidate",
                "jurisdiction": self.jurisdiction,
                "audience": self.audience,
                "source_name": self.source_name,
                "source_type": self.source_type,
                "url": self.base_url,
                "discovered_date": self.discovery_date,
                "access_method": self.access_method,
                "status": self.status,
                "active": str(self.active).lower(),
                "notes": self.notes,
            }
        )


@dataclass
class RunLog:
    run_date: str
    run_timestamp: str
    status: str
    sources_checked: int
    items_fetched: int
    items_relevant: int
    items_written: int
    new_sources_written: int
    errors: str

    def to_row(self) -> list[str]:
        return _build_unified_row(
            {
                "record_type": "run_log",
                "run_date": self.run_date,
                "run_timestamp": self.run_timestamp,
                "status": self.status,
                "sources_checked": str(self.sources_checked),
                "items_fetched": str(self.items_fetched),
                "items_relevant": str(self.items_relevant),
                "items_written": str(self.items_written),
                "new_sources_written": str(self.new_sources_written),
                "errors": self.errors,
            }
        )
