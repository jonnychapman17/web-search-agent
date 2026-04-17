from __future__ import annotations

from datetime import date, datetime


def choose_resource_date(published_date: str, updated_date: str) -> tuple[str, str]:
    if updated_date:
        return updated_date, "updated"
    if published_date:
        return published_date, "published"
    return "", ""


def parse_date_string(value: str) -> date | None:
    cleaned = (value or "").strip()
    if not cleaned:
        return None

    try:
        return datetime.fromisoformat(cleaned.replace("Z", "+00:00")).date()
    except ValueError:
        pass

    for fmt in ("%Y-%m-%d", "%d %B %Y", "%d %b %Y", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    return None


def is_fresh_enough(source_type: str, resource_date: str, run_date: date, lookback_days: int) -> bool:
    parsed = parse_date_string(resource_date)
    if parsed is None:
        return source_type == "official_guidance"

    age_days = (run_date - parsed).days
    if age_days < 0:
        return True

    max_age_by_source_type = {
        "official_guidance": 180,
        "legal_blog": 120,
        "forum_or_publisher": 90,
        "forum": max(lookback_days * 3, 30),
        "social_forum": max(lookback_days * 2, 21),
    }
    max_age = max_age_by_source_type.get(source_type, max(lookback_days * 3, 30))
    return age_days <= max_age
