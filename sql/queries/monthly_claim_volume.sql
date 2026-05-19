-- Count how many claims were submitted each month.

SELECT
    strftime('%Y-%m', submitted_date) AS claim_month,
    COUNT(*) AS total_claims
FROM claims
GROUP BY claim_month
ORDER BY claim_month;
