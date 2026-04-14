from __future__ import annotations

from pathlib import Path
from typing import Sequence

from src.core.models import Finding, RunLog, SourceRecord, WeeklySummary
from src.core.settings import Settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except ImportError:  # pragma: no cover - handled at runtime when dependencies are missing
    Credentials = None
    build = None


class GoogleSheetsClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._service = None

    def _get_service(self):
        if Credentials is None or build is None:
            raise RuntimeError(
                "Google Sheets dependencies are not installed. "
                "Install project dependencies before running with live Sheets writes."
            )
        if self._service is None:
            credentials = Credentials.from_service_account_file(
                Path(self.settings.service_account_file),
                scopes=SCOPES,
            )
            self._service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
        return self._service

    def append_rows(self, target_range: str, rows: Sequence[Sequence[str]]) -> None:
        if not rows:
            return
        body = {"values": [list(row) for row in rows]}
        self._get_service().spreadsheets().values().append(
            spreadsheetId=self.settings.spreadsheet_id,
            range=target_range,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()

    def get_column_values(self, target_range: str) -> list[str]:
        response = self._get_service().spreadsheets().values().get(
            spreadsheetId=self.settings.spreadsheet_id,
            range=target_range,
        ).execute()
        values = response.get("values", [])
        return [row[0] for row in values if row]

    def get_existing_field_values(self, field_name: str) -> set[str]:
        response = self._get_service().spreadsheets().values().get(
            spreadsheetId=self.settings.spreadsheet_id,
            range=self.settings.main_range,
        ).execute()
        values = response.get("values", [])
        if not values:
            return set()
        headers = values[0]
        if field_name not in headers:
            return set()
        index = headers.index(field_name)
        collected: set[str] = set()
        for row in values[1:]:
            if index < len(row) and row[index]:
                collected.add(row[index])
        return collected

    def get_existing_source_urls(self) -> set[str]:
        return self.get_existing_field_values("url")

    def append_findings(self, findings: Sequence[Finding]) -> None:
        self.append_rows(self.settings.main_range, [item.to_row() for item in findings])

    def append_weekly_summary(self, summary: WeeklySummary) -> None:
        self.append_rows(self.settings.main_range, [summary.to_row()])

    def append_sources(self, sources: Sequence[SourceRecord]) -> None:
        self.append_rows(self.settings.main_range, [item.to_row() for item in sources])

    def append_run_log(self, run_log: RunLog) -> None:
        self.append_rows(self.settings.main_range, [run_log.to_row()])
