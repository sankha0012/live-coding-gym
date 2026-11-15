SELECT r.restaurant_id, MAX(o.created_at) AS latest_created_at
FROM restaurants r LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id
WHERE o.created_at IS NULL OR o.created_at < '2026-10-29 00:00:00'
GROUP BY r.restaurant_id
ORDER BY latest_created_at, r.restaurant_id;
