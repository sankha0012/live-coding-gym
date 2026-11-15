SELECT name, cuisine FROM (SELECT * FROM restaurants WHERE city = 'Belo Horizonte') ORDER BY restaurant_id;
