**Why this matters.** Real tables mix numbers and text, and each needs different preparation. In production a new category will show up one day, and the pipeline must not crash.

**How we get there.**
1. Use `ColumnTransformer`, which takes `(name, transformer, columns)` triples and joins the results side by side.
2. First triple: `("num", StandardScaler(), numeric)`. Scaling the numbers is the point of this block, so passing them through untouched would be wrong.
3. Second triple: `("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical)`. With `ignore`, a category never seen in training becomes a row of zeros instead of an error. `sparse_output=False` gives a normal array.
4. Keep that order, so scaled numbers come first and one-hot columns after.
5. Return it unfitted, so the caller fits it on training data only. Leave `remainder` at its default, which drops all other columns such as an id.

**Check it.** Empty `numeric` or `categorical` lists work, since each triple just gets zero columns. Fitting is linear in rows and columns.

**Watch out.** Fitting inside the function, or `remainder="passthrough"`, quietly bakes in data or lets stray columns reach the model.
