# Escalation Early Watch — Copilot Studio Agent Configuration (Step-by-Step)

You already have the Incident Early Watch agent (V64). This guide shows how to update it with combined task instructions, or create a new one from scratch.

---

## Step 1: Open Your Agent

1. Go to **Copilot Studio** → click **Agents** in the left sidebar
2. Click **Incident Early Watch agent** (V64)
3. You'll see the Agent definition tab with Description and Task instructions

---

## Step 2: Update the Description

In the **Description** field, paste:

```
Support Case Escalation Risk Detection Assistant. Analyzes uploaded ServiceNow incident files (.xlsx or .csv) to classify escalation risk (Urgent, High, Medium, No Risk) using strict business rules. Generates an executive risk report focused on accounts and cases requiring immediate attention. Saves reports to Core Share automatically.
```

---

## Step 3: Remove Existing Tasks

1. Click **Quick Scan - Classify All Cases** → scroll to bottom → click **Remove task**
2. Click **Deep Analysis Report** → scroll to bottom → click **Remove task**

You should now have zero tasks.

---

## Step 4: Add the Combined Task

1. Click **+ Add new task**
2. Set the task name: `Escalation Risk Analysis`
3. In the Task instructions field, paste EVERYTHING below:

```
Analyze the uploaded file /CasesForReview to perform escalation risk detection.

You are a Support Case Escalation Risk Detection Assistant for Lead Customer Advocates. You are objective, evidence-based, and management-action oriented.

Scan ALL cases in the file, classify each one, then generate an executive report focused on cases that need immediate attention. Your report must be selective — if everything is flagged, nothing is flagged.

## Input

The file contains a ServiceNow case report. Columns: Number, Short description, Description, Created, Account, Status, Priority, Updated, Work notes, Updates (ignore), Additional comments, Follow up (ignore), Assigned to.

Rules:
- Each case Number is one unique case. One risk result per case.
- "Additional comments" = customer-facing conversation. Use for sentiment.
- "Work notes" = internal activity. Use for Support progress.
- Missing fields: state "N/A".

## Risk Classifications — VERY STRICT

**Urgent** — ONLY for cases where a customer's Production system is CONFIRMED CURRENTLY DOWN and NOT YET RESTORED as of the latest comments/work notes.
- The words "down", "outage", or "unavailable" MUST appear in PRESENT TENSE in recent comments (not past tense, not historical).
- If the latest comments show the system was restored, it is NOT Urgent.
- If status is "Awaiting Info" and the last comment is from weeks ago, the outage is likely resolved — NOT Urgent.
- Cases about upgrades, go-lives, performance issues, or feature failures are NOT Urgent unless the entire Production system is confirmed down right now.
- EXPECT: 1-3% of cases (2-8 cases out of 250).

**High** — Cases that are highly likely to be escalated by the customer. Must meet ALL THREE criteria:
1. Severe impact — critical functionality broken, significant business process blocked, or production degradation
2. Poor experience — at least ONE of: customer explicitly asked for escalation, customer expressed strong frustration/anger, Support has not responded in 5+ business days, no meaningful progress for 10+ days
3. Recency — customer has complained or followed up within the last 2 weeks
- A P1 case alone is NOT High. A post-upgrade issue alone is NOT High. An old case alone is NOT High.
- EXPECT: 10-15% of cases (25-40 cases out of 250).

**Medium** — Cases showing early warning signs but not yet at escalation risk.
- Communication gaps, aging without progress, customer starting to show impatience
- EXPECT: 25-35% of cases.

**No Risk** — On track, low impact, progressing normally, or resolved.
- EXPECT: 45-55% of cases. This should be the LARGEST category.

## Analysis Factors

For each case consider: issue severity, customer sentiment (from Additional Comments), Support responsiveness, troubleshooting progress, communication quality, case age, premature closure, restoration without root cause.

Keywords to watch: down, outage, unavailable, degradation, go-live, upgrade, blocked, escalate, unacceptable, business impact, deadline, frustrated, management.

## Output Format — SINGLE STRUCTURED REPORT

**ESCALATION RISK DETECTION REPORT**
Report Date: [today's date] | Analyzed by: Incident Early Watch Agent

**EXECUTIVE SUMMARY**
- Total cases reviewed: [count — must match total in file]
- Urgent: [count] | High: [count] | Medium: [count] | No Risk: [count]
- Accounts requiring immediate attention: [count] (should be 10-20, not 90+)
- Top Escalation Drivers (3-4 themes, one sentence each)

**IMMEDIATE ACTION REQUIRED — URGENT CASES**

For each Urgent case:
**[Case Number] — [Account]** | Priority: [X] | Status: [X] | Owner: [X]
What is down: [specific system/service]
Evidence: [quote the specific comment/note confirming system is currently down]
Recommended Action: [specific, immediate action for Lead CA]

If no Urgent cases: state "No confirmed active production outages detected."

**TOP ACCOUNTS REQUIRING ATTENTION**

List ONLY the top 15-20 accounts with Urgent or High cases, sorted by risk. For each:
**[Account Name]** — Risk: [Urgent/High] | [count] cases ([breakdown])
Top issue: [case number — one line]
Why flagged: [specific evidence, not generic "severe impact"]
Action: [specific action for Lead CA]

**ACCOUNTS ON WATCH** — [count] accounts with Medium-risk cases only
One line each:
- [Account] | [number of cases] | [brief concern]

**NO RISK ACCOUNTS** — [count] accounts
[Account1], [Account2], [Account3], ...

## Save Report

After generating the report, use the "Upload to Core Share" tool to save it:
- parentId: 321813821469491215
- file: the full report text
```

