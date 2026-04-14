from __future__ import annotations

from collections import Counter

from src.core.models import Finding, WeeklySummary


def build_weekly_summary(run_date: str, findings: list[Finding], new_sources_count: int) -> WeeklySummary:
    official = [item.title for item in findings if item.category == "official_update"]
    landlord = [item.title for item in findings if item.category == "landlord_concern"]
    tenant = [item.title for item in findings if item.category == "tenant_concern"]
    theme_counts = Counter(item.theme for item in findings if item.theme)
    top_themes = ", ".join(theme for theme, _ in theme_counts.most_common(5)) or "none"

    return WeeklySummary(
        run_date=run_date,
        official_updates_summary=_join_titles(official),
        landlord_concerns_summary=_join_titles(landlord),
        tenant_concerns_summary=_join_titles(tenant),
        top_themes=top_themes,
        new_sources_found=str(new_sources_count),
    )


def _join_titles(items: list[str], limit: int = 5) -> str:
    if not items:
        return "No notable items captured."
    return "; ".join(items[:limit])
