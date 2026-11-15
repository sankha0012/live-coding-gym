INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900001, 'Rest Cancelled Only', 'Curitiba', 'pizza');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900002, 'Rest Near Average', 'Curitiba', 'pizza');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900003, 'Rest Tie A', 'Curitiba', 'pizza');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900004, 'Rest Tie B', 'Curitiba', 'pizza');
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900001, 1, 900001, NULL, '2026-10-30 12:00:00', 30.0, 5.0, NULL, 'cancelled', 30, NULL);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900002, 1, 900002, 1, '2026-10-30 12:05:00', 4650.0, 5.0, NULL, 'delivered', 30, 25.0);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900003, 1, 900003, 1, '2026-10-30 12:10:00', 7000.0, 5.0, NULL, 'delivered', 30, 25.0);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900004, 1, 900004, 1, '2026-10-30 12:15:00', 7000.0, 5.0, NULL, 'delivered', 30, 25.0);
