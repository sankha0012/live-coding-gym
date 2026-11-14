SELECT 'subtotal_over_150' AS rule_name, COUNT(*) AS violations
FROM orders WHERE subtotal > 150
