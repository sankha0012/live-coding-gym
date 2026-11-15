WITH rev AS (
  SELECT restaurant_id, ROUND(SUM(subtotal), 2) AS revenue FROM orders GROUP BY restaurant_id
)
SELECT restaurant_id, revenue FROM rev
WHERE revenue > (SELECT AVG(revenue) FROM rev)
ORDER BY revenue DESC, restaurant_id;
