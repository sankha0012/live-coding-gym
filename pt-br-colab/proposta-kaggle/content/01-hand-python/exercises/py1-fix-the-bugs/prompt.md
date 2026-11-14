The starter code has a function `tag_rows(rows)` written by someone in a hurry. It contains three bugs. Find and fix them without rewriting the function from scratch.

What it should do:

- `rows` is a list of dicts, each with a key `"value"` that is a number or `None`.
- Return a new list with one tag per row, in the same order: `"missing"` if the value is `None`, `"negative"` if it is below zero, otherwise `"ok"`.
- Every call returns a fresh list. Calling the function twice must not mix the results.
- Do not modify `rows`.

Run the starter on a few inputs first and read what goes wrong. In the interview, say each bug out loud as you find it.
