---
name: linkedjobtoEmailTest
description: Sets up an automated weekly LinkedIn job digest that scrapes relevant job listings and emails them via Gmail. Creates a Python scraper, Gmail SMTP sender, and GitHub Actions workflow. Use when a user wants to receive a weekly email digest of LinkedIn jobs filtered by keywords and location.
---

# LinkedIn Job to Email Digest

Automates a weekly LinkedIn job search digest delivered to a Gmail inbox via GitHub Actions.

## What This Skill Does

1. Asks the user for their job preferences (keywords, location, email service)
2. Creates `scripts/job_digest.py` — scrapes LinkedIn guest API, deduplicates results, sends HTML email via Gmail SMTP
3. Creates `requirements.txt` — `requests` and `beautifulsoup4`
4. Creates `.github/workflows/job-digest.yml` — scheduled weekly run (Monday 9am AEST) with `workflow_dispatch` for manual testing

## Setup Steps

### Step 1 — Collect user preferences

Ask the user (use AskUserQuestion with 4 questions):
- What job types/keywords to search (e.g. "Microsoft Azure", "SAP", "AI Engineer")
- What location (default: Sydney, New South Wales, Australia)
- Which email service (Gmail recommended)
- How to run (GitHub Actions recommended)

### Step 2 — Create the three files

**`scripts/job_digest.py`** must include:
- `search_linkedin_jobs(query, location, days=7)` — fetches LinkedIn guest endpoint:
  `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={query}&location={location}&f_TPR=r604800&start=0`
  Parse HTML with BeautifulSoup to extract: title, company, location, date, URL, job ID
- `deduplicate(jobs_by_category)` — removes duplicate jobs across keyword searches
- `build_html_email(jobs_by_category)` — renders grouped HTML table with job title links
- `send_email(html, subject)` — sends via Gmail SMTP port 587 TLS using `smtplib`
- `main()` — runs all searches, deduplicates, builds email, sends; reads config from env vars:
  - `GMAIL_USER`, `GMAIL_APP_PASSWORD`, `RECIPIENT_EMAIL`

**`requirements.txt`**:
```
requests==2.31.0
beautifulsoup4==4.12.3
```

**`.github/workflows/job-digest.yml`**:
```yaml
name: Weekly Job Digest
on:
  schedule:
    - cron: '0 23 * * 0'  # Sunday 11pm UTC = Monday 9am AEST
  workflow_dispatch:
jobs:
  send-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run job digest
        run: python scripts/job_digest.py
        env:
          GMAIL_USER: ${{ secrets.GMAIL_USER }}
          GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
          RECIPIENT_EMAIL: ${{ secrets.RECIPIENT_EMAIL }}
```

### Step 3 — Commit and push

```bash
git add scripts/job_digest.py requirements.txt .github/workflows/job-digest.yml
git commit -m "Add weekly LinkedIn job digest email automation"
git push -u origin <branch>
```

### Step 4 — Merge to default branch

Instruct the user to:
1. Go to GitHub → Pull requests → Create PR for the branch → Merge

### Step 5 — Add GitHub Secrets

Tell the user to go to: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
|---|---|
| `GMAIL_USER` | Gmail address (e.g. you@gmail.com) |
| `GMAIL_APP_PASSWORD` | 16-char app password from Google Account → Security → 2-Step Verification → App Passwords |
| `RECIPIENT_EMAIL` | Destination inbox |

> **Gmail App Password note:** Must have 2-Step Verification enabled first. Generate under Google Account → Security → App Passwords → Mail → Other → Generate. Use the 16-char code (no spaces) as the secret value.

### Step 6 — Test

After secrets are set and branch is merged:
- Go to **Actions** tab → **Weekly Job Digest** → **Run workflow** → **Run workflow**
- Watch the logs — scraping succeeds if it prints "Found N listing(s)" for each keyword
- If `SMTPAuthenticationError` appears, the app password is wrong — regenerate it

## Troubleshooting

| Error | Fix |
|---|---|
| `SMTPAuthenticationError: 534 Application-specific password required` | `GMAIL_APP_PASSWORD` is set to regular password — generate an App Password from Google Account |
| `Found 0 listing(s)` for all searches | LinkedIn may be blocking the scraper — add `time.sleep(3)` between requests or try different User-Agent headers |
| Workflow not showing in Actions tab | Workflow file must be on the **default branch** — merge the PR first |
| `KeyError: GMAIL_USER` | Secret not set in GitHub — check Settings → Secrets |
