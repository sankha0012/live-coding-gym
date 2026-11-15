SELECT customer_id, name FROM customers
WHERE city IN ('Curitiba', 'Belo Horizonte') AND signup_date >= '2026-01-08' AND signup_date < '2026-03-13' AND name LIKE 'Customer 1%';
