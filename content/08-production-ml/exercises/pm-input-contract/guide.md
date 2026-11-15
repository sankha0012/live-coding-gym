**Why this matters.** A prediction API gets whatever clients send. Bad input should be caught at the door with a clear list of problems, so the model never sees a string where it expects a number.

**How we get there.**
1. Loop over the contract, not the request. Violations come out in contract order and unknown fields drop for free.
2. Read `request.get(name)`. `None` or absent is missing: add `"missing:<name>"` if required, and either way move on.
3. Check the type. `bool` is a subclass of `int` in Python, so we exclude it explicitly. An `int` is accepted for a float field, and we convert it with `float(value)`.
4. For numbers, check `nan` and the inclusive `min` and `max`, and add `"out_of_range:<name>"`. `nan` fails every comparison, so it needs its own `math.isnan` test.
5. A field with a violation uses `continue`, so it stays out of `clean`. A passing field goes into `clean`.

**Check it.** `0` and `""` are values, not missing, because we only test for `None`. Cost is linear in the contract size.

**Watch out.** Stopping at the first problem, or letting `True` pass as the number 1, are the two classic slips here.
