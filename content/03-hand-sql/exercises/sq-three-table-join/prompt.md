List the delivered orders handled by a courier with vehicle 'car' from a restaurant with cuisine 'japanese'. Columns: order_id, restaurant_name, courier_name. Sort by order_id.

Tables:

```
orders(order_id, restaurant_id, courier_id, status)   -- cancelled orders have courier_id NULL
restaurants(restaurant_id, name, city, cuisine)
couriers(courier_id, name, vehicle)
```
