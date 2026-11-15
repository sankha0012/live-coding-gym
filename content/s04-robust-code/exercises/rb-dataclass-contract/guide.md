**Why this matters.** Bad records are cheapest to catch at the door. If an invalid order can be built, every function downstream has to doubt it. And when it is rejected, the sender wants all the problems at once, not one per retry.

**How we get there.**
1. Declare the dataclass with the four fields, and put the checks in `__post_init__`. It runs right after the object is filled, so an `Order` that exists is a valid one.
2. Start an empty `problems` list. Check each field in order and append its message, instead of raising immediately.
3. Be strict about types. `True` is an `int` in Python, so for `items` and `total` we reject `bool` first, then check `isinstance`, then the range.
4. For `total`, test `math.isnan(t)` explicitly. NaN is never less than zero, so `t < 0` alone lets it through.
5. At the end, `if problems: raise ValueError("; ".join(problems))`.

**Check it.** A valid order raises nothing; an empty id with `items=0` gives `order_id invalid; items invalid`. Checking is constant work per record.

**Watch out.** Raising at the first failure hides the other problems, and forgetting bool and NaN lets `True` items and NaN totals slip in.
