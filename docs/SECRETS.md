# Secrets and Runtime Configuration

## Required GitHub Secrets

- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SHEETS_MAIN_RANGE`
- `GOOGLE_WIF_PROVIDER`
- `GOOGLE_WIF_SERVICE_ACCOUNT`

## Recommended Values

- `GOOGLE_SHEETS_MAIN_RANGE=2026!A:AB`

## Notes

- `GOOGLE_WIF_PROVIDER` should look like:
  `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID`
- `GOOGLE_WIF_SERVICE_ACCOUNT` should be the service account email.
- The workflow uses `google-github-actions/auth` to generate short-lived credentials at runtime.
- Keep `AGENT_DRY_RUN=false` only in live environments where credentials and sheet access are ready.

## Optional Future Secrets

Add these later if needed:

- Slack webhook URL for failure alerts
- Reddit API credentials if you switch away from public-page access
