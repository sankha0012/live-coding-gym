WITH rev AS (
  SELECT r.restaurant_id, ROUND(COALESCE(SUM(o.subtotal), 0), 2) AS revenue
  FROM restaurants r LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id AND o.status = 'delivered'
  GROUP BY r.restaurant_id
)
SELECT restaurant_id, revenue FROM rev
WHERE revenue > (SELECT AVG(revenue) FROM rev)
ORDER BY revenue DESC, restaurant_id;
