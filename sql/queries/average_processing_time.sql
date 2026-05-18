-- Calculate average processing time for completed claims.

SELECT
    ROUND(AVG(julianday(closed_date) - julianday(submitted_date)), 2)
        AS average_processing_days
FROM claims
WHERE closed_date IS NOT NULL;