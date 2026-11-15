**Why this matters.** Retrieval means "find the documents whose vectors point the same way as the query". Cosine similarity measures that angle, and doing it by hand shows there is no magic in it.

**How we get there.**
1. Write a small `norm`: the square root of the sum of squares. Compute the query's norm once, outside the loop.
2. For each document compute its norm too. If either norm is 0, skip it: the cosine would divide by zero, and a zero vector has no direction.
3. Cosine is the dot product, `sum(x * y for x, y in zip(query, vec))`, divided by `qn * dn`.
4. Collect `(cos, doc_id)` pairs and sort with `key=lambda t: (-t[0], t[1])`. The minus puts the highest score first, and ties go by id ascending.
5. Slice the first `k` and return only the ids.

**Check it.** If fewer than `k` documents qualify, we return them all. Cost is `n * d` to score plus `n log n` to sort.

**Watch out.** Sorting by score alone leaves ties in the dict's insertion order, not by id, and skipping the zero-vector check crashes on an empty embedding.
