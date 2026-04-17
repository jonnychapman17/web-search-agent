from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Iterable, Optional
from urllib.parse import urljoin

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:  # pragma: no cover - handled at runtime
    BeautifulSoup = None
    Tag = None


@dataclass
class ExtractedLink:
    title: str
    url: str
    published_date: str
    updated_date: str
    text: str


def extract_relevant_links(
    *,
    html: str,
    page_url: str,
    include_keywords: Iterable[str],
    max_items: int,
) -> list[ExtractedLink]:
    if BeautifulSoup is None:
        return []

    soup = BeautifulSoup(html, "html.parser")
    items: list[ExtractedLink] = []
    seen_urls: set[str] = set()
    lowered_keywords = [keyword.lower() for keyword in include_keywords]

    for anchor in soup.find_all("a", href=True):
        href = str(anchor.get("href", "")).strip()
        title = " ".join(anchor.stripped_strings)
        if not href or not title:
            continue

        absolute_url = urljoin(page_url, href)
        haystack = f"{title} {absolute_url}".lower()
        if not any(keyword in haystack for keyword in lowered_keywords):
            continue
        if absolute_url in seen_urls:
            continue

        container_text = _extract_container_text(anchor)
        published_date, updated_date = _extract_dates(anchor, soup)
        items.append(
            ExtractedLink(
                title=title,
                url=absolute_url,
                published_date=published_date,
                updated_date=updated_date,
                text=container_text,
            )
        )
        seen_urls.add(absolute_url)
        if len(items) >= max_items:
            break

    return items


def _extract_dates(anchor: Tag, soup: BeautifulSoup) -> tuple[str, str]:
    published_date = ""
    updated_date = ""
    container = anchor.parent
    for _ in range(4):
        if container is None:
            break
        container_text = " ".join(container.stripped_strings)

        for time_tag in container.find_all("time"):
            time_value = _time_value(time_tag)
            if not time_value:
                continue
            lowered = container_text.lower()
            if any(token in lowered for token in {"updated", "modified", "last updated"}):
                updated_date = updated_date or time_value
            else:
                published_date = published_date or time_value

        published_label_date = _find_labeled_date(container_text, ("published", "posted"))
        updated_label_date = _find_labeled_date(container_text, ("updated", "modified", "last updated"))
        if published_label_date:
            published_date = published_date or published_label_date
        if updated_label_date:
            updated_date = updated_date or updated_label_date
        container = container.parent

    if not published_date:
        published_date = _extract_meta_date(
            soup,
            selectors=(
                ("meta", "property", "article:published_time"),
                ("meta", "name", "article:published_time"),
                ("meta", "name", "publish-date"),
                ("meta", "property", "og:published_time"),
            ),
        )
    if not updated_date:
        updated_date = _extract_meta_date(
            soup,
            selectors=(
                ("meta", "property", "article:modified_time"),
                ("meta", "name", "article:modified_time"),
                ("meta", "name", "last-modified"),
                ("meta", "property", "og:updated_time"),
            ),
        )

    ld_published, ld_updated = _extract_json_ld_dates(soup)
    return published_date or ld_published, updated_date or ld_updated


def _time_value(time_tag: Tag) -> str:
    datetime_value = time_tag.get("datetime")
    if datetime_value:
        return str(datetime_value)
    return " ".join(time_tag.stripped_strings)


def _find_labeled_date(text: str, labels: tuple[str, ...]) -> str:
    date_pattern = (
        r"(\d{4}-\d{2}-\d{2}"
        r"|(?:\d{1,2}\s+[A-Z][a-z]+\s+\d{4})"
        r"|(?:[A-Z][a-z]+\s+\d{1,2},\s+\d{4}))"
    )
    for label in labels:
        match = re.search(rf"{re.escape(label)}[:\s]+{date_pattern}", text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return ""


def _extract_meta_date(soup: BeautifulSoup, selectors: tuple[tuple[str, str, str], ...]) -> str:
    for tag_name, attribute_name, attribute_value in selectors:
        tag = soup.find(tag_name, attrs={attribute_name: attribute_value})
        if tag and tag.get("content"):
            return str(tag.get("content"))
    return ""


def _extract_json_ld_dates(soup: BeautifulSoup) -> tuple[str, str]:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text(strip=True)
        if not raw:
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for item in _iterate_json_ld_items(payload):
            if not isinstance(item, dict):
                continue
            published = str(item.get("datePublished", "") or "")
            updated = str(item.get("dateModified", "") or "")
            if published or updated:
                return published, updated
    return "", ""


def _iterate_json_ld_items(payload):
    if isinstance(payload, list):
        for item in payload:
            yield from _iterate_json_ld_items(item)
        return
    if isinstance(payload, dict) and isinstance(payload.get("@graph"), list):
        for item in payload["@graph"]:
            yield from _iterate_json_ld_items(item)
        return
    yield payload


def _extract_container_text(anchor: Tag) -> str:
    container = _closest_content_container(anchor)
    if container is None:
        return " ".join(anchor.stripped_strings)
    text = " ".join(container.stripped_strings)
    return text[:2000]


def _closest_content_container(anchor: Tag) -> Optional[Tag]:
    container = anchor.parent
    for _ in range(3):
        if container is None:
            return None
        if container.name in {"article", "li", "div", "section"}:
            return container
        container = container.parent
    return anchor.parent
