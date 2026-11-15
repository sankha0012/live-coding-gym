SELECT r.restaurant_id, m.latest AS latest_created_at
FROM restaurants r
LEFT JOIN (SELECT restaurant_id, MAX(created_at) AS latest FROM orders GROUP BY restaurant_id) m
  ON m.restaurant_id = r.restaurant_id
WHERE m.latest IS NULL OR m.latest < '2026-10-29 00:00:00'
ORDER BY m.latest, r.restaurant_id;
