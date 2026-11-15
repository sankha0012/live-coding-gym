SELECT r.restaurant_id, MAX(o.created_at) AS latest_created_at
FROM restaurants r JOIN orders o ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id
HAVING MAX(o.created_at) < '2026-10-29 00:00:00'
ORDER BY latest_created_at, r.restaurant_id;
