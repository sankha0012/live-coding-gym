SELECT MAX(subtotal) AS second FROM orders WHERE status = 'delivered' AND subtotal < (SELECT MAX(subtotal) FROM orders WHERE status = 'delivered');
