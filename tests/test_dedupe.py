from src.pipeline.dedupe import build_duplicate_key, normalize_url


def test_normalize_url_strips_query_and_fragment() -> None:
    url = "https://example.com/path/?q=1#section"
    assert normalize_url(url) == "https://example.com/path"


def test_duplicate_key_is_stable() -> None:
    first = build_duplicate_key("Test", "https://example.com?a=1", "Source", "2026-04-14")
    second = build_duplicate_key("Test", "https://example.com?a=2", "Source", "2026-04-14")
    assert first == second