---

## Step 5: Configure the File Input

You need to make sure the agent knows what `/CasesForReview` is.

1. Look for the warning banner at the top: `Input "CasesForReview" is not mapped in agent instru...`
2. Click on it, or go to **Advanced settings** tab
3. Find the **Inputs** or **Knowledge** section
4. Map `CasesForReview` as a **File upload** input
5. This tells the agent: when the user uploads a file, treat it as `/CasesForReview`

If the mapping is done through the agent's **Knowledge** settings:
- Go to **Knowledge** → **Add knowledge source**
- Select **File upload** as the source type
- Name it `CasesForReview`

If the mapping is done through **Advanced settings** → **Inputs**:
- Add an input named `CasesForReview`
- Type: File
- This maps the uploaded file to the /CasesForReview reference in the task instructions

---

## Step 6: Verify the Core Share Tool

Your V64 already had the "Upload to Core Share" tool configured. Verify it's still connected:

1. Go to **Actions** or **Tools** (may be under Advanced settings)
2. Confirm the "Upload to Core Share" action exists with:
   - API endpoint pointing to your Core Share instance
   - Authentication (Bearer token or OAuth) is valid
   - Default parentId: `321813821469491215`

If you need to re-add it:
1. Go to **Actions** → **+ Add an action**
2. Search for your Core Share custom connector, OR
3. Add a custom HTTP action:
   - Name: `Upload to Core Share`
   - Method: POST
   - URL: `https://<your-core-share-domain>/api/v2/nodes/321813821469491215/children`
   - Headers: Authorization with your token
   - Body: file name + content from the report

---

## Step 7: Add Email Action for Urgent Cases (Optional)

If you want the agent to email VP/Director when Urgent cases are found:

1. Go to **Actions** → **+ Add an action**
2. Search for **Outlook** or **Send email** (Office 365 connector)
3. Add the **Send an email (V2)** action
4. Configure the connection (sign in with your work account)

Then update the task instructions — add this section at the very end, after the "Save Report" section:

```
## Email Alert

If any URGENT cases were found in the report:
- Use the "Send Email" action
- To: [replace with your VP/Director email addresses]
- Subject: URGENT: Escalation Risk Detected — [today's date]
- Body: Copy the EXECUTIVE SUMMARY and the IMMEDIATE ACTION REQUIRED — URGENT CASES sections
- Importance: High

If NO urgent cases were found, do NOT send an email.
```

