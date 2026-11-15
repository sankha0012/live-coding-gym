SELECT subtotal AS second FROM (SELECT subtotal, RANK() OVER (ORDER BY subtotal DESC) AS rk FROM orders) WHERE rk = 2 LIMIT 1;
