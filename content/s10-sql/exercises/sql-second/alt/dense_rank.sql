SELECT subtotal AS second FROM (SELECT DISTINCT subtotal, DENSE_RANK() OVER (ORDER BY subtotal DESC) AS rk FROM orders WHERE subtotal IS NOT NULL) WHERE rk = 2;
