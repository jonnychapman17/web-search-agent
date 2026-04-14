from src.core.models import Finding
from src.pipeline.discovery import build_source_candidates, filter_new_source_candidates, normalize_domain


def _finding(url: str) -> Finding:
    return Finding(
        run_date="2026-04-14",
        run_timestamp="2026-04-14T08:00:00+01:00",
        jurisdiction="England",
        audience="landlord",
        category="landlord_concern",
        theme="other",
        source_name="Example Source",
        source_type="forum",
        title="Interesting external link",
        url=url,
        published_date="",
        discovered_date="2026-04-14",
        summary="summary",
        why_relevant="relevant",
        confidence=0.75,
        priority_score=50,
        duplicate_key="abc",
    )


def test_normalize_domain_strips_www() -> None:
    assert normalize_domain("https://www.example.com/path") == "example.com"


def test_build_source_candidates_ignores_known_domains() -> None:
    findings = [_finding("https://newsite.example/articles/1"), _finding("https://www.gov.uk/guidance/1")]
    candidates = build_source_candidates(
        findings=findings,
        known_source_urls={"https://gov.uk/"},
        run_date="2026-04-14",
        limit=10,
    )
    assert len(candidates) == 1
    assert candidates[0].base_url == "https://newsite.example/"


def test_filter_new_source_candidates_removes_existing_registry_rows() -> None:
    candidates = build_source_candidates(
        findings=[_finding("https://forum.example/thread/1")],
        known_source_urls=set(),
        run_date="2026-04-14",
        limit=10,
    )
    filtered = filter_new_source_candidates(candidates, {"https://forum.example/"})
    assert filtered == []
