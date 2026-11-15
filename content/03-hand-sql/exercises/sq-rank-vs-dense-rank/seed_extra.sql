INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900001, 'Rest X1', 'Curitiba', 'pizza');
INSERT INTO restaurants (restaurant_id, name, city, cuisine) VALUES (900002, 'Rest X2', 'Curitiba', 'japanese');
INSERT INTO orders (order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes) VALUES (900001, 1, 900001, NULL, '2026-10-05 12:00:00', 40.0, 5.0, NULL, 'cancelled', 40, NULL);
