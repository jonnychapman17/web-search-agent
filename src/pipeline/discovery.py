from __future__ import annotations

from collections import OrderedDict
from urllib.parse import urlparse

from src.core.models import Finding, SourceRecord


def normalize_domain(url: str) -> str:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def build_source_candidates(
    findings: list[Finding],
    known_source_urls: set[str],
    run_date: str,
    limit: int,
) -> list[SourceRecord]:
    known_domains = {normalize_domain(url) for url in known_source_urls if url}
    candidates: "OrderedDict[str, SourceRecord]" = OrderedDict()

    for finding in findings:
        domain = normalize_domain(finding.url)
        if not domain or domain in known_domains or domain in candidates:
            continue
        candidates[domain] = SourceRecord(
            source_name=_make_source_name(domain),
            base_url=f"https://{domain}/",
            source_type="candidate_source",
            jurisdiction=finding.jurisdiction,
            audience=finding.audience,
            access_method="discovered_from_finding",
            discovery_date=run_date,
            status="candidate",
            active=False,
            notes=(
                f"Discovered from finding '{finding.title}' captured from {finding.source_name}."
            ),
        )
        if len(candidates) >= limit:
            break

    return list(candidates.values())


def filter_new_source_candidates(
    candidates: list[SourceRecord],
    existing_registry_urls: set[str],
) -> list[SourceRecord]:
    existing_domains = {normalize_domain(url) for url in existing_registry_urls if url}
    return [
        candidate
        for candidate in candidates
        if normalize_domain(candidate.base_url) not in existing_domains
    ]


def _make_source_name(domain: str) -> str:
    parts = [part for part in domain.split(".") if part not in {"co", "uk", "com", "org", "gov"}]
    if not parts:
        return domain
    return " ".join(part.capitalize() for part in parts)
