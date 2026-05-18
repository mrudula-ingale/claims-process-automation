-- Count open claims per department.

SELECT
    d.department_name,
    COUNT(c.claim_id) AS open_claims
FROM claims AS c
JOIN departments AS d
    ON c.department_id = d.department_id
WHERE c.status NOT IN ('rejected', 'paid', 'closed')
GROUP BY d.department_name
ORDER BY open_claims DESC;