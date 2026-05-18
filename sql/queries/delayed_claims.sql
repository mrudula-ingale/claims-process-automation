-- Find open claims older than 14 days.

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