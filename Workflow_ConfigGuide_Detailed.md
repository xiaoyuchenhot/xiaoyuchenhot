# Escalation Early Watch — Workflow Configuration Guide

Follow these steps exactly in Copilot Studio to build the workflow.

---

## Step 1: Create the Workflow

1. Open **Copilot Studio** → click **Workflows** in the left sidebar
2. Click **+ New workflow**
3. Name: `Escalation Early Watch`
4. Description: `Analyzes ServiceNow incident file and generates escalation risk report`

---

## Step 2: Configure the Trigger

For V1, use a manual trigger so you can upload the file yourself.

1. In the workflow designer, click the **trigger** block at the top
2. Select: **Manually trigger a flow**
3. Click **+ Add an input** inside the trigger block
4. Select: **File**
5. Set input name: `CasesForReview`
6. This means when you run the workflow, it will ask you to attach a file

Your trigger should now look like:

```
Trigger: Manually trigger a flow
  Input: CasesForReview (File)
```

---

## Step 3: Extract File Content

The AI step needs the file content as text. Add a step to read the Excel file.

### Option A: If using .csv file (simpler)

1. Click **+** below the trigger → **Add an action**
2. Search: **Compose**
3. Name it: `FileContent`
4. Input: Select the dynamic content **CasesForReview** (file content) from the trigger

### Option B: If using .xlsx file (need Excel connector)

