# Google Sheet Setup

Target sheet:

- [Residential landlord and tenant tracking sheet](https://docs.google.com/spreadsheets/d/1HyR3YYtmWRmhj7uPklfEVSrV_D7C405DHF7TnzSCryQ/edit?usp=sharing)

## Required Sheet Structure

Use one single tab only. The agent writes all row types into the same table.

Recommended tab name:

- `Sheet1`

Paste this header row into row 1:

```text
record_type,run_date,run_timestamp,jurisdiction,audience,category,theme,source_name,source_type,title,url,published_date,updated_date,resource_date_type,discovered_date,summary,why_relevant,confidence,priority_score,duplicate_key,access_method,status,active,notes,review_relevant,review_reason,sources_checked,items_fetched,items_relevant,items_written,new_sources_written,errors
```

`record_type` values used by the agent:

- `finding`
- `weekly_summary`
- `source_candidate`
- `run_log`

## Service Account Setup

1. Create a Google Cloud project.
2. Enable the Google Sheets API.
3. Create a service account for this agent.
4. Generate a JSON key.
5. Share the Google Sheet with the service account email as an editor.

Important assumption:

- this setup assumes your single tab can be addressed as `Sheet1`
- if the actual tab has a different name, change `GOOGLE_SHEETS_MAIN_RANGE` accordingly

## Expected Secret Values

Set these values in your runtime or GitHub repository secrets:

- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `GOOGLE_SHEETS_MAIN_RANGE`

Suggested ranges:

- `2026!A:AF`

## First Live Test

Before relying on the schedule:

1. Run the workflow manually with `workflow_dispatch`.
2. Confirm one row appears with `record_type=run_log`.
3. Confirm content rows append with `record_type=finding` when the agent can fetch content.
4. Confirm new domains are added as `record_type=source_candidate` with `status=candidate` and `active=false`.
