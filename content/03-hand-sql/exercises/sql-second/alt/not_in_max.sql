SELECT MAX(subtotal) AS second FROM orders WHERE subtotal NOT IN (SELECT MAX(subtotal) FROM orders);
