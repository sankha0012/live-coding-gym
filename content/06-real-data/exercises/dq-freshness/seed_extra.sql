INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900001, 'Rest Never', 'Curitiba', 'pizza');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900002, 'Rest Edge', 'Curitiba', 'burger');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900003, 'Rest Just Stale', 'Curitiba', 'arabic');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900004, 'Rest Never 2', 'Curitiba', 'healthy');
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900001, 1, 900002, 1, '2026-10-29 00:00:00', 30.0, 5.0, NULL, 'delivered', 30, 28.0);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900002, 1, 900003, 1, '2026-10-28 23:59:59', 30.0, 5.0, NULL, 'delivered', 30, 28.0);
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900003, 1, 900003, 1, '2026-10-01 12:00:00', 30.0, 5.0, NULL, 'delivered', 30, 28.0);
