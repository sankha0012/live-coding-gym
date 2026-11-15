WITH d AS (
  SELECT date(created_at) AS day, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY 1
)
SELECT day, orders,
       ROUND((SELECT AVG(orders) FROM (SELECT orders FROM d d2 WHERE d2.day <= d.day ORDER BY d2.day DESC LIMIT 7)), 2) AS avg_7d
FROM d WHERE day BETWEEN '2026-10-20' AND '2026-10-31' ORDER BY day;
