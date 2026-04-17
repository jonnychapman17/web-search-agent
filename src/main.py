from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.collectors.runner import CollectionRunner
from src.core.config import load_sources, load_themes
from src.core.logging_utils import configure_logging
from src.core.models import Finding, RunLog
from src.core.settings import load_settings
from src.core.time_utils import now_in_timezone
from src.pipeline.classify import classify_jurisdiction, infer_audience, infer_category, infer_theme
from src.pipeline.dates import choose_resource_date, is_fresh_enough
from src.pipeline.dedupe import build_duplicate_key, filter_new_findings
from src.pipeline.discovery import build_source_candidates, filter_new_source_candidates
from src.pipeline.scoring import score_relevance
from src.pipeline.summarize import build_weekly_summary

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the landlord tenant search agent.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write to Google Sheets.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = load_settings()
    configure_logging(settings.log_level)

    run_now = now_in_timezone(settings.timezone)
    run_date = run_now.date().isoformat()
    run_timestamp = run_now.isoformat()
    dry_run = settings.dry_run or args.dry_run

    project_root = Path(__file__).resolve().parents[1]
    config_dir = project_root / "config"
    sources = load_sources(config_dir)
    themes = load_themes(config_dir)

    LOGGER.info("Loaded %s sources and %s themes", len(sources), len(themes))

    collector = CollectionRunner()
    collection_result = collector.collect(sources=sources, discovered_date=run_date)
    raw_items = collection_result.items
    findings = [
        _to_finding(raw_item, run_date=run_date, run_timestamp=run_timestamp)
        for raw_item in raw_items
        if is_fresh_enough(
            raw_item.source_type,
            choose_resource_date(raw_item.published_date, raw_item.updated_date)[0],
            run_now.date(),
            settings.lookback_days,
        )
    ]

    sheets_client = None
    existing_keys: set[str] = set()
    existing_source_urls: set[str] = {source["base_url"] for source in sources}
    if not dry_run:
        from src.outputs.sheets import GoogleSheetsClient

        sheets_client = GoogleSheetsClient(settings)
        LOGGER.info("Fetching existing duplicate keys from Google Sheets")
        existing_keys = set(sheets_client.get_existing_field_values("duplicate_key"))
        existing_source_urls.update(sheets_client.get_existing_source_urls())

    relevant_findings = [item for item in findings if item.priority_score >= settings.relevance_threshold]
    new_findings = filter_new_findings(relevant_findings, existing_keys)
    discovered_sources = build_source_candidates(
        new_findings,
        known_source_urls=existing_source_urls,
        run_date=run_date,
        limit=settings.discovery_max_new_sources_per_run,
    )
    new_source_candidates = filter_new_source_candidates(discovered_sources, existing_source_urls)
    run_status = "success"
    if collection_result.errors and new_findings:
        run_status = "partial_success"
    elif collection_result.errors:
        run_status = "failure"

    summary = build_weekly_summary(run_date, new_findings, new_sources_count=len(new_source_candidates))
    run_log = RunLog(
        run_date=run_date,
        run_timestamp=run_timestamp,
        status=run_status,
        sources_checked=len(sources),
        items_fetched=len(raw_items),
        items_relevant=len(relevant_findings),
        items_written=len(new_findings),
        new_sources_written=len(new_source_candidates),
        errors=" | ".join(collection_result.errors[:10]),
    )

    if dry_run:
        LOGGER.info("Dry run enabled; no Google Sheets writes will be performed")
        LOGGER.info("Would write %s findings", len(new_findings))
        LOGGER.info("Would write %s source candidates", len(new_source_candidates))
        LOGGER.info("Weekly summary: %s", summary.top_themes)
        if collection_result.errors:
            LOGGER.info("Collection errors: %s", run_log.errors)
        return

    LOGGER.info("Writing %s findings to Google Sheets", len(new_findings))
    sheets_client.append_findings(new_findings)
    if new_source_candidates:
        sheets_client.append_sources(new_source_candidates)
    sheets_client.append_weekly_summary(summary)
    sheets_client.append_run_log(run_log)


def _to_finding(raw_item, *, run_date: str, run_timestamp: str) -> Finding:
    audience = infer_audience(raw_item.source_audience)
    category = infer_category(audience)
    jurisdiction = classify_jurisdiction(f"{raw_item.title} {raw_item.text}")
    theme = infer_theme(f"{raw_item.title} {raw_item.text}")
    resource_date, resource_date_type = choose_resource_date(raw_item.published_date, raw_item.updated_date)
    priority_score = score_relevance(
        source_authority=30 if audience == "official" else 18,
        recency=20 if resource_date else 8,
        direct_relevance=20,
        novelty=10,
        discussion_signal=5 if audience == "official" else 12,
    )
    duplicate_key = build_duplicate_key(
        title=raw_item.title,
        url=raw_item.url,
        source_name=raw_item.source_name,
        published_date=raw_item.published_date,
    )
    return Finding(
        run_date=run_date,
        run_timestamp=run_timestamp,
        jurisdiction=jurisdiction,
        audience=audience,
        category=category,
        theme=theme,
        source_name=raw_item.source_name,
        source_type=raw_item.source_type,
        title=raw_item.title,
        url=raw_item.url,
        published_date=raw_item.published_date,
        updated_date=raw_item.updated_date,
        resource_date_type=resource_date_type,
        discovered_date=raw_item.discovered_date,
        summary=raw_item.notes or raw_item.title,
        why_relevant=(
            f"Captured from {raw_item.source_name} during the weekly monitoring run "
            f"and tagged as {category}. Resource date source: {resource_date_type or 'unknown'}."
        ),
        confidence=0.95 if audience == "official" else 0.75,
        priority_score=priority_score,
        duplicate_key=duplicate_key,
    )


if __name__ == "__main__":
    main()
