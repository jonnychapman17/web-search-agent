from __future__ import annotations

import logging
import time
from typing import Optional

try:
    import requests
except ImportError:  # pragma: no cover - handled at runtime
    requests = None

LOGGER = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; LandlordTenantSearchAgent/0.1; "
        "+https://example.invalid/agent)"
    )
}


def fetch_html(url: str, timeout: int = 20, retries: int = 2, backoff_seconds: float = 1.0) -> Optional[str]:
    if requests is None:
        LOGGER.warning("requests is not installed; skipping fetch for %s", url)
        return None

    attempt = 0
    while attempt <= retries:
        try:
            response = requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            if attempt >= retries:
                LOGGER.warning("Failed to fetch %s: %s", url, exc)
                return None
            sleep_for = backoff_seconds * (attempt + 1)
            LOGGER.info("Retrying %s after %.1fs due to fetch error", url, sleep_for)
            time.sleep(sleep_for)
            attempt += 1
    return None
