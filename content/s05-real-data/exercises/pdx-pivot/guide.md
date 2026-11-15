**Why this matters.** A city by cuisine table answers "where do people order what" at a glance. Getting it right means joining first, counting rows instead of summing ids, and making sure empty cells show a real zero.

**How we get there.**
1. Orders only know `restaurant_id`, so merge the city and cuisine in with a left join on `restaurant_id`. We keep just the columns we need.
2. Build the table with `pivot_table(index="city", columns="cuisine", ...)`. Cities become rows and cuisines become columns, both sorted alphabetically by default.
3. The cell value is `values="order_id"` with `aggfunc="count"`. Counting rows is what the problem asks for, whereas summing ids would be meaningless.
4. Add `fill_value=0`. A pair with no orders then shows `0`, not NaN, and the cells stay integers.

Only cities and cuisines that appear in the merged orders get a row or column, which matches the rule that unused ones do not show.

**Check it.** Adding up all the cells gives the number of orders. The cost is linear in the number of orders.

**Watch out.** Forgetting `fill_value=0` leaves NaN cells, which also turns the whole table into floats.
