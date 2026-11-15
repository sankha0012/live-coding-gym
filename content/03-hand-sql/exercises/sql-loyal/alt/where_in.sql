SELECT COUNT(*) AS loyal FROM customers c WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'delivered') >= 3;
