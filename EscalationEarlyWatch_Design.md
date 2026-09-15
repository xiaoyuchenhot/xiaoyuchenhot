# Escalation Early Watch Agent — Business Requirements & Design

## 1. Business Context

**Owner**: Eric Chen (ceric), Mission Control Center / OpenText
**Purpose**: Proactively detect support case escalation risks before customers escalate, enabling Lead Customer Advocates (Lead CAs) to take preventive action.
**Users**: Lead Customer Advocates, Support Managers

## 2. Problem Statement

Lead CAs manage 250+ active ServiceNow support cases. Manually reviewing each case for escalation risk is time-consuming and error-prone. Cases slip through the cracks, leading to reactive escalation handling instead of proactive prevention.

## 3. Solution Overview

An AI agent that:
1. Ingests a ServiceNow case export file (250+ cases)
2. Classifies each case into risk levels (Urgent, High, Medium, No Risk)
3. Generates an executive-ready escalation risk report
4. Uploads the report to a shared folder for team access

## 4. Input Specification

**Source**: ServiceNow case export file (CSV/Excel)
**Input name**: `CasesForReview`
**Expected volume**: 200-300 cases per run

**Columns used**:
| Column | Purpose |
|--------|---------|
| Number | Unique case identifier |
| Short description | Issue summary |
| Description | Detailed issue description |
| Created | Case creation date |
| Account | Customer account name |
| Status | Current case status |
| Priority | P1/P2/P3/P4 |
| Updated | Last update timestamp |
| Work notes | Internal support activity (progress tracking) |
| Additional comments | Customer-facing conversation (sentiment analysis) |
| Assigned to | Current case owner |

**Columns ignored**: Updates, Follow up

## 5. Risk Classification Rules

### Urgent (expect 1-3% of cases, i.e. 2-8 out of 250)
Production system CONFIRMED CURRENTLY DOWN and NOT YET RESTORED.
- Words "down", "outage", or "unavailable" MUST appear in PRESENT TENSE in recent comments
- If latest comments show system was restored → NOT Urgent
- If status is "Awaiting Info" and last comment is weeks old → NOT Urgent
- Upgrades, go-lives, performance issues, feature failures → NOT Urgent unless entire production is confirmed down now

### High (expect 10-15% of cases, i.e. 25-40 out of 250)
Must meet ALL THREE criteria:
1. **Severe impact** — critical functionality broken, significant business process blocked, or production degradation
2. **Poor experience** — at least ONE of: customer asked for escalation, customer expressed strong frustration, Support not responded in 5+ business days, no meaningful progress for 10+ days
3. **Recency** — customer complained or followed up within last 2 weeks

A P1 case alone is NOT High. A post-upgrade issue alone is NOT High. An old case alone is NOT High.

### Medium (expect 25-35% of cases)
Early warning signs but not yet at escalation risk:
- Communication gaps
- Aging without progress
- Customer starting to show impatience

### No Risk (expect 45-55% of cases — LARGEST category)
- On track, low impact, progressing normally, or resolved

## 6. Analysis Factors

For each case evaluate:
- Issue severity and business impact
- Customer sentiment (from Additional Comments)
- Support responsiveness and communication quality
- Troubleshooting progress
- Case age relative to complexity
- Premature closure risk
- Restoration without root cause

**Keywords to watch**: down, outage, unavailable, degradation, go-live, upgrade, blocked, escalate, unacceptable, business impact, deadline, frustrated, management

## 7. Architecture — Two-Pass Pipeline

Due to output token limits when processing 250+ cases, the agent uses a two-task pipeline:

### Task 1: Quick Scan — Classify All Cases
- Scans ALL cases in the input file
- Classifies each case into Urgent/High/Medium/No Risk
- Outputs ONLY Urgent, High, and Medium cases (skips No Risk to save tokens)
- One line per case, compact format
- Ends with summary counts of all categories

**Task 1 Output Format**:
```
[Case Number] | [Account] | [Priority] | [Status] | [Risk Level] | [One reason, max 10 words]
...
TOTAL: [count] cases scanned | Urgent: [count] | High: [count] | Medium: [count] | No Risk: [count]
```

### Task 2: Deep Analysis Report
- Uses Task 1 classification results as input
- Generates executive-ready escalation risk report
- Focuses on Urgent and High cases with specific evidence and actions
- Uploads report to Core Share

