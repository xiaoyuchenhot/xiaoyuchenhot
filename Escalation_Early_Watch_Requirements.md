# Escalation Early Watch — Requirements Specification

## Objective

Build an AI-powered early warning system that detects at-risk customer support incidents before they escalate. The system combines data from three source systems — ServiceNow (ticketing), CRM/Sales, and Project Management — and uses OpenText Aviator Studio to analyze consolidated incident data, score risk, and route alerts.

## Problem Statement

- Aviator Studio has no direct connector to ServiceNow.
- Incident data, customer context (hot deals, customer temperature), and go-live schedules live in separate systems with no unified risk view.
- Support managers lack proactive visibility into which incidents are "going south" until a customer escalates.

## Source Systems

| System | Data Points | Refresh Rate |
|--------|------------|--------------|
| **ServiceNow** (ticketing — NOT SMAX) | Incidents, blockers, priority, assignment, SLA status, resolution, escalation count, repeat issue history, activity logs, email count | Every 10 min |
| **CRM / Sales** | Account tier, hot deal flag, deal stage, customer temperature score, CSM owner | Every 30 min |
| **Project / PM Tool** | Go-live date, project phase, milestone blockers, days to go-live | Daily |

## Risk Signals to Detect

1. **Hot deal customer with open blockers** — revenue at risk, sales will escalate
2. **Go-live in <30 days with unresolved P1/P2** — customer may miss launch date
3. **Declining customer temperature or escalated sentiment** — customer is already unhappy
4. **SLA breached** — contractual violation
5. **Repeat high-severity issues (3+ times)** — systemic problem, not a one-off
6. **Production system down (P1)** — active business impact
7. **Stale case (no activity 5+ days)** — customer feels abandoned
8. **High email volume (>5 unresolved)** — customer repeatedly reaching out
9. **Prior escalation history** — already formally escalated

## Consolidated Data Model

The BI job should produce a single flat file (CSV saved as .txt) with one row per open incident, enriched with customer context. Columns:

| Column | Source | Example |
|--------|--------|---------|
| Account | CRM | Deutsche Bank AG |
| Is_Hot_Deal | CRM | Yes |
| Customer_Temperature | CRM | Cold / Warm / Hot / Escalated |
| Go_Live_Date | PM Tool | 2026-09-15 |
| Days_To_GoLive | PM Tool | 28 |
| Go_Live_Blockers | PM Tool | 2 |
| Case_Number | ServiceNow | INC0741215 |
| Title | ServiceNow | OTDS auth failing for SSO |
| Priority | ServiceNow | 1 - Critical |
| Status | ServiceNow | Open |
| Is_Blocker | ServiceNow | Yes |
| SLA_Breached | ServiceNow | Yes |
| Days_Open | ServiceNow | 5 |
| Repeat_Issue_Count | ServiceNow (historical) | 3 |
| Escalation_Count | ServiceNow | 2 |
| Email_Count | ServiceNow | 14 |
| System_In_Production | PM Tool | Yes |
| Last_Activity_Date | ServiceNow | 2026-08-10 |

Join key: Account / Customer ID at the BI layer.

## Risk Scoring Model

| Signal | Condition | Points |
|--------|-----------|--------|
| Hot deal + blocker | Is_Hot_Deal=Yes AND Is_Blocker=Yes | +5 |
| Go-live at risk | Days_To_GoLive < 30 AND open P1/P2 | +4 |
| Customer escalated | Customer_Temperature = Escalated | +4 |
| SLA breached | SLA_Breached = Yes | +3 |
| Repeat high issues | Repeat_Issue_Count >= 3 AND P1/P2 | +3 |
| Production system down | System_In_Production = Yes AND P1 | +3 |
| Stale case | No activity in 5+ days | +2 |
| High email volume | Email_Count > 5 unresolved | +2 |
| Escalation history | Escalation_Count > 0 | +1 |

### Classification Thresholds

| Level | Score | Action |
|-------|-------|--------|
| **CRITICAL** | 8+ points | Immediate alert to VP/Director + Teams notification |
| **WARNING** | 4-7 points | Added to daily risk digest |
| **MONITOR** | 0-3 points | Logged for trend analysis |

