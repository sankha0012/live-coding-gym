Some orders have a NULL subtotal. List those orders with their total, where total = subtotal + delivery_fee and a missing subtotal counts as 0. Columns: order_id, total. Sort by order_id.

*NULL + number is NULL. COALESCE fixes that.*

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
