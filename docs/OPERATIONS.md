# Operations Guide

## Run Schedule

- Weekly
- Friday
- 08:00 Europe/London

## Local Run

```bash
python3 src/main.py --dry-run
```

For live Sheets writes:

1. Install dependencies from `pyproject.toml`
2. Create `.env` from `.env.example`
3. Set `AGENT_DRY_RUN=false`
4. Provide a valid Google service account JSON file
5. Share the target sheet with the service account email

## Recommended Scheduler

GitHub Actions is the easiest first production target.

Suggested cron:

- `0 8 * * 5`

This must be paired with `TZ=Europe/London` handling in the runtime or workflow.

## Failure Handling

The agent now:

- retries failed fetches with linear backoff
- records source-level collection failures in the run log
- marks runs as `failure` when no findings were collected and fetch errors occurred
- marks runs as `partial_success` when some findings were collected but some sources failed

## Source Discovery

New source candidates are derived from domains found in newly written findings.

Rules:

- known configured domains are ignored
- existing `Source Registry` domains are ignored
- new domains are appended as `candidate`
- candidates are created with `active=false`

## Recommended Next Live Setup

1. Create the single target tab in Google Sheets with the unified header row.
2. Install dependencies locally or in CI.
3. Add Google service account credentials.
4. Run one live test append.
5. Review first captured findings and candidate sources.
6. Tune threshold and keywords after the first 2 to 3 runs.

Supporting docs:

- [SHEET-SETUP.md](/Users/jonchapman/Documents/New%20project/landlord-tenant-search-agent/docs/SHEET-SETUP.md)
- [SECRETS.md](/Users/jonchapman/Documents/New%20project/landlord-tenant-search-agent/docs/SECRETS.md)
- [FIRST-LIVE-RUN.md](/Users/jonchapman/Documents/New%20project/landlord-tenant-search-agent/docs/FIRST-LIVE-RUN.md)
- [WIF-SETUP.md](/Users/jonchapman/Documents/New%20project/landlord-tenant-search-agent/docs/WIF-SETUP.md)

## GitHub Actions Example

```yaml
name: Weekly Landlord Tenant Agent

on:
  schedule:
    - cron: "0 7 * * 5"
  workflow_dispatch:

jobs:
  run-agent:
    runs-on: ubuntu-latest
    env:
      TZ: Europe/London
      AGENT_DRY_RUN: "false"
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install .
      - run: python src/main.py
```

Note:

- GitHub cron is UTC. During British Summer Time, `08:00 Europe/London` is `07:00 UTC`.
