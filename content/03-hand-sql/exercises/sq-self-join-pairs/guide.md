**Why this matters.** Sometimes the question is about two rows of the same table, such as a customer who ordered twice from the same place. We solve it by joining the table to itself.

**How we get there.**
1. Read `orders` twice under two aliases, `a` and `b`. Think of them as the first order and the second order.
2. Join them on the same `customer_id` and the same `restaurant_id`.
3. Add `b.order_id > a.order_id`. This stops an order from pairing with itself and counts each pair once.
4. Join `restaurants` and keep `city = 'Rio de Janeiro'` and `cuisine = 'burger'`.
5. A customer with three orders at one place makes three pairs, so we use `SELECT DISTINCT` to get one row per customer and restaurant, then sort.

**Check it.** The self join can create many pairs per customer, up to the square of their orders at one restaurant. Fine here, but grows quickly.

**Watch out.** Joining without `b.order_id > a.order_id`: every order matches itself, so customers with a single order would wrongly appear.
