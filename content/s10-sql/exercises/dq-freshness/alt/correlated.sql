SELECT restaurant_id, latest_created_at FROM (
  SELECT r.restaurant_id,
         (SELECT MAX(o.created_at) FROM orders o WHERE o.restaurant_id = r.restaurant_id) AS latest_created_at
  FROM restaurants r
)
WHERE latest_created_at IS NULL OR latest_created_at < '2026-10-29 00:00:00'
ORDER BY latest_created_at, restaurant_id;
