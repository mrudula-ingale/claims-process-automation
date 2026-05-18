-- Validate that all tables were populated correctly.

SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'departments' AS table_name, COUNT(*) AS row_count FROM departments
UNION ALL
SELECT 'claims' AS table_name, COUNT(*) AS row_count FROM claims
UNION ALL
SELECT 'claim_events' AS table_name, COUNT(*) AS row_count FROM claim_events
UNION ALL
SELECT 'payments' AS table_name, COUNT(*) AS row_count FROM payments;