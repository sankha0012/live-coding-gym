Count delivered orders for each pair of restaurant city and cuisine. Return city, cuisine and delivered_orders. Pairs with no delivered orders do not appear. Sort by city, then cuisine.

Tables:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
