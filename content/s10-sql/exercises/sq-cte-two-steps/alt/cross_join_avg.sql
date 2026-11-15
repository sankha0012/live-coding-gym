WITH rev AS (
  SELECT restaurant_id, ROUND(SUM(subtotal), 2) AS revenue FROM orders WHERE status = 'delivered' GROUP BY restaurant_id
), a AS (SELECT AVG(revenue) AS m FROM rev)
SELECT rev.restaurant_id, rev.revenue FROM rev, a WHERE rev.revenue > a.m
ORDER BY rev.revenue DESC, rev.restaurant_id;
