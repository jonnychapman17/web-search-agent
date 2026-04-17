# First Live Run Checklist

Use this in order.

## 1. Confirm the Sheet Tab Name

Open the Google Sheet and check the single tab name.

Use:

- `Sheet1!A:AF` if the tab is named `Sheet1`
- `<YourTabName>!A:AF` if the tab has a different name

Example:

- `Monitoring!A:AF`

## 2. Paste the Header Row

Paste this into row 1 of the single tab:

```text
record_type,run_date,run_timestamp,jurisdiction,audience,category,theme,source_name,source_type,title,url,published_date,updated_date,resource_date_type,discovered_date,summary,why_relevant,confidence,priority_score,duplicate_key,access_method,status,active,notes,review_relevant,review_reason,sources_checked,items_fetched,items_relevant,items_written,new_sources_written,errors
```

## 3. Configure Google Auth

You already created the service account.

Because your org blocks JSON key creation, use Workload Identity Federation instead.

Follow:

- [WIF-SETUP.md](/Users/jonchapman/Documents/New%20project/landlord-tenant-search-agent/docs/WIF-SETUP.md)

## 4. Share the Sheet

Share the Google Sheet with the service account email as an editor.

This email will look something like:

- `agent-name@project-id.iam.gserviceaccount.com`

## 5. Add GitHub Secrets

In the GitHub repo settings, add:

- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SHEETS_MAIN_RANGE`
- `GOOGLE_WIF_PROVIDER`
- `GOOGLE_WIF_SERVICE_ACCOUNT`

Suggested values:

- `GOOGLE_SHEETS_SPREADSHEET_ID=1HyR3YYtmWRmhj7uPklfEVSrV_D7C405DHF7TnzSCryQ`
- `GOOGLE_SHEETS_MAIN_RANGE=2026!A:AF`
- `GOOGLE_WIF_SERVICE_ACCOUNT=web-search-agent@web-search-agent-493311.iam.gserviceaccount.com`

## 6. Manual Workflow Run

Run the GitHub Actions workflow manually using `workflow_dispatch`.

Expected results:

- at least one `run_log` row gets appended
- if fetching works, `finding` rows appear
- if new domains are discovered, `source_candidate` rows appear

## 7. Review the Output

Check:

- `record_type=run_log`
- `status`
- `errors`
- whether any `finding` rows were captured
- whether any `source_candidate` rows were captured

## 8. Tune After First Run

After the first live run:

1. review noisy findings
2. review missing important findings
3. tune `include_keywords`
4. tune `AGENT_RELEVANCE_THRESHOLD`
