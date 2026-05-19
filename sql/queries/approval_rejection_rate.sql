-- Calculate approval and rejection rates as percentages.

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