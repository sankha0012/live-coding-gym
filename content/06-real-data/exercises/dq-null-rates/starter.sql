SELECT 'subtotal' AS column_name, ROUND(100.0 * SUM(subtotal IS NULL) / COUNT(*), 2) AS null_pct
FROM orders
