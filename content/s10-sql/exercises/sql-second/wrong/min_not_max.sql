SELECT MIN(subtotal) AS second FROM orders WHERE subtotal > (SELECT MIN(subtotal) FROM orders);
