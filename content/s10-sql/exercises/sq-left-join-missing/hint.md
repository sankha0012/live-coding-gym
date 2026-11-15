A LEFT JOIN keeps every customer and fills the order columns with NULL when there is no match. Then test a column of orders with IS NULL.
