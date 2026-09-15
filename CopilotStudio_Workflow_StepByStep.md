# Escalation Early Watch — Copilot Studio Workflow Build (Step-by-Step)

## What You Are Building

A Copilot Studio Workflow that:
1. Gets triggered (manually from Teams, or when a file arrives)
2. Reads the uploaded ServiceNow incident file (.xlsx or .csv)
3. Uses an AI step to classify all cases using your business rules
4. Generates the executive risk report
5. Saves the report to Core Share
6. Posts a summary to a Teams channel and/or sends email alerts for critical cases

---

## Step 1: Create the Workflow

1. Go to **Copilot Studio** (https://copilotstudio.microsoft.com)
2. Click **Workflows** in the left sidebar
3. Click **+ New workflow**
4. You will see the workflow designer with a trigger selection

### Choose Your Trigger

For V1, pick one of these:

**Option A: Manual trigger from Teams (simplest for V1)**
- Select: **Manually trigger a flow**
- Add input: **File** (name it `CasesForReview`)
- This creates a button in Teams where the user clicks, attaches the file, and the workflow runs

**Option B: When a file is created in SharePoint**
- Select: **When a file is created (properties only)** — SharePoint connector
- Site Address: [your SharePoint site]
- Library Name: e.g., `Incident Reports` or a specific folder
- When someone drops an .xlsx into that folder, the workflow fires automatically

**Option C: Scheduled (for automated daily runs)**
- Select: **Recurrence**
- Set to: Every day at 8:00 AM (or every 10 minutes like the Aviator design)
- You'll add a "Get file content" step to read from a fixed location

For this guide, we'll use **Option A** (manual trigger) since you said you're uploading in Teams.

---

## Step 2: Add the File Content Step

After the trigger, add a step to get the file content ready for AI processing.

1. Click **+ Add an action** after the trigger
2. If using manual trigger: The file is already in the trigger output as `triggerBody()?['file']`
3. If using SharePoint trigger: Add **Get file content** (SharePoint) with the file identifier from the trigger

---

## Step 3: Add the AI Step — Classify and Analyze

This is the core step. Copilot Studio Workflows support **AI Builder** actions and **Copilot** actions.

### Option 1: Use "Create text with Copilot" action (Recommended for V1)

1. Click **+ Add an action**
2. Search for **Create text with GPT** or **Create text with Copilot** (under AI Builder)
3. Configure:

**Prompt / Instructions:**

```
You are a Support Case Escalation Risk Detection Assistant. Analyze the following ServiceNow incident data and classify every case.

## Input Data
The data contains a ServiceNow case report with columns: Number, Short description, Description, Created, Account, Status, Priority, Updated, Work notes, Updates (ignore), Additional comments, Follow up (ignore), Assigned to.

Rules:
- Each case Number = one unique case. One risk classification per case.
- "Additional comments" = customer-facing conversation. Use for sentiment.
- "Work notes" = internal activity. Use for Support progress.
- Missing fields: state "N/A".

## Risk Classifications — VERY STRICT

**Urgent** — Production system CONFIRMED CURRENTLY DOWN and NOT RESTORED.
- Must have present-tense evidence: "down", "outage", "unavailable" in recent comments/work notes.
- If latest comments show restored → NOT Urgent.
- If "Awaiting Info" with last comment weeks ago → NOT Urgent.
- Upgrades, go-lives, performance issues → NOT Urgent unless entire Production confirmed down now.
- EXPECT: 1-3% of cases.

**High** — Highly likely to be escalated. Requires ALL THREE:
1. Severe impact — critical functionality broken, business process blocked, production degradation
2. Poor experience — at least ONE of: customer asked for escalation, customer expressed strong frustration, Support no response 5+ business days, no progress 10+ days
3. Recency — customer complained/followed up within last 2 weeks
- P1 alone is NOT High. Old case alone is NOT High.
- EXPECT: 10-15%.

**Medium** — Early warning signs. Communication gaps, aging without progress, customer impatience.
- EXPECT: 25-35%.

**No Risk** — On track, low impact, progressing, or resolved. LARGEST category.
- EXPECT: 45-55%.

## Analysis Factors
Consider: issue severity, customer sentiment (from Additional Comments), Support responsiveness, troubleshooting progress, communication quality, case age, premature closure, restoration without root cause.

Keywords: down, outage, unavailable, degradation, go-live, upgrade, blocked, escalate, unacceptable, business impact, deadline, frustrated, management.

## Output — SINGLE STRUCTURED REPORT

**ESCALATION RISK DETECTION REPORT**
Report Date: [today's date] | Analyzed by: Incident Early Watch Workflow

**EXECUTIVE SUMMARY**
- Total cases reviewed: [count — must match total in file]
- Urgent: [count] | High: [count] | Medium: [count] | No Risk: [count]
- Accounts requiring immediate attention: [count] (should be 10-20, not 90+)
- Top Escalation Drivers (3-4 themes, one sentence each)

**IMMEDIATE ACTION REQUIRED — URGENT CASES**

For each Urgent case:
**[Case Number] — [Account]** | Priority: [X] | Status: [X] | Owner: [X]
What is down: [specific system/service]
Evidence: [quote the comment confirming system is currently down]
Recommended Action: [specific action for Lead CA]

If no Urgent cases: "No confirmed active production outages detected."

**TOP ACCOUNTS REQUIRING ATTENTION**

List ONLY top 15-20 accounts with Urgent or High cases, sorted by risk:
**[Account Name]** — Risk: [Urgent/High] | [count] cases ([breakdown])
Top issue: [case number — one line]
Why flagged: [specific evidence]
Action: [specific action for Lead CA]

**ACCOUNTS ON WATCH** — [count] accounts with Medium-risk cases only
- [Account] | [number of cases] | [brief concern]

**NO RISK ACCOUNTS** — [count] accounts
[Account1], [Account2], [Account3], ...
```

**Data input:** Map the file content from Step 2 into the prompt's data field.

4. Store the output in a variable: `RiskReport`

### Option 2: Use "AI Prompt" custom action

If "Create text with Copilot" doesn't support file input directly:

1. Add a **Compose** action to extract the file content as text
2. Add **Create text with Copilot** with the text content embedded in the prompt
3. Use dynamic content to insert the file text: `@{body('Compose')}`

---

## Step 4: Save Report to Core Share

After the AI step generates the report, save it to OpenText Core Share.

### Option A: HTTP action (if you have the Core Share API endpoint)

1. Click **+ Add an action**
2. Search for **HTTP** (premium connector)
3. Configure:

- **Method:** POST
- **URI:** `https://<your-core-share-instance>/api/v2/nodes/<parentId>/children`
  - Replace `<parentId>` with your folder ID: `321813821469491215`
- **Headers:**
  ```
  Content-Type: multipart/form-data
  Authorization: Bearer <your-token or use OAuth connection>
  ```
- **Body:** The report text from the AI step variable `RiskReport`

### Option B: Custom connector (better for production)

If your team has set up an OpenText Core Share custom connector in Power Platform:

1. Click **+ Add an action**
2. Search for your custom connector name (e.g., "Core Share" or "OpenText")
3. Select the **Upload file** action
4. Configure:
   - Parent ID: `321813821469491215`
   - File name: `risk_report_@{formatDateTime(utcNow(), 'yyyy-MM-dd_HHmm')}.txt`
   - File content: `@{outputs('Create_text_with_Copilot')?['text']}`

### Option C: Save to SharePoint first (fallback if Core Share connector not ready)

1. Click **+ Add an action**
2. Search for **Create file** (SharePoint)
3. Configure:
   - Site Address: [your SharePoint site]
   - Folder Path: `/EarlyWatch/Reports/`
   - File Name: `risk_report_@{formatDateTime(utcNow(), 'yyyy-MM-dd_HHmm')}.txt`
   - File Content: `@{outputs('Create_text_with_Copilot')?['text']}`

---

## Step 5: Post Summary to Teams Channel

1. Click **+ Add an action**
2. Search for **Post message in a chat or channel** (Microsoft Teams)
3. Configure:
   - Post as: Flow bot
   - Post in: Channel
   - Team: [your team]
   - Channel: [e.g., "Escalation Watch" or "Support Leads"]
   - Message: Use the AI output variable

**Message template:**

```
🔍 **Escalation Risk Detection Report** — @{formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm')}

@{outputs('Create_text_with_Copilot')?['text']}

---
_Report saved to Core Share. Full report available in the EarlyWatch folder._
```

**If the full report is too long for a Teams message**, post a summary instead:

```
🔍 **Escalation Risk Scan Complete** — @{formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm')}

Cases Reviewed: [count]
⚠️ Urgent: [count] | 🔴 High: [count] | 🟡 Medium: [count] | ✅ No Risk: [count]

Top accounts requiring attention:
[list from AI output]

📄 Full report saved to Core Share.
```

---

## Step 6: (Optional) Send Email for Urgent Cases

Add a condition to send email only when Urgent cases are detected.

1. Click **+ Add an action**
2. Add a **Condition** step:
   - Condition: `contains(outputs('Create_text_with_Copilot')?['text'], 'IMMEDIATE ACTION REQUIRED')`
   - AND: `not(contains(outputs('Create_text_with_Copilot')?['text'], 'No confirmed active production outages'))`

3. In the **Yes** branch, add **Send an email (V2)** (Office 365 Outlook):
   - To: VP/Director email addresses
   - Subject: `⚠️ URGENT: Escalation Risk Detected — @{formatDateTime(utcNow(), 'yyyy-MM-dd')}`
   - Body: Extract the URGENT CASES section from the report

4. The **No** branch: Do nothing (no email for non-urgent runs)

---

## Step 7: Save and Test

1. Click **Save** in the workflow designer
2. Click **Test** in the top-right corner
3. Select **Manually**
4. Upload your ServiceNow incident file (.xlsx)
5. Watch the flow run step by step
6. Verify:
   - AI classification matches expected distribution
   - Report is saved to Core Share (or SharePoint)
   - Teams message appears in the channel
   - Email fires only for Urgent cases

---

## Complete Workflow Diagram

```
[Trigger: Manual / SharePoint / Schedule]
         │
         ▼
[Get File Content]
         │
         ▼
[AI Step: Create text with Copilot]
 - Input: file content
 - Prompt: business rules + classification + report format
 - Output: RiskReport variable
         │
         ├──────────────────────────────┐
         ▼                              ▼
[Save to Core Share]          [Post to Teams Channel]
 - parentId: 32181...          - Summary or full report
 - filename: risk_report_      - Channel: Support Leads
   YYYY-MM-DD_HHMM.txt
         │
         ▼
[Condition: Urgent cases exist?]
    Yes ──▶ [Send Email Alert to VP/Director]
    No  ──▶ [End]
```

---

## Workflow vs Your Existing Agent

You don't have to choose one — they serve different purposes:

| Use Case | Use Agent (V64) | Use Workflow |
|---|---|---|
| Ad-hoc analysis: "check this file for me" | ✅ Chat in Teams | |
| Follow-up questions: "tell me more about case X" | ✅ Conversational | |
| Daily automated scan at 8 AM | | ✅ Scheduled trigger |
| Auto-process when file lands in SharePoint | | ✅ Event trigger |
| Email VP when Urgent cases found | | ✅ Conditional action |
| Save every report to Core Share automatically | | ✅ Built into flow |
| Quick spot-check by a support lead | ✅ Chat in Teams | |

**Recommendation:** Keep the Agent for interactive use. Add the Workflow for automation. They use the same business rules/prompt.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| AI step can't read .xlsx content | Add a "Convert file" step before the AI step to convert .xlsx to CSV/text. Or use "List rows present in a table" (Excel Online) to extract data as JSON first. |
| Report is truncated | Reduce Medium/No Risk detail: change output to counts-only for those categories. |
| Core Share upload fails (401/403) | Check OAuth token or API key. May need a custom connector with proper auth. |
| Teams message too long | Post summary only to Teams; save full report to Core Share/SharePoint. |
| AI classification too many Urgent | Tighten the Urgent criteria: add "MUST have evidence from the last 48 hours" |
| Workflow timeout (5 min limit) | For 250+ cases, the AI step may take time. Consider splitting into batches or using an async pattern. |
