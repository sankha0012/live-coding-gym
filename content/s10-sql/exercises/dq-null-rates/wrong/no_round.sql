SELECT column_name, null_pct FROM (
  SELECT 'subtotal' AS column_name, 100.0 * SUM(subtotal IS NULL) / COUNT(*) AS null_pct FROM orders
  UNION ALL
  SELECT 'courier_id', 100.0 * SUM(courier_id IS NULL) / COUNT(*) FROM orders
  UNION ALL
  SELECT 'coupon_code', 100.0 * SUM(coupon_code IS NULL) / COUNT(*) FROM orders
  UNION ALL
  SELECT 'actual_minutes', 100.0 * SUM(actual_minutes IS NULL) / COUNT(*) FROM orders
)
WHERE null_pct > 0
ORDER BY null_pct DESC, column_name;
