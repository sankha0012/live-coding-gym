WITH d AS (
  SELECT date(created_at) AS day, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY 1
), m AS (
  SELECT day, orders, AVG(orders) OVER (ORDER BY day ROWS 6 PRECEDING) AS a FROM d
)
SELECT day, orders, ROUND(a, 2) AS avg_7d FROM m WHERE day >= '2026-10-20' AND day <= '2026-10-31' ORDER BY day;
