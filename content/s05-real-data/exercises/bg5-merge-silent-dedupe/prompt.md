Joining orders with restaurants must not create or lose orders. Write `merge_restaurants(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame`.

It does a left merge of `orders` with `restaurants` on `restaurant_id`, so every order keeps one row and gets the restaurant columns (orders without a matching restaurant get NaN there). The order of the rows is the order of `orders`.

Then it checks the row count. If the merged frame does not have exactly as many rows as `orders` (for example because `restaurants` has the same `restaurant_id` twice), raise `ValueError`. Do not return a partly fixed frame. Do not modify the inputs.

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
