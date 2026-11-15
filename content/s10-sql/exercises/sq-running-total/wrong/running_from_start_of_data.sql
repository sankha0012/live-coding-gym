SELECT day, revenue, running_total FROM (
  SELECT date(created_at) AS day, ROUND(SUM(subtotal), 2) AS revenue,
         ROUND(SUM(SUM(subtotal)) OVER (ORDER BY date(created_at)), 2) AS running_total
  FROM orders WHERE status = 'delivered' GROUP BY date(created_at)
) WHERE day BETWEEN '2026-10-01' AND '2026-10-07' ORDER BY day;
