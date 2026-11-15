SELECT subtotal AS second FROM (SELECT subtotal, ROW_NUMBER() OVER (ORDER BY subtotal DESC) AS rn FROM orders) WHERE rn = 2;
