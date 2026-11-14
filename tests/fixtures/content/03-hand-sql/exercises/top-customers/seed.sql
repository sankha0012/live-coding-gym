CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Bruno'), (3, 'Carla');
INSERT INTO orders VALUES (1, 1, 80), (2, 1, 70), (3, 2, 40), (4, 3, 200), (5, 3, 10);
