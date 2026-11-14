SELECT r.restaurant_id, MAX(o.created_at) AS latest_created_at
FROM restaurants r
