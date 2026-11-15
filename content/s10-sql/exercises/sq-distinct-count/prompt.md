For delivered orders from restaurants with cuisine 'pizza', return one row with two numbers: customers (how many different customers ordered) and orders (how many orders in total).

Tables used:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
