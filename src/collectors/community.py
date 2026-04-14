from __future__ import annotations

from src.collectors.base import RawItem
from src.collectors.http import fetch_html
from src.collectors.parser import extract_relevant_links


class CommunityCollector:
    def collect(self, source: dict, discovered_date: str) -> list[RawItem]:
        items: list[RawItem] = []
        seed_urls = source.get("seed_urls", [source["base_url"]])
        include_keywords = source.get("include_keywords", [])
        max_items = int(source.get("max_items", 20))

        for seed_url in seed_urls:
            html = fetch_html(seed_url)
            if not html:
                continue
            extracted = extract_relevant_links(
                html=html,
                page_url=seed_url,
                include_keywords=include_keywords,
                max_items=max_items,
            )
            for link in extracted:
                items.append(
                    RawItem(
                        source_name=source["source_name"],
                        source_type=source["source_type"],
                        source_audience=source["audience"],
                        title=link.title,
                        url=link.url,
                        published_date=link.published_date,
                        discovered_date=discovered_date,
                        text=link.text,
                        notes=f"Captured from {source['source_name']} community page {seed_url}.",
                    )
                )
            if len(items) >= max_items:
                break
        return items[:max_items]