1. Click **+** below the trigger → **Add an action**
2. Search: **List rows present in a table** (Excel Online Business connector)
3. Configure:
   - Location: **OneDrive for Business** or **SharePoint**
   - Document Library: (where you'll put the file, or use the trigger file)
   - File: Use dynamic content from trigger — but this connector needs the file in OneDrive/SharePoint

**Alternative for .xlsx** (if the file comes from the manual trigger directly):

1. Click **+** → **Add an action**
2. Search: **Create text with Copilot** (AI Builder)
3. This action can read file attachments directly — skip to Step 4

**Simplest approach for V1:** Export your ServiceNow data as **.csv** instead of .xlsx. CSV is plain text and the AI step can read it directly without conversion.

---

## Step 4: AI Analysis Step (The Core)

This is where the business rules and classification happen.

1. Click **+** below the previous step → **Add an action**
2. Search for one of these (depends on what's available in your tenant):
   - **Create text with Copilot** (AI Builder — recommended)
   - **AI Prompt** (custom prompt)
   - **Generate text with GPT** (AI Builder)
3. Select it and configure:

### Configuration

**Name this action:** `AnalyzeIncidents`

**Prompt field — paste this entire block:**

```
You are a Support Case Escalation Risk Detection Assistant for Lead Customer Advocates. You are objective, evidence-based, and management-action oriented.

Analyze the following ServiceNow incident data. Classify EVERY case and generate a structured risk report.

## DATA TO ANALYZE:
@{triggerBody()?['file']?['contentBytes']}

## INPUT FORMAT
The data is a ServiceNow case report. Columns: Number, Short description, Description, Created, Account, Status, Priority, Updated, Work notes, Updates (ignore), Additional comments, Follow up (ignore), Assigned to.

Rules:
- Each case Number = one unique case. One risk classification per case.
- "Additional comments" = customer-facing conversation. Use for sentiment.
- "Work notes" = internal activity. Use for Support progress.
- Missing fields: state "N/A".

## RISK CLASSIFICATIONS — VERY STRICT

URGENT (expect 1-3% of cases):
Production system CONFIRMED CURRENTLY DOWN and NOT RESTORED.
- Words "down", "outage", "unavailable" MUST appear in PRESENT TENSE in recent comments/work notes.
- If latest comments show system was restored: NOT Urgent.
- If status is "Awaiting Info" and last comment is from weeks ago: NOT Urgent.
- Upgrades, go-lives, performance issues, feature failures: NOT Urgent unless entire Production system is confirmed down right now.

HIGH (expect 10-15% of cases):
Highly likely to be escalated. Requires ALL THREE:
1. Severe impact: critical functionality broken, business process blocked, or production degradation
2. Poor experience: at least ONE of: customer asked for escalation, customer expressed strong frustration, Support no response in 5+ business days, no progress for 10+ days
3. Recency: customer complained or followed up within last 2 weeks
A P1 case alone is NOT High. An old case alone is NOT High.

MEDIUM (expect 25-35% of cases):
Early warning signs. Communication gaps, aging without progress, customer starting to show impatience.

NO RISK (expect 45-55% of cases — LARGEST category):
On track, low impact, progressing normally, or resolved.

## ANALYSIS FACTORS
For each case consider: issue severity, customer sentiment (from Additional Comments), Support responsiveness, troubleshooting progress, communication quality, case age, premature closure, restoration without root cause.

Keywords to watch: down, outage, unavailable, degradation, go-live, upgrade, blocked, escalate, unacceptable, business impact, deadline, frustrated, management.

## OUTPUT FORMAT — GENERATE THIS EXACT STRUCTURE:

ESCALATION RISK DETECTION REPORT
Report Date: [today's date] | Analyzed by: Incident Early Watch Workflow

EXECUTIVE SUMMARY
- Total cases reviewed: [count]
- Urgent: [count] | High: [count] | Medium: [count] | No Risk: [count]
- Accounts requiring immediate attention: [count]
- Top Escalation Drivers (3-4 themes, one sentence each)

IMMEDIATE ACTION REQUIRED — URGENT CASES

For each Urgent case:
[Case Number] — [Account] | Priority: [X] | Status: [X] | Owner: [X]
What is down: [specific system/service]
Evidence: [quote the comment confirming system is currently down]
Recommended Action: [specific action for Lead CA]

If no Urgent cases: "No confirmed active production outages detected."

TOP ACCOUNTS REQUIRING ATTENTION

List ONLY top 15-20 accounts with Urgent or High cases, sorted by risk:
[Account Name] — Risk: [Urgent/High] | [count] cases ([breakdown])
Top issue: [case number — one line]
Why flagged: [specific evidence]
Action: [specific action for Lead CA]

ACCOUNTS ON WATCH — [count] accounts with Medium-risk cases only
- [Account] | [number of cases] | [brief concern]

NO RISK ACCOUNTS — [count] accounts
[Account1], [Account2], [Account3], ...
```

**Important:** Where you see `@{triggerBody()?['file']?['contentBytes']}` — this is the dynamic content reference to the uploaded file. In the Copilot Studio UI:
- Click in the prompt field where you want to insert the file data
- Click the **lightning bolt** icon (dynamic content)
- Select **CasesForReview** from the trigger outputs
- This inserts the file content into the prompt

If the UI uses a different format for dynamic content (like a tag or pill), use that instead of the expression syntax.

**Output variable:** The AI step will produce a text output. Name it or note the default name (e.g., `Text` or `predictionOutput`). You'll reference this in later steps.

---

## Step 5: Save Report to Core Share

### Option A: HTTP connector (direct API call)

1. Click **+** → **Add an action**
2. Search: **HTTP** (premium connector)
3. Configure:

| Field | Value |
|---|---|
| **Method** | `POST` |
| **URI** | `https://<your-core-share-domain>/api/v2/nodes/321813821469491215/children` |
| **Headers** | `Content-Type`: `application/json` |
| | `Authorization`: `Bearer <your-token>` |
| **Body** | See below |

**Body:**
```json
{
  "name": "risk_report_@{formatDateTime(utcNow(), 'yyyy-MM-dd_HHmm')}.txt",
  "type": "content",
  "parent_id": 321813821469491215,
  "file": "@{outputs('AnalyzeIncidents')?['text']}"
}
```

**Note:** Replace `<your-core-share-domain>` with your actual Core Share URL. Replace `<your-token>` with your API token or set up OAuth.

The exact API call depends on your Core Share version. If you already have this working in the Aviator agent (V64), use the same endpoint and auth method.

### Option B: Custom connector (if your team set one up)

1. Click **+** → **Add an action**
2. Search for your custom OpenText connector
3. Select **Upload document** or **Create node**
4. Configure:
   - Parent ID: `321813821469491215`
   - File name: `risk_report_@{formatDateTime(utcNow(), 'yyyy-MM-dd_HHmm')}.txt`
   - Content: Select the AI step output (dynamic content)

### Option C: Save to SharePoint instead (if Core Share not ready)

1. Click **+** → **Add an action**
2. Search: **Create file** (SharePoint)
3. Configure:

| Field | Value |
|---|---|
| **Site Address** | `https://<your-tenant>.sharepoint.com/sites/<your-site>` |
| **Folder Path** | `/Shared Documents/EarlyWatch/Reports` |
| **File Name** | `risk_report_@{formatDateTime(utcNow(), 'yyyy-MM-dd_HHmm')}.txt` |
| **File Content** | Select the AI step output (dynamic content → AnalyzeIncidents → Text) |

---

## Step 6: Post to Teams Channel

1. Click **+** → **Add an action**
2. Search: **Post message in a chat or channel** (Microsoft Teams)
3. Configure:

| Field | Value |
|---|---|
| **Post as** | Flow bot |
| **Post in** | Channel |
| **Team** | Select your team (e.g., "Support Operations") |
| **Channel** | Select channel (e.g., "Escalation Watch") |
| **Message** | See below |

**Message content:**

```
**Escalation Risk Detection Report** — @{formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm')} UTC

@{outputs('AnalyzeIncidents')?['text']}

---
Report saved to Core Share.
```

**If the full report is too long for Teams** (Teams message limit is ~28,000 characters):

Use a shorter message that summarizes and links to the full report:

```
**Escalation Risk Scan Complete** — @{formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm')} UTC

[Paste only the EXECUTIVE SUMMARY section here]

Full report saved to Core Share (EarlyWatch folder).
```

To extract just the summary, you can add a **Compose** step before Teams that uses an expression:
```
first(split(outputs('AnalyzeIncidents')?['text'], 'IMMEDIATE ACTION REQUIRED'))
```
This grabs everything before the detailed cases section.

---

## Step 7: Conditional Email Alert for Urgent Cases

1. Click **+** → **Add an action**
2. Search: **Condition** (Control)
3. Configure the condition:

| Field | Value |
|---|---|
| **Left side** | `outputs('AnalyzeIncidents')?['text']` (dynamic content) |
| **Operator** | `contains` |
| **Right side** | `IMMEDIATE ACTION REQUIRED` |

Then add a second condition row (AND):

| Field | Value |
|---|---|
| **Left side** | `outputs('AnalyzeIncidents')?['text']` |
| **Operator** | `does not contain` |
| **Right side** | `No confirmed active production outages detected` |

### In the YES branch (Urgent cases exist):

1. Click **Add an action** inside the Yes branch
2. Search: **Send an email (V2)** (Office 365 Outlook)
3. Configure:

| Field | Value |
|---|---|
| **To** | `vp@yourcompany.com; director@yourcompany.com` (your escalation recipients) |
| **Subject** | `URGENT: Escalation Risk Detected — @{formatDateTime(utcNow(), 'yyyy-MM-dd')}` |
| **Body** | See below |
| **Importance** | High |

**Email body:**

```html
<h2>Escalation Risk Detection — Urgent Cases Found</h2>
<p>The automated Incident Early Watch scan has detected cases requiring immediate attention.</p>
<hr>
<pre>@{outputs('AnalyzeIncidents')?['text']}</pre>
<hr>
<p>Full report saved to Core Share.</p>
<p><em>This is an automated alert from the Escalation Early Watch workflow.</em></p>
```

### In the NO branch:
Leave empty — no email needed if there are no Urgent cases.

---

## Step 8: Save and Test

1. Click **Save** (top right)
2. Click **Test** (top right)
3. Select **Manually**
4. Click **Run flow**
5. When prompted, upload your ServiceNow .csv/.xlsx file
6. Watch each step execute:
   - Green checkmark = step passed
   - Red X = step failed (click to see error details)

### Test Checklist

| Check | Expected Result |
|---|---|
| AI step produces output | Report with Urgent/High/Medium/No Risk counts |
| Classification distribution | Urgent: 1-3%, High: 10-15%, Medium: 25-35%, No Risk: 45-55% |
| Core Share upload | File appears in folder 321813821469491215 |
| Teams message | Posted to the correct channel |
| Email (if Urgent cases) | Email received by VP/Director addresses |
| Email (if no Urgent) | No email sent |

### Common Test Failures

| Error | Fix |
|---|---|
| AI step: "Input too large" | File has too many cases or columns with very long text. Pre-filter to open cases only, or truncate Work notes to last 500 chars in the export. |
| AI step: Empty or partial output | The model hit its output limit. Add to prompt: "For Medium and No Risk cases, output counts only, not individual lines." |
| Core Share: 401 Unauthorized | Token expired. Regenerate or set up OAuth connection. |
| Core Share: 404 Not Found | Parent ID wrong or folder doesn't exist. Verify parentId. |
| Teams: Message too long | Switch to summary-only Teams message (see Step 6 alternative). |
| Condition step: Always goes to No | Check the expression — the output text might use different casing. Change condition to case-insensitive or check for "Urgent" instead. |

---

## Final Workflow Summary

```
┌─────────────────────────────────────┐
│  TRIGGER: Manually trigger a flow   │
│  Input: CasesForReview (File)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  AI STEP: Create text with Copilot  │
│  Prompt: Business rules +           │
│          classification +           │
│          report format              │
│  Input: File content from trigger   │
│  Output: RiskReport text            │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌──────────────┐ ┌─────────────────┐
│ Save to      │ │ Post to Teams   │
│ Core Share   │ │ Channel         │
│ (HTTP POST)  │ │ (Full or        │
│              │ │  summary)       │
└──────────────┘ └─────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  CONDITION: Urgent cases exist?     │
│                                     │
│  YES → Send email to VP/Director    │
│  NO  → End (no email)              │
└─────────────────────────────────────┘
```

---

## Next Steps After V1 Works

Once the manual trigger workflow is validated:

1. **Add scheduled trigger**: Duplicate the workflow, change trigger to "Recurrence" (daily at 8 AM), and add a "Get file content" step to read from a fixed SharePoint location where someone drops the daily export.

2. **Add SharePoint trigger**: Change trigger to "When a file is created in a folder" — workflow auto-fires when the ServiceNow export lands.

3. **Add ServiceNow connector**: Replace the file upload entirely — use the ServiceNow connector (premium) to query incidents directly, eliminating the manual export step.
