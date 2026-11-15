SELECT date(created_at) AS day, ROUND(SUM(subtotal) OVER (PARTITION BY date(created_at)), 2) AS revenue,
       ROUND(SUM(subtotal) OVER (ORDER BY created_at, order_id), 2) AS running_total
FROM orders WHERE status = 'delivered' AND date(created_at) BETWEEN '2026-10-01' AND '2026-10-07' ORDER BY created_at, order_id;