**Task 2 Output Format**:
```
ESCALATION RISK DETECTION REPORT
Report Date: [date] | Analyzed by: Incident Early Watch Agent

EXECUTIVE SUMMARY
- Total cases reviewed: [number]
- Urgent: [count] | High: [count] | Medium: [count] | No Risk: [count]
- Accounts requiring immediate attention: [count]
- Top Escalation Drivers (3-4 themes)

IMMEDIATE ACTION REQUIRED — URGENT CASES
[Case details with evidence and recommended actions]

TOP ACCOUNTS REQUIRING ATTENTION (max 20 accounts)
[Account details with top issue, why flagged, and specific actions]

ACCOUNTS ON WATCH — [count] with Medium-risk cases
[One line per account]

NO RISK ACCOUNTS — [count]
[Comma-separated list]
```

## 8. Output Delivery

### Primary: Core Share Upload
- **Endpoint**: `POST https://core.opentext.com/api/v3/documents?collisionStrategy=overwrite`
- **Parameters**: `parentId` (folder ID), `file` (report content)
- **Authentication**: Bearer token (JWT)
- **Destination folder**: AITest folder on Core Share (ID: `321813821469491215`)
- **File naming**: `EscalationReport_[YYYY-MM-DD].txt`

### Secondary: Chat Output
- Report also displays in the agent chat interface for immediate viewing

## 9. Anti-Hallucination Techniques

1. **Grounding in source data** — agent must cite specific evidence from case comments/notes
2. **Strict classification rules** — explicit criteria with expected distribution percentages
3. **Two-pass verification** — Task 1 classifies, Task 2 reviews and reports
4. **Selective output** — "if everything is flagged, nothing is flagged" principle
5. **Evidence requirement** — Urgent cases must quote the specific comment confirming system is down
6. **Knowledge base** — AviatorRules.docx can be attached as grounding document with detailed business rules

## 10. Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Two-task pipeline | Yes | Single-task hit output token limit at ~160/258 cases |
| Skip No Risk in Task 1 output | Yes | Reduces output from ~258 lines to ~120, avoids token limit |
| Max 20 accounts in report | Yes | Report with 90+ accounts is useless; selectivity = value |
| Present-tense requirement for Urgent | Yes | Prevents false Urgent flags from historical outage mentions |
| ALL THREE criteria for High | Yes | Prevents over-classification (169 High → 41 High) |
| No structured outputs | Yes | Structured output fields produce JSON, not readable reports |

## 11. Model Configuration

- **Tested model**: Gemini 2.5 Flash (1M token context window)
- **Other available models**: Gemini 3 Flash, Gemini 3 Pro (availability depends on Aviator Studio environment)
- **Key constraint**: `max_output_tokens` is platform-controlled, not configurable by agent builder

## 12. Iteration History

| Version | Key Change | Result |
|---------|-----------|--------|
| V7 | Added structured output references | Produced JSON instead of readable text |
| V8 | Slim approach, only top 1-2 High per account | Agent kept running with no result |
| V9 | Plain headings, expected distribution % | 24 Urgent (too many), 169 High (too many) |
| V10 | Present-tense evidence for Urgent, ALL THREE for High | 5 Urgent, 41 High (correct range) |
| Two-pass | Split into Task 1 (scan) + Task 2 (report) | Processed 160/258 cases |
| Two-pass v2 | Skip No Risk in Task 1 output | Pending full test |

## 13. Known Limitations

1. **Output token limit**: Platform-controlled `max_output_tokens` caps how much the agent can output per task. Two-pass pipeline mitigates but doesn't fully solve for very large case volumes.
2. **Bearer token expiry**: Core Share browser tokens expire in 15 minutes. Production use requires OAuth2 with client_id/client_secret for long-lived tokens.
3. **No email integration**: No built-in email tool in current Aviator Studio environment.
4. **Input file format**: Agent expects a specific column structure from ServiceNow export.

## 14. File References

| File | Description |
|------|-------------|
| `TaskInstructions_V10.md` | Full single-task instruction set (strict classification) |
| `Task1_QuickScan.md` | Two-pass Task 1: compact classification scan |
| `Task2_DeepAnalysis.md` | Two-pass Task 2: executive report generation |
| `coreshare-upload-openapi.yaml` | OpenAPI spec for Core Share file upload |
| `sharepoint-upload-openapi.yaml` | OpenAPI spec for SharePoint upload (alternative, not used) |
| `AviatorRules.docx` | Comprehensive business rules document (knowledge base) |
