from __future__ import annotations

import hashlib
from urllib.parse import urlparse, urlunparse

from src.core.models import Finding


def normalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    cleaned = parsed._replace(query="", fragment="")
    return urlunparse(cleaned).rstrip("/")


def build_duplicate_key(title: str, url: str, source_name: str, published_date: str) -> str:
    payload = "||".join(
        [
            title.strip().lower(),
            normalize_url(url).lower(),
            source_name.strip().lower(),
            published_date.strip(),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def filter_new_findings(findings: list[Finding], existing_keys: set[str]) -> list[Finding]:
    return [finding for finding in findings if finding.duplicate_key not in existing_keys]
