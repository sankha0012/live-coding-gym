WITH m AS (SELECT substr(created_at, 1, 7) AS month, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY 1)
SELECT a.month, a.orders, a.orders - b.orders AS diff FROM m a LEFT JOIN m b ON b.month = strftime('%Y-%m', date(a.month || '-01', '-1 month')) ORDER BY a.month;
