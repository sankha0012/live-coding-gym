INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900001, 'Salvador A', 'Salvador', 'pizza');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900002, 'Salvador B', 'Salvador', 'burger');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900003, 'Recife A', 'Recife', 'pizza');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900004, 'Recife B', 'Recife', 'burger');
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900001, 1, 900001, 1, '2026-10-30 12:00:00', 20.0, 5.0, NULL, 'delivered', 30, 25.0);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900002, 1, 900002, 1, '2026-10-30 12:05:00', 80.0, 5.0, NULL, 'delivered', 30, 25.0);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900003, 1, 900001, NULL, '2026-10-30 12:10:00', 10.0, 5.0, NULL, 'cancelled', 30, NULL);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900004, 1, 900003, 1, '2026-10-30 12:15:00', 20.03, 5.0, NULL, 'delivered', 30, 25.0);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900005, 1, 900004, 1, '2026-10-30 12:20:00', 79.97, 5.0, NULL, 'delivered', 30, 25.0);
