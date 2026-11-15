A LEFT JOIN keeps every order, and the parent columns are NULL when there is no match. Filter on that NULL. COUNT(*) returns a row with 0 even when nothing matches.
