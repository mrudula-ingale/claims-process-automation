-- Count claims by priority level.

SELECT
    priority,
    COUNT(*) AS total_claims
FROM claims
GROUP BY priority
ORDER BY total_claims DESC;