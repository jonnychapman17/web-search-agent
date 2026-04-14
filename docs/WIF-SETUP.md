# Workload Identity Federation Setup

This is the right path when your organization blocks service account key creation.

Official references:

- [Workload Identity Federation overview](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Workload Identity Federation with deployment pipelines](https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines)
- [google-github-actions/auth](https://github.com/google-github-actions/auth)

## What You Already Have

- Google Cloud project: `Web Search Agent`
- service account:
  `web-search-agent@web-search-agent-493311.iam.gserviceaccount.com`
- Google Sheet shared with that service account

## What You Need Next

1. Create a workload identity pool.
2. Create a GitHub OIDC provider inside that pool.
3. Grant that GitHub identity permission to impersonate the service account.
4. Add the provider and service account values as GitHub secrets.

## Step 1: Open Workload Identity Federation

In Google Cloud:

1. Go to `IAM & Admin`
2. Open `Workload Identity Federation`

## Step 2: Create a Pool

1. Click `Create pool`
2. Use a name like:
   - `github-actions-pool`
3. Save it

Record the pool ID.

## Step 3: Create a Provider for GitHub

Inside that pool:

1. Click `Add provider`
2. Choose `OpenID Connect`
3. Use GitHub's OIDC issuer:
   - `https://token.actions.githubusercontent.com`
4. Configure the allowed audiences if prompted
5. Add attribute mapping and conditions for your GitHub repo

Important:

- restrict this to your specific GitHub repository if possible

Record the full provider resource name. It should look like:

```text
projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID
```

## Step 4: Allow the Provider to Use the Service Account

Grant the principal from the workload identity pool the role:

- `roles/iam.workloadIdentityUser`

Do this on the service account:

- `web-search-agent@web-search-agent-493311.iam.gserviceaccount.com`

## Step 5: Add GitHub Secrets

Add these secrets:

- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SHEETS_MAIN_RANGE`
- `GOOGLE_WIF_PROVIDER`
- `GOOGLE_WIF_SERVICE_ACCOUNT`

For your setup:

```text
GOOGLE_SHEETS_SPREADSHEET_ID=1HyR3YYtmWRmhj7uPklfEVSrV_D7C405DHF7TnzSCryQ
GOOGLE_SHEETS_MAIN_RANGE=2026!A:AB
GOOGLE_WIF_SERVICE_ACCOUNT=web-search-agent@web-search-agent-493311.iam.gserviceaccount.com
```

## Step 6: Run the Workflow Manually

Once the provider is configured and the secrets are added:

1. go to GitHub Actions
2. run `Weekly Landlord Tenant Agent`
3. review the result

## What To Send Me Next

When you get to the provider step, send me:

- the provider resource name
- or a screenshot of the provider creation screen

Then I can help verify the exact value for `GOOGLE_WIF_PROVIDER`.
