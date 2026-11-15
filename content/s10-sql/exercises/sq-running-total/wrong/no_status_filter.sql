WITH d AS (SELECT date(created_at) AS day, SUM(subtotal) AS revenue FROM orders
  WHERE date(created_at) BETWEEN '2026-10-01' AND '2026-10-07' GROUP BY date(created_at))
SELECT day, ROUND(revenue, 2) AS revenue, ROUND(SUM(revenue) OVER (ORDER BY day), 2) AS running_total FROM d ORDER BY day;
