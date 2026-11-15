WITH d AS (SELECT date(created_at) AS day, SUM(subtotal) AS revenue FROM orders
  WHERE status = 'delivered' AND created_at >= '2026-10-01' AND created_at < '2026-10-08' GROUP BY 1)
SELECT a.day, ROUND(a.revenue, 2) AS revenue, ROUND((SELECT SUM(b.revenue) FROM d b WHERE b.day <= a.day), 2) AS running_total
FROM d a ORDER BY a.day;
