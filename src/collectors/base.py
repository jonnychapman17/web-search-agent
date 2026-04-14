from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RawItem:
    source_name: str
    source_type: str
    source_audience: str
    title: str
    url: str
    published_date: str
    discovered_date: str
    text: str
    notes: str = ""
