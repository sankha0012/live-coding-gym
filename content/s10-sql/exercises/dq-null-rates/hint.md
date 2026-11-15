In SQLite a comparison like `subtotal IS NULL` is 1 or 0, so SUM of it counts the NULLs. Build one row per column and stack the rows with UNION ALL.