## Agent Task Instructions

### Task 1: Parse and Enrich
- Read the CSV input file
- For each row where Status is NOT "Resolved" or "Closed":
  - Calculate days since Last_Activity_Date using today's date
  - Calculate Days_To_GoLive if Go_Live_Date is present
  - Flag repeat issues where Repeat_Issue_Count >= 3

### Task 2: Score and Classify
- Apply the scoring model above
- Sum points per case
- Classify: CRITICAL (8+), WARNING (4-7), MONITOR (0-3)

### Task 3: Generate Report
- Output a summary sorted by score (highest first)
- For CRITICAL and WARNING cases, include:
  - Case #, Account, Title, Score, Triggered Signals
  - Business context: hot deal? go-live date? temperature?
  - Recommended action (one sentence)
- End with ACCOUNT RISK SUMMARY:
  - Group all flagged cases by account
  - Flag accounts with multiple critical/warning cases
  - Flag accounts with hot deal status + any flagged case
  - Flag accounts with go-live < 30 days + any blocker

## Output Routing

| Risk Level | Channel | Timing |
|------------|---------|--------|
| Critical (8+) | Email to VP/Director + Teams notification | Within minutes of detection |
| Warning (4-7) | Daily summary email to team leads + Content Server | Daily 8:00 AM |
| Monitor (0-3) | Content Server archive only | Weekly review |

## Data Lifecycle & Storage

### Layer 1: Staging Database
| Table | Strategy | Retention |
|-------|----------|-----------|
| incident_current | TRUNCATE + INSERT every run (full refresh) | Replaced every 10 min |
| incident_history | INSERT (append) with run_timestamp | 90 days, then archive |
| customer_context | UPSERT by Account ID | Always current |

### Layer 2: Agent Input File
- File: `active_incidents_LATEST.txt` (fixed name, overwritten each run)
- Contains ONLY open/active incidents (not Resolved, Closed, Cancelled)
- Typically 50-200 rows, well within file size limits
- Format: CSV saved as .txt (Aviator Studio supported format)

### Layer 3: Output Archive
- Risk reports saved to Content Server per run: `/EarlyWatch/YYYY/MM/DD/risk_HHMM.txt`
- Daily digest compiled and emailed at 8:00 AM
- Critical alerts sent only when a NEW critical case appears (compare against previous run to avoid alert fatigue)

## Architecture Flow

```
ServiceNow ──(stored proc / REST API, every 10 min)──┐
CRM / Sales ──(API / DB view, every 30 min)───────────┼──> Staging DB ──> BI Job (every 10 min)
Project / PM Tool ──(query / export, daily)───────────┘         │
                                                                ▼
                                                   active_incidents_LATEST.txt
                                                                │
                                                                ▼
                                                   Aviator Studio Agent
                                                   (Parse → Score → Report)
                                                                │
                                          ┌─────────────────────┼─────────────────────┐
                                          ▼                     ▼                     ▼
                                    Email Alert           Risk Report          Dashboard / Teams
                                  (critical only)      (Content Server)       (real-time visibility)
```

## Implementation Roadmap

| Week | Milestone | Owner |
|------|-----------|-------|
| 1-2 | Create stored procedures for ServiceNow extraction | DBA / Data team |
| 2-3 | Add CRM views (hot deal, temperature) and PM views (go-live dates) | CRM admin + PM team |
| 3-4 | Build BI job to consolidate and export CSV/TXT | BI / ETL team |
| 4-5 | Build and test Aviator agent with sample data | Aviator Studio |
| 5-6 | Connect agent trigger to BI job output; add email tool | Integration team |
| 6-7 | UAT with real data; tune scoring thresholds | Support managers |
| 8 | Go live | All |

## Constraints & Notes

- Aviator Studio file input supports: .pdf, .docx, .doc, .txt, .jpeg, .tiff, .png — **NOT .xlsx**
- Agent is deployed to OpenText cloud, invoked via REST API (POST only) or Share button for users
- The mock spreadsheet (`incident_risk_monitor_sample_data.txt`) with 20 sample incidents across 8 accounts is available for testing
- File upload happens at agent Run time, not during agent setup
