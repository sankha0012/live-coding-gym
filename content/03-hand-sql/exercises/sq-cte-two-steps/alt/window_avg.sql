SELECT restaurant_id, revenue FROM (
  SELECT restaurant_id, ROUND(SUM(subtotal), 2) AS revenue,
         AVG(ROUND(SUM(subtotal), 2)) OVER () AS avg_rev
  FROM orders WHERE status = 'delivered' GROUP BY restaurant_id)
WHERE revenue > avg_rev ORDER BY revenue DESC, restaurant_id;
