from __future__ import annotations

from dataclasses import dataclass
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
        items.append(
            ExtractedLink(
                title=title,
                url=absolute_url,
                published_date=_extract_published_date(anchor),
                text=container_text,
            )
        )
        seen_urls.add(absolute_url)
        if len(items) >= max_items:
            break

    return items


def _extract_published_date(anchor: Tag) -> str:
    container = anchor.parent
    for _ in range(4):
        if container is None:
            break
        time_tag = container.find("time")
        if time_tag:
            datetime_value = time_tag.get("datetime")
            if datetime_value:
                return str(datetime_value)
            text_value = " ".join(time_tag.stripped_strings)
            if text_value:
                return text_value
        container = container.parent
    return ""


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
