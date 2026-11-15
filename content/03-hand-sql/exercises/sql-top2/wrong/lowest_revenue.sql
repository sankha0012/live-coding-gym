WITH rev AS (SELECT r.city, o.restaurant_id, SUM(o.subtotal) AS revenue FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered' GROUP BY r.city, o.restaurant_id)
SELECT * FROM (SELECT rev.*, ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue) AS rn FROM rev) WHERE rn <= 2 ORDER BY city, rn;