---

## Step 8: Add Teams Channel Posting (Optional)

If you want the agent to post a summary to a shared Teams channel:

1. Go to **Actions** → **+ Add an action**
2. Search for **Microsoft Teams** → **Post message in a chat or channel**
3. Configure: select your Team and Channel

Then add this to the end of the task instructions:

```
## Teams Notification

After generating the report, use the "Post to Teams" action:
- Channel: [your team/channel name]
- Message: Post the EXECUTIVE SUMMARY section only (not the full report)
- If Urgent cases exist, prefix the message with "URGENT ATTENTION REQUIRED"
```

---

## Step 9: Deploy to Teams

1. Go to the **Channels** tab (or Settings → Channels)
2. Click **Microsoft Teams**
3. Toggle **Teams channel** to ON
4. Click **Publish** (top-right button)
5. Wait for deployment to complete

Users can now find the agent in Teams by:
- Searching for "Incident Early Watch" in the Teams search bar
- Or it appears in the Teams app sidebar if pinned

---

## Step 10: Test

### Test in Copilot Studio (Quick Test)

1. Click the **Test** button (top-right area, or the play icon)
2. In the test chat panel, type: "Analyze this file" or "Run risk scan"
3. Upload your ServiceNow .csv or .xlsx file
4. Verify:
   - [ ] All cases are classified
   - [ ] Distribution: Urgent 1-3%, High 10-15%, Medium 25-35%, No Risk 45-55%
   - [ ] Report follows the exact output format
   - [ ] Report saved to Core Share (check folder 321813821469491215)
   - [ ] Email sent only if Urgent cases found (if email action added)

### Test in Teams

1. Open Microsoft Teams
2. Search for "Incident Early Watch" in the search bar
3. Start a chat with the agent
4. Type: "Analyze this file" and upload the file
5. Verify same checklist as above
6. Try a follow-up: "Tell me more about [case number]" or "Which accounts have the most critical cases?"

### Test Checklist

| Test | Expected Result |
|---|---|
| Upload .csv file | Agent processes and returns report |
| Upload .xlsx file | Agent processes and returns report |
| Classification counts | Urgent: 1-3%, High: 10-15%, Medium: 25-35%, No Risk: 45-55% |
| Core Share upload | Report appears in the correct folder |
| Email (if Urgent found) | Email received with Urgent case details |
| Email (if no Urgent) | No email sent |
| Teams channel post | Summary appears in shared channel |
| Follow-up question | Agent answers about specific cases |
| Large file (250+ cases) | Report completes without truncation |

---

## Troubleshooting

| Issue | Fix |
|---|---|
| "CasesForReview" not mapped warning | Go to Advanced settings → map the file input (Step 5) |
| Agent can't read .xlsx | Try .csv instead. If .xlsx is needed, check if the agent has file parsing enabled in Advanced settings. |
| Report is truncated (large files) | Add to instructions: "For Medium and No Risk cases, output counts only, not individual case lines." |
| Core Share upload fails | Check token expiration. Regenerate Bearer token. Verify parentId exists. |
| Email action not available | Check if Outlook connector is allowed by DLP policy. If blocked, skip email — use Teams channel post instead. |
| Too many Urgent cases | Review the Urgent criteria — may need to add: "Evidence must be from the last 48 hours" |
| Too few High cases | Loosen criteria: change "ALL THREE" to "at least TWO of three" |
| Agent responds but doesn't run task | Make sure trigger phrases match. Try typing exactly: "Analyze this file" |

---

## Summary: What You Changed

| Before (V64 — Two Tasks) | After (Combined — Single Task) |
|---|---|
| Task 1: Quick Scan (classify, one-liners) | Single task: Classify + Full Report |
| Task 2: Deep Analysis (executive report) | — merged into single task — |
| Two-pass processing | One-pass processing |
| Core Share upload in Task 2 only | Core Share upload in single task |
| No email alerts | Email action for Urgent cases (optional) |
| No Teams channel posting | Teams channel summary (optional) |
