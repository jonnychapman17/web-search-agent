from src.core.models import Finding
from src.pipeline.summarize import build_weekly_summary


def _finding(category: str, theme: str, title: str) -> Finding:
    return Finding(
        run_date="2026-04-14",
        run_timestamp="2026-04-14T08:00:00+01:00",
        jurisdiction="England",
        audience="official",
        category=category,
        theme=theme,
        source_name="Example",
        source_type="official_guidance",
        title=title,
        url="https://example.com",
        published_date="2026-04-10",
        updated_date="2026-04-11",
        resource_date_type="updated",
        discovered_date="2026-04-14",
        summary="summary",
        why_relevant="relevant",
        confidence=0.95,
        priority_score=60,
        duplicate_key=title,
    )


def test_build_weekly_summary_collects_top_themes() -> None:
    summary = build_weekly_summary(
        "2026-04-14",
        [
            _finding("official_update", "epc", "EPC update"),
            _finding("landlord_concern", "epc", "Landlord EPC concern"),
            _finding("tenant_concern", "repairs_and_disrepair", "Tenant mould issue"),
        ],
        new_sources_count=2,
    )
    assert "epc" in summary.top_themes
    assert summary.new_sources_found == "2"
