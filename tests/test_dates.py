from datetime import date

from src.pipeline.dates import choose_resource_date, is_fresh_enough, parse_date_string


def test_choose_resource_date_prefers_updated() -> None:
    resource_date, resource_date_type = choose_resource_date("2026-04-01", "2026-04-10")
    assert resource_date == "2026-04-10"
    assert resource_date_type == "updated"


def test_parse_date_string_handles_human_date() -> None:
    assert parse_date_string("10 April 2026") == date(2026, 4, 10)


def test_is_fresh_enough_rejects_old_forum_content() -> None:
    assert not is_fresh_enough("forum", "2025-01-01", date(2026, 4, 14), 10)
