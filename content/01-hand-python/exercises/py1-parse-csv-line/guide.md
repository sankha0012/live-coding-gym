**Why this matters.** `line.split(",")` works until a field contains a comma inside quotes. CSV has quoting rules, and the standard library already implements them correctly.

**How we get there.**
1. Reach for the `csv` module, not for `split`. It understands that `"b,c"` in quotes is one field and it removes the quotes for us.
2. `csv.reader` expects an iterable of lines, such as a file. Our single string is not that, so wrap it in a list: `csv.reader([line])`.
3. The reader yields one row per line. Collect them with `list(...)`.
4. Return the first row. For `""` the reader gives one empty row, `[[]]`, so `rows[0]` is `[]`. The guard `rows[0] if rows else []` only matters if the reader got no lines at all, which cannot happen here, so it is a harmless safety net.

**Check it.** `"a,,c"` keeps its empty middle field as `""`, and a lone `","` gives two empty fields. The work is linear in the length of the line.

**Watch out.** Splitting on commas breaks quoted fields such as `"b,c"`. Passing the bare string, `csv.reader(line)`, makes the reader treat each character as a line.
