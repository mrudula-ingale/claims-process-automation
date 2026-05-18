-- Identify claims above 5000 EUR.

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