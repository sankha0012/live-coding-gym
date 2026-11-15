WITH n AS (SELECT customer_id, COUNT(*) AS k FROM orders WHERE status = 'delivered' GROUP BY customer_id)
SELECT COUNT(*) AS loyal FROM n WHERE k >= 3;
