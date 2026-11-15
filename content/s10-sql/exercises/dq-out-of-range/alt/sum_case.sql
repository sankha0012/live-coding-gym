SELECT 'actual_over_4x' AS rule_name, COALESCE(SUM(actual_minutes > 4 * promised_minutes), 0) AS violations FROM orders
UNION ALL
SELECT 'negative_amount', COALESCE(SUM(subtotal < 0 OR delivery_fee < 0), 0) FROM orders
UNION ALL
SELECT 'nonpositive_minutes', COALESCE(SUM(promised_minutes <= 0 OR actual_minutes < 0), 0) FROM orders
UNION ALL
SELECT 'subtotal_over_150', COALESCE(SUM(subtotal > 150), 0) FROM orders
ORDER BY rule_name;
