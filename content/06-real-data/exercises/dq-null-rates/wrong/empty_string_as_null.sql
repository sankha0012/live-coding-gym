SELECT column_name, null_pct FROM (
  SELECT 'subtotal' AS column_name, ROUND(100.0 * SUM(subtotal IS NULL) / COUNT(*), 2) AS null_pct FROM orders
  UNION ALL
  SELECT 'courier_id', ROUND(100.0 * SUM(courier_id IS NULL) / COUNT(*), 2) FROM orders
  UNION ALL
  SELECT 'coupon_code', ROUND(100.0 * SUM(coupon_code IS NULL OR coupon_code = '') / COUNT(*), 2) FROM orders
  UNION ALL
  SELECT 'actual_minutes', ROUND(100.0 * SUM(actual_minutes IS NULL) / COUNT(*), 2) FROM orders
)
WHERE null_pct > 0
ORDER BY null_pct DESC, column_name;
