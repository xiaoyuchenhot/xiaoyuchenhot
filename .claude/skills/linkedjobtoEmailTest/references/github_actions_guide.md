# GitHub Actions Setup Guide

## How the Workflow Runs

The job digest workflow triggers in two ways:
- **Scheduled**: Every Monday ~9am AEST (Sunday 11pm UTC) via `cron`
- **Manual**: Any time via the "Run workflow" button in the Actions tab

## Cron Schedule Reference

```
┌─ minute (0-59)
│  ┌─ hour in UTC (0-23)
│  │  ┌─ day of month (1-31)
│  │  │  ┌─ month (1-12)
│  │  │  │  ┌─ day of week (0=Sun, 1=Mon … 6=Sat)
│  │  │  │  │
0  23  *  *  0     → Sunday 11pm UTC = Monday 9am AEST (UTC+10)
```

Common AEST-friendly schedules:

| Cron | UTC time | AEST time |
|---|---|---|
| `0 23 * * 0` | Sunday 11pm | Monday 9am |
| `0 21 * * 0` | Sunday 9pm | Monday 7am |
| `0 22 * * 6` | Saturday 10pm | Sunday 8am |

> **Note:** GitHub Actions cron runs from the **default branch** only. `workflow_dispatch` can be triggered from any branch.

## Adding GitHub Secrets

1. Go to your repo on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:

| Secret name | Description |
|---|---|
| `GMAIL_USER` | Sender Gmail address |
| `GMAIL_APP_PASSWORD` | 16-char Gmail app password (see gmail_setup_guide.md) |
| `RECIPIENT_EMAIL` | Destination email address |

Secrets are encrypted and never shown again after creation. To update, click the secret name → **Update**.

## Triggering a Manual Test Run

1. Go to **Actions** tab in your GitHub repo
2. Click **Weekly Job Digest** in the left workflow list
3. Click **Run workflow** (top right of the run list)
4. Select the branch and click **Run workflow**

> The workflow must be on the **default branch** to appear in the list. Merge your PR first if it doesn't show.

## Reading the Logs

Click on a run → **send-digest** job to see step-by-step output:

- `Found N listing(s)` — scraping succeeded for that keyword
- `Total unique jobs after deduplication: N` — how many jobs will be in the email
- `Email sent to ...` — email was sent successfully
- `SMTPAuthenticationError` — Gmail credentials issue (see gmail_setup_guide.md)

## Re-running a Failed Job

On the failed run page, click **Re-run jobs** → **Re-run failed jobs**.
This is useful after fixing a secret without needing to push new code.
