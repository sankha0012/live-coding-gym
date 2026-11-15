WITH r AS (
  SELECT 'subtotal' AS column_name, ROUND(100.0 * AVG(subtotal IS NULL), 2) AS null_pct FROM orders
  UNION ALL SELECT 'courier_id', ROUND(100.0 * AVG(courier_id IS NULL), 2) FROM orders
  UNION ALL SELECT 'coupon_code', ROUND(100.0 * AVG(coupon_code IS NULL), 2) FROM orders
  UNION ALL SELECT 'actual_minutes', ROUND(100.0 * AVG(actual_minutes IS NULL), 2) FROM orders
)
SELECT column_name, null_pct FROM r WHERE null_pct > 0 ORDER BY null_pct DESC, column_name;
