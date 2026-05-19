-- Show all claims that are still open.

SELECT
    c.claim_id,
    d.department_name,
    c.claim_type,
    c.claim_amount,
    c.status,
    c.submitted_date,
    c.priority
FROM claims AS c
JOIN departments AS d
    ON c.department_id = d.department_id
WHERE c.status NOT IN ('rejected', 'paid', 'closed')
ORDER BY c.submitted_date ASC;