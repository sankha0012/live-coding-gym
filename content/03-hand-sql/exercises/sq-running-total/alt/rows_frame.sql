SELECT day, ROUND(revenue, 2) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_total
FROM (SELECT date(created_at) AS day, SUM(subtotal) AS revenue FROM orders
      WHERE status = 'delivered' AND date(created_at) BETWEEN '2026-10-01' AND '2026-10-07' GROUP BY 1)
ORDER BY day;
