SELECT r.restaurant_id, MIN(o.created_at) AS latest_created_at
FROM restaurants r LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id
HAVING MIN(o.created_at) IS NULL OR MIN(o.created_at) < '2026-10-29 00:00:00'
ORDER BY latest_created_at, r.restaurant_id;
