Find restaurants with more than 100 delivered orders. Return restaurant_id and delivered_orders (the count). Most orders first, ties by restaurant_id.

Tables:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
