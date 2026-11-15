Write `parse_csv_line(line: str) -> list[str]` that splits one CSV line into fields. Use the `csv` module.

- Fields in double quotes may contain commas: `'a,"b,c",d'` gives `["a", "b,c", "d"]`.
- Quotes are removed from the result.
- Empty fields are kept: `"a,,c"` gives `["a", "", "c"]`.
- An empty line returns an empty list.
- Spaces are kept as written (fields are not trimmed), and a doubled quote `""` inside a quoted field is one literal quote.
