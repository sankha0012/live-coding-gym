INSERT INTO customers (customer_id, name, city, signup_date) VALUES (900001, 'Cust X1', 'Curitiba', '2026-07-01');
INSERT INTO customers (customer_id, name, city, signup_date) VALUES (900002, 'Cust X2', 'Curitiba', '2026-07-02');
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900001, 900001, 1, 1, '2026-10-05 12:00:00', 636.53, 5.0, NULL, 'delivered', 40, 30.0);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900002, 900002, 1, NULL, '2026-10-06 12:00:00', 900.0, 5.0, NULL, 'cancelled', 40, NULL);
INSERT INTO customers (customer_id, name, city, signup_date) VALUES (900003, 'Cust X3', 'Curitiba', '2026-07-03');
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900003, 900003, 1, 1, '2026-10-07 12:00:00', 636.53, 5.0, NULL, 'delivered', 40, 30.0);
