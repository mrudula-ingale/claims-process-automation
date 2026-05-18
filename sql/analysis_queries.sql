-- Query 1 — Validate table row counts
-- Validate that all tables were populated correctly.
-- UNION ALL combines multiple SELECT results into one result table.
SELECT 'customers' AS  table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'departments' AS  table_name, COUNT(*) AS row_count FROM departments
UNION ALL
SELECT 'claims' AS  table_name, COUNT(*) AS row_count FROM claims
UNION ALL
SELECT 'claim_events' AS  table_name, COUNT(*) AS row_count FROM claim_events
UNION ALL
SELECT 'payments' AS  table_name, COUNT(*) AS row_count FROM payments;

-- Query 2 — Claims by status
-- Count how many claims are currently in each status.
-- This helps the business understand the workload distribution.
SELECT 
    status,
    COUNT(*) AS total_claims
FROM claims
GROUP BY status
ORDER BY total_claims DESC;

-- Query 3 — Show open claims
-- Show all claims that are still open.
-- A claim is open if it has not reached a final status.
SELECT
    claim_id,
    claim_type,
    claim_amount,
    status,
    submitted_date,
    priority
FROM claims
WHERE status NOT IN ('rejected', 'paid', 'closed')
ORDER BY submitted_date ASC;

-- Query 4 — Delayed open claims
-- Find open claims older than 14 days.
-- julianday() converts a date into a number so we can calculate date differences.
SELECT
    claim_id,
    claim_type,
    claim_amount,
    status,
    submitted_date,
    ROUND(julianday('now') - julianday(submitted_date), 1) AS days_open,
    priority
FROM claims
WHERE status NOT IN ('rejected', 'paid', 'closed')
    AND julianday('now') - julianday(submitted_date) > 14
ORDER BY days_open DESC;

-- Query 5 — Average processing time
-- Calculate average processing time for completed claims.
-- Processing time = closed_date - submitted_date.
SELECT
    ROUND(AVG(julianday(closed_date) - julianday(submitted_date)), 2)
        AS average_processing_days
FROM claims
WHERE closed_date IS NOT NULL;

-- Query 6 — Department workload
-- Count open claims per department.
-- JOIN connects claims with department names.
SELECT
	d.department_name,
	COUNT(c.claim_id) AS open_claims
FROM claims AS c
JOIN departments AS d
	ON c.department_id = d.department_id
WHERE c.status NOT IN ('rejected', 'paid', 'closed')
GROUP BY d.department_name
ORDER BY open_claims DESC;

-- Query 7 — High-value claims
-- Identify high-value claims above 5000 EUR.
-- These may require priority handling or additional review.
SELECT 
    claim_id,
    claim_type,
    claim_amount,
    status,
    submitted_date,
    priority
FROM claims
WHERE claim_amount > 5000
ORDER BY claim_amount DESC;

-- Query 8 — Monthly claim volume
-- Count how many claims were submitted each month.
-- strftime('%Y-%m', submitted_date) extracts year and month.
SELECT 
    strftime('%Y-%m', submitted_date) AS claim_month,
    COUNT(*) AS total_claims
FROM claims
GROUP BY claim_month
ORDER BY claim_month;

-- Query 9 — Approval and rejection rates
-- Calculate approval and rejection rates as percentages.
-- CASE WHEN allows conditional counting inside SQL.
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN status IN ('approved', 'paid', 'closed') THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate_percent,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN status = 'rejected' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS rejection_rate_percent
FROM claims;

-- Query 10 — Claims with customer and department details
-- Combine claims with customer and department information.
-- This is useful for operational reports.
SELECT
    c.claim_id,
    cu.first_name || ' ' || cu.last_name AS customer_name,
    cu.city,
    d.department_name,
    c.claim_type,
    c.claim_amount,
    c.status,
    c.submitted_date,
    c.priority
FROM claims AS c
JOIN customers AS cu
    ON c.customer_id = cu.customer_id
JOIN departments AS d
    ON c.department_id = d.department_id
ORDER BY c.submitted_date DESC
LIMIT 20;