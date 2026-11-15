WITH rev AS (
  SELECT restaurant_id, ROUND(SUM(subtotal), 2) AS revenue FROM orders WHERE status = 'delivered' GROUP BY restaurant_id
)
SELECT restaurant_id, revenue FROM rev
WHERE revenue > (SELECT AVG(subtotal) FROM orders WHERE status = 'delivered')
ORDER BY revenue DESC, restaurant_id;
