**Why this matters.** Real requests arrive with fields missing, and the model still needs a full row. The danger is treating valid values like `0` or `False` as missing and overwriting them.

**How we get there.**
1. Copy the row with `dict(row)`. We edit the copy, so the caller's data is never changed.
2. Loop over the `defaults`. Those are the features we know how to fill, and keys in `row` that are not in `defaults` stay in the copy untouched.
3. Test each one with `row.get(name) is None`. `get` returns `None` both for an absent key and for a stored `None`, so one check covers both kinds of missing.
4. When missing, write the default into the copy and record the name.
5. Return the copy and `sorted(filled)`, so the list of filled names is predictable and easy to log.

**Check it.** The cost is one pass over the defaults. A row with `0`, `0.0`, `False` or `""` for a feature keeps it and does not appear in the filled list.

**Watch out.** Writing `if not row.get(name)` silently replaces real zeros with defaults, and editing `row` itself surprises the caller who still holds it.
