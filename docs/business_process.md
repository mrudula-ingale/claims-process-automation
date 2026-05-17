# Business Process: Insurance Claims Automation

## Project Context

This project simulates an insurance claims operations process. The goal is to use SQL and Python automation to identify delayed claims, analyze operational bottlenecks, and generate recurring reports.

## Business Problem

Claims teams often need to manually review claim data, filter Excel sheets, calculate delays, and prepare regular reports. This project automates those tasks by combining a relational SQL database with Python-based reporting.

## Claims Process

The simplified claims process is:

1. Claim submitted
2. Initial review
3. Document check
4. Decision
5. Payment
6. Closed

## Claim Statuses

| Status | Meaning |
|---|---|
| submitted | Claim was created by customer |
| under_review | Claim is being checked |
| documents_requested | Missing documents are requested |
| approved | Claim is accepted |
| rejected | Claim is rejected |
| paid | Payment was completed |
| closed | Process is fully completed |

## Automation Opportunities

| Manual Task | Automated Solution |
|---|---|
| Checking old open claims | SQL query flags delayed claims |
| Calculating average processing time | SQL aggregation |
| Finding overloaded departments | SQL grouped analysis |
| Preparing weekly Excel report | Python report script |
| Showing KPIs visually | Streamlit dashboard |

## KPIs

| KPI | Description |
|---|---|
| Total claims | Number of claims in the system |
| Open claims | Claims not yet closed |
| Delayed claims | Open claims older than 14 days |
| Average processing time | Average days from submitted to closed |
| Approval rate | Approved claims divided by total decided claims |
| Rejection rate | Rejected claims divided by total decided claims |
| Claim volume by month | Number of claims submitted per month |
| Average claim amount | Average requested claim value |
| Department workload | Number of active claims per department |

## Business Rules

- A claim is delayed if it is still open after more than 14 days.
- A high-value claim is any claim with an amount greater than 5000 EUR.
- A claim is open if its status is not `rejected`, `paid`, or `closed`.
- Processing time is calculated as the difference between the submitted date and closed date.

## Data Entities

| Entity | Description |
|---|---|
| Customer | Person who submitted a claim |
| Department | Team handling the claim |
| Claim | Main claim information |
| Claim Event | Status history over time |
| Payment | Payment information for approved claims |