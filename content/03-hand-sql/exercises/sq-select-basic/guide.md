**Why this matters.** Every query starts here: pick the columns you want, from the table you want, for the rows you want. The rest of SQL is built from these pieces.

**How we get there.**
1. `FROM restaurants` says which table we read.
2. `WHERE city = 'Belo Horizonte'` keeps only the rows we want. Text goes in single quotes, and we copy the spelling exactly.
3. `SELECT name, cuisine` keeps only the two columns, in the order the problem asks for.

**Check it.** SQL runs `FROM` and `WHERE` first and `SELECT` last, even though we write `SELECT` first. If no restaurant matches, we get zero rows, not an error. The cost is a single scan of the table, linear in its size.

**Watch out.** A slightly different spelling: SQLite compares text case-sensitively, so `'belo horizonte'` returns zero rows. Also keep to single quotes for text; double quotes are for identifiers in standard SQL, and some engines reject them as values.
