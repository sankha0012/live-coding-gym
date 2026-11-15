WITH t AS (SELECT COUNT(*) AS total FROM orders),
g AS (
  SELECT 'by_status' AS check_name, (SELECT SUM(n) FROM (SELECT COUNT(*) AS n FROM orders GROUP BY status)) AS grouped_total
  UNION ALL SELECT 'by_restaurant', (SELECT COUNT(*) FROM orders o WHERE EXISTS (SELECT 1 FROM restaurants r WHERE r.restaurant_id = o.restaurant_id))
  UNION ALL SELECT 'by_courier', (SELECT COUNT(*) FROM orders o WHERE EXISTS (SELECT 1 FROM couriers c WHERE c.courier_id = o.courier_id))
)
SELECT check_name, total AS total_orders, grouped_total, total - grouped_total AS difference
FROM g, t ORDER BY check_name;
