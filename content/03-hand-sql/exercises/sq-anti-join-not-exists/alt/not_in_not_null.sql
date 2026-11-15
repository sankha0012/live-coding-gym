SELECT customer_id, name FROM customers
WHERE city = 'Rio de Janeiro'
  AND customer_id NOT IN (SELECT customer_id FROM orders WHERE status = 'delivered' AND customer_id IS NOT NULL)
ORDER BY customer_id;
