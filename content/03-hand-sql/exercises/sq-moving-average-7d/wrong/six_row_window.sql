SELECT day, orders, avg_7d FROM (
  SELECT date(created_at) AS day, COUNT(*) AS orders,
         ROUND(AVG(COUNT(*)) OVER (ORDER BY date(created_at) ROWS BETWEEN 5 PRECEDING AND CURRENT ROW), 2) AS avg_7d
  FROM orders WHERE status = 'delivered' GROUP BY date(created_at)
)
WHERE day BETWEEN '2026-10-20' AND '2026-10-31' ORDER BY day;
