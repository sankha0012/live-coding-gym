---
title: Embeddings, cosine similarity and top-k retrieval
summary: Score each document vector against the query with cosine similarity and return the k best, ties broken by id.
tags: [ai, retrieval]
---
```python
import heapq, math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0      # zero vector: define as 0

def top_k(query, docs, k):
    """docs: list of (doc_id, vector). Best first, ties by doc_id."""
    scored = [(cosine(query, vec), doc_id) for doc_id, vec in docs]
    return heapq.nsmallest(k, scored, key=lambda s: (-s[0], s[1]))
```

- Use it for semantic search and for the retrieval step of RAG.
- Key rule: cosine compares direction, not length. Define the zero-vector case and the tie-break.
- Say: "This is a full scan, O(n) per query. For millions of vectors I would use an approximate index."

<!-- more -->

## Details

An embedding is a list of floats that represents a text. Texts with a similar meaning get vectors that point in a similar direction. Cosine similarity is the dot product divided by both lengths. It is 1 for the same direction, 0 for unrelated (orthogonal) vectors and -1 for opposite ones.

```python
docs = [("a", [1.0, 0.0]), ("b", [0.6, 0.8]), ("c", [0.0, 1.0]), ("d", [2.0, 0.0])]
top_k([1.0, 0.0], docs, 2)        # [(1.0, 'a'), (1.0, 'd')]
top_k([1.0, 0.0], docs, 10)       # [(1.0, 'a'), (1.0, 'd'), (0.6, 'b'), (0.0, 'c')]
cosine([0.0, 0.0], [1.0, 2.0])    # 0.0
```

Document `d` is twice as long as `a` and has the same score, because only direction counts. The tie is broken by id, so the result is deterministic.

`heapq.nsmallest(k, ...)` with a negated score keeps only k items in memory, in O(n log k). `sorted(scored, key=...)[:k]` gives the same answer and is fine for small inputs. A `k` larger than the number of documents returns them all.

If all vectors are normalised to length 1 when stored, cosine is just the dot product. That is what vector databases do.

After retrieval, a real system often filters by a minimum score, so that an unrelated query returns nothing instead of the k least bad documents.

## Common mistakes

- Dividing by zero for an empty text or a zero vector.
- Sorting by score only, so equal scores come back in an arbitrary order.
- Using `zip` without `strict=True`: vectors of different sizes are silently cut.
- Comparing vectors from two different embedding models. Their spaces are unrelated.
- Sorting in ascending order and returning the k worst.

## See also

- [heapq: top-k and priority queues](#/kb/py-heapq)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Chunking text with overlap](#/kb/ai-chunking)
