**Why this matters.** `line.split(",")` works until a field contains a comma inside quotes. CSV has quoting rules, and the standard library already implements them correctly.

**How we get there.**
1. Reach for the `csv` module, not for `split`. It understands that `"b,c"` in quotes is one field and it removes the quotes for us.
2. `csv.reader` expects an iterable of lines, such as a file. Our single string is not that, so wrap it in a list: `csv.reader([line])`.
3. The reader yields one row per line. Collect them with `list(...)`.
4. Return the first row. An empty line yields no rows at all, so we return `[]` in that case: `rows[0] if rows else []`.

**Check it.** `"a,,c"` keeps its empty middle field as `""`, and a lone `","` gives two empty fields. The work is linear in the length of the line.

**Watch out.** Taking `rows[0]` without checking: for the empty string the list of rows is empty and you get an `IndexError`.
