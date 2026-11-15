Write top_k(query, docs, k). query is a vector (list of numbers); docs maps id → vector. Return the ids of the k most similar docs by cosine similarity, highest first, ties by id. Skip docs whose vector is all zeros.

*The core of RAG retrieval, without libraries.*
