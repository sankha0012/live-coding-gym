SELECT customer_id, name FROM customers
WHERE (city = 'Curitiba' OR city = 'Belo Horizonte')
  AND signup_date >= '2026-01-08' AND signup_date <= '2026-03-13'
  AND SUBSTR(name, 1, 10) = 'Customer 1';
