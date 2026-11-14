FIRST_VALUE(subtotal) OVER (PARTITION BY customer_id ORDER BY created_at, order_id) repeats the first row's value on every row of the customer.
