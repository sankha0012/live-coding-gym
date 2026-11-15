SELECT 'actual_over_4x' AS rule_name, COUNT(*) AS violations FROM orders WHERE actual_minutes > 4 * promised_minutes
UNION ALL
SELECT 'negative_amount', (SELECT COUNT(*) FROM orders WHERE subtotal < 0) + (SELECT COUNT(*) FROM orders WHERE delivery_fee < 0)
UNION ALL
SELECT 'nonpositive_minutes', COUNT(*) FROM orders WHERE promised_minutes <= 0 OR actual_minutes < 0
UNION ALL
SELECT 'subtotal_over_150', COUNT(*) FROM orders WHERE subtotal > 150
ORDER BY rule_name;
