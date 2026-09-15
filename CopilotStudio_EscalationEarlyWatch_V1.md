# Escalation Early Watch — Copilot Studio V1 Build Guide

## Overview

Rebuild the Escalation Early Watch agent in Microsoft Copilot Studio. V1 is file-upload based: a user uploads a ServiceNow incident export (.xlsx or .csv) in Teams chat, and the agent classifies escalation risk using business rules.

This mirrors the Aviator Studio agent (Incident Early Watch v5) but takes advantage of Copilot Studio's native .xlsx support and Teams integration.

---

## Prerequisites

| Requirement | Details |
|---|---|
| **License** | Microsoft 365 Copilot (premium) or Copilot Studio standalone license |
| **Copilot Studio access** | https://copilotstudio.microsoft.com |
| **Teams deployment** | Agent will be published to Microsoft Teams |
| **Test data** | ServiceNow incident export as .xlsx or .csv |

---

## Step-by-Step Build

### Step 1: Create the Agent

1. Go to **Copilot Studio** (https://copilotstudio.microsoft.com)
2. Click **Create** > **New agent**
3. Choose **Skip to configure** (don't use the wizard description — we'll configure manually)
4. Name: `Escalation Early Watch`
5. Description: `Analyzes uploaded ServiceNow incident files and classifies escalation risk using weighted business rules`
6. Icon: Use a warning/shield icon

### Step 2: Configure Agent Instructions

Go to **Settings** > **Generative AI** and paste the following into the **Instructions** field:

```
You are an Escalation Risk Detection Agent for Lead Customer Advocates. You are objective, evidence-based, and management-action oriented.

Your job: When a user uploads a ServiceNow incident file (.xlsx or .csv), analyze EVERY case in it, classify escalation risk, and produce a structured risk report.

You must be strict with classifications. If everything is flagged, nothing is flagged. A useful report highlights the cases that truly need attention.

Always respond in a professional, concise tone. Use the exact output format specified in your instructions.
```

### Step 3: Create the Analysis Topic

This is the core of the agent. Go to **Topics** > **Create** > **Topic** > **From blank**.

**Topic name:** `Analyze Incident File`

**Trigger phrases:**
- Analyze this file
- Run risk scan
- Check these incidents
- Review cases
- Escalation risk analysis
- Here is the incident file
- Upload incident file

**Topic flow:**

1. **Trigger** — User sends a message matching trigger phrases (or uploads a file)
2. **Message node** — Ask: `Please upload your ServiceNow incident export file (.xlsx or .csv). The file should contain columns: Number, Short description, Description, Created, Account, Status, Priority, Updated, Work notes, Additional comments, Assigned to.`
3. **Question node** — Variable type: **File** (accept .xlsx, .csv). Store in variable `IncidentFile`.
4. **Generative Answers node** — This is where the AI processes the file. Connect the uploaded file as context and use the prompt below.

### Step 4: The Analysis Prompt (Generative Answers Node)

In the Generative Answers node, set **Data source** to the uploaded file variable, and use this as the **custom prompt / instructions**:

```
Analyze the uploaded file to perform escalation risk detection.

## Input Format
The file contains a ServiceNow case report. Expected columns:
- Number: Unique case identifier
- Short description: Brief issue summary
- Description: Detailed issue description
- Created: Case creation date
- Account: Customer/company name
- Status: Case status (Open, Awaiting Info, Resolved, etc.)
- Priority: 1-Critical, 2-High, 3-Medium, 4-Low
- Updated: Last update timestamp
- Work notes: Internal support activity (use for progress assessment)
- Additional comments: Customer-facing conversation (use for sentiment)
- Assigned to: Current case owner

Rules:
- Each case Number = one unique case. One risk classification per case.
- "Additional comments" = customer-facing conversation. Use for sentiment analysis.
- "Work notes" = internal activity. Use for Support responsiveness/progress.
- Missing or empty fields: state "N/A".
- Ignore columns: Updates, Follow up.

## Risk Classification Business Rules — STRICT

### URGENT (expect 1-3% of cases)
ONLY for cases where a customer's Production system is CONFIRMED CURRENTLY DOWN and NOT YET RESTORED.
Required evidence:
- The words "down", "outage", "unavailable", or "not working" MUST appear in PRESENT TENSE in recent comments or work notes
- If latest comments show the system was restored → NOT Urgent
- If status is "Awaiting Info" and last comment is from weeks ago → outage likely resolved → NOT Urgent

NOT Urgent (even if P1):
- Upgrade issues, go-live planning, performance degradation, feature failures
- Unless the ENTIRE production system is confirmed down RIGHT NOW

### HIGH (expect 10-20% of cases)
Cases highly likely to be escalated by the customer. Must meet ALL THREE:
1. **Severe impact** — critical functionality broken, significant business process blocked, or production degradation
2. **Poor experience** — at least ONE of:
   - Customer explicitly asked for escalation
   - Customer expressed strong frustration or anger
   - Support has not responded in 5+ business days
   - No meaningful progress for 10+ days
3. **Recency** — customer has complained or followed up within last 2 weeks

A P1 case alone is NOT High. An old case alone is NOT High.

### MEDIUM (expect 25-35% of cases)
Early warning signs but not yet at escalation risk:
- Communication gaps developing
- Case aging without clear progress
- Customer starting to show impatience
- Awaiting vendor response with no timeline

### NO RISK (expect 45-55% of cases — LARGEST category)
- On track, low impact, progressing normally, or resolved
- Customer satisfied with communication
- Active troubleshooting with clear next steps

## Analysis Factors
For each case evaluate:
1. Issue severity and business impact
2. Customer sentiment (from Additional Comments — look for frustration, anger, escalation requests)
3. Support responsiveness (from Work notes — gaps in activity?)
4. Troubleshooting progress (is it moving forward or stuck?)
5. Communication quality (is the customer being kept informed?)
6. Case age in context (old isn't bad if progressing; new can be urgent if production down)
7. Premature closure risk (resolved without root cause?)

Escalation keywords to watch: down, outage, unavailable, degradation, go-live, upgrade, blocked, escalate, unacceptable, business impact, deadline, frustrated, management, executive, legal

## Output Format — EXECUTIVE BRIEF

**ESCALATION RISK DETECTION REPORT**
Report Date: [today's date] | Analyzed by: Escalation Early Watch Agent

---

**EXECUTIVE SUMMARY**
- Total cases reviewed: [count — must match total cases in file]
- Urgent: [count] | High: [count] | Medium: [count] | No Risk: [count]
- Verification total: [sum of all four — must equal total cases reviewed]
- Accounts requiring immediate attention: [count]

**Top Escalation Drivers** (3-4 themes, one sentence each)

---

**URGENT CASES — IMMEDIATE ACTION REQUIRED**

For each Urgent case:

**[Case Number] — [Account]**
Priority: [X] | Status: [X] | Owner: [X] | Days Open: [X]
System Down: [what is confirmed down and evidence]
Risk Drivers: [specific evidence from comments/work notes]
Customer Sentiment: [one line summary from Additional Comments]
Recommended Action: [specific, immediate action for Lead CA]

If no Urgent cases: "No confirmed active production outages detected."

---

**HIGH RISK CASES — ESCALATION LIKELY**

For each High case:

**[Case Number] — [Account]**
Priority: [X] | Status: [X] | Owner: [X] | Days Open: [X]
Risk Drivers: [specific evidence — not generic phrases]
Customer Sentiment: [one line]
Recommended Action: [specific action]

---

**MEDIUM RISK CASES — MONITOR**

One line per case:
- [Case Number] | [Account] | [Priority] | [Days Open] | [Brief concern]

---

**NO RISK CASES**

One line per case:
- [Case Number] | [Account] | [Priority] | [Status/reason: resolved/progressing/low impact]

---

**ACCOUNT RISK SUMMARY**

Group flagged cases by account. List accounts with 2+ Urgent or High cases:

**[Account Name]** — [count] flagged cases
- [Case Number]: [risk level] — [one line summary]
- [Case Number]: [risk level] — [one line summary]
Overall Assessment: [one sentence]
Recommended Account Action: [specific action for Lead CA]
```

### Step 5: Configure Knowledge Source (Optional Enhancement)

If you want the agent to reference OpenText product knowledge when analyzing cases:

1. Go to **Knowledge** > **Add knowledge**
2. Add relevant sources:
   - SharePoint site with OpenText product documentation
   - Or upload a reference file with common product issues and known resolutions
3. This helps the agent provide more specific recommended actions

For V1, this is optional — the agent works with just the uploaded file and business rules.

### Step 6: Publish to Teams

1. Go to **Channels** > **Microsoft Teams**
2. Click **Turn on Teams**
3. Click **Open in Teams** to test
4. Users can find the agent in Teams by searching for "Escalation Early Watch"

### Step 7: Test the Agent

1. Open the agent in Teams
2. Type: "Analyze this file" or "Run risk scan"
3. Upload your ServiceNow incident export (.xlsx or .csv)
4. Verify the output matches the expected format and classification distribution

**Expected distribution for ~250 cases:**
- Urgent: 2-8 cases (1-3%)
- High: 25-50 cases (10-20%)
- Medium: 60-90 cases (25-35%)
- No Risk: 110-140 cases (45-55%)

If the agent classifies too many as Urgent or High, the instructions need tightening. If too many are No Risk, loosen the Medium criteria.

---

## Known Limitations and Workarounds

| Limitation | Impact | Workaround |
|---|---|---|
| **File size limit** | Copilot Studio has a file upload size limit (typically 10MB) | Pre-filter to open/active cases only. 250 cases in .xlsx is typically 200-500KB — well within limits. |
| **Token/context window** | Very large files with long work notes may exceed the model's context window | If the file has 500+ cases, split into batches of 250. Or truncate Work notes/Additional comments columns to last 500 characters each before uploading. |
| **No .xlsx in Aviator** | This was a major pain point — had to convert to .txt | Copilot Studio handles .xlsx natively. No workaround needed. |
| **Output truncation** | For 250+ cases, the full report may be long | The agent may need to split output across multiple messages. Consider asking for "summary only" mode for large files. |
| **No persistent storage** | V1 doesn't save reports anywhere | Copy/paste from Teams chat. V2 can add Power Automate to save reports to SharePoint or Core Share. |

---

## File Preparation

### What to Export from ServiceNow

Run a ServiceNow report or list export with these columns:

| Column | ServiceNow Field | Required |
|---|---|---|
| Number | number | Yes |
| Short description | short_description | Yes |
| Description | description | Yes |
| Created | sys_created_on | Yes |
| Account | account.name | Yes |
| Status | state (display value) | Yes |
| Priority | priority (display value) | Yes |
| Updated | sys_updated_on | Yes |
| Work notes | work_notes | Yes |
| Additional comments | comments | Yes |
| Assigned to | assigned_to.name | Yes |

### Filters to Apply Before Export
- **Status**: NOT IN (Resolved, Closed, Cancelled) — only open/active cases
- **Priority**: 1-Critical OR 2-High (or include 3-Medium if desired)
- **Created**: Last 90 days (adjust as needed)

This keeps the file to ~50-250 rows, well within processing limits.

---

## V1 vs Aviator Studio Comparison

| Aspect | Aviator Studio | Copilot Studio V1 |
|---|---|---|
| File format | .txt only (had to convert from .xlsx) | .xlsx and .csv natively |
| Deployment | REST API or Share button | Teams chat (conversational) |
| User interaction | Upload file, wait for batch result | Chat-based — can ask follow-up questions |
| Follow-up queries | Not supported — new run needed | Ask "tell me more about case CS0625042" or "which accounts have go-live coming up?" |
| Batch splitting | Needed 13 DOCX batches for 258 cases | Single file upload |
| Knowledge base | AvKnowledgeRetrieval + CSM Helix KB | SharePoint / uploaded docs |
| Cost | OpenText Aviator license | Microsoft 365 Copilot / Copilot Studio license |
| Integration | Content Server, Core Share | Teams, SharePoint, Power Automate |

---

## V2 Roadmap (After V1 Is Working)

Once V1 is validated, the next iteration can add:

1. **Automated trigger**: Power Automate flow watches a SharePoint folder. When a new incident file lands, it triggers the agent automatically.
2. **Scheduled runs**: Power Automate runs the ServiceNow export on a schedule (every 10 min or daily) and feeds it to the agent.
3. **Email alerts**: Power Automate sends email/Teams notifications for Critical cases.
4. **Dataverse storage**: Store risk scores in Dataverse for trend analysis over time.
5. **Dashboard**: Power BI dashboard reading from Dataverse showing risk trends per account.
6. **Core Share integration**: Use a custom connector to save reports back to OpenText Core Share if the organization requires it.
