**Why this matters.** Serving needs "the newest production version of this model". As strings, `"1.9.0"` sorts after `"1.10.0"`, so a naive max would roll back to an older model.

**How we get there.**
1. Write a small `_parse` that splits the version on dots, checks that every piece is digits, and returns the pieces as integers. Anything that does not parse, like `"v1"` or `""`, returns `None`.
2. Strip trailing zeros from the list and return a tuple. Then `"2.1"` and `"2.1.0"` become the same key. Tuples compare part by part, so `(1, 10) > (1, 9)`.
3. Loop over the records, skipping other names or stages and unparsed versions.
4. Keep the best record so far. Replace it only when the new key is strictly greater, so on a tie the first record in the list stays.
5. If nothing was kept, raise `LookupError`. Otherwise return the original record, not a copy.

**Check it.** One pass: linear time, constant extra space. An empty list and a list with only bad versions both raise.

**Watch out.** Comparing the version strings directly, or using `>=` for the update, gives the wrong model or the wrong tie-break.
