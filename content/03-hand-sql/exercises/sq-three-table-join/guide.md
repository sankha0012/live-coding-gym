**Why this matters.** Real questions spread facts across tables: the order is in one, the restaurant's cuisine in another, the courier's vehicle in a third. We connect them by their ids.

**How we get there.**
1. Start from `orders`, the center, because each row is one event we want to list.
2. `JOIN restaurants r ON r.restaurant_id = o.restaurant_id` brings the restaurant name and cuisine.
3. `JOIN couriers k ON k.courier_id = o.courier_id` brings the courier name and vehicle.
4. Filter with `WHERE o.status = 'delivered' AND k.vehicle = 'car' AND r.cuisine = 'japanese'`.
5. Both `restaurants` and `couriers` have a `name`, so we alias them: `restaurant_name` and `courier_name`. Then `ORDER BY o.order_id`.

**Check it.** Cancelled orders have a NULL courier, so the inner join would drop them anyway; the status filter just makes it explicit. Each join matches on a key, so the cost stays linear in the orders.

**Watch out.** Selecting `name` twice without aliases, which gives two columns with the same name and no way to tell them apart.
