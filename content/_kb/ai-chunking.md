---
title: Chunking text with overlap
summary: Cut a long text into windows of a fixed size that share a few tokens, so no sentence is lost at a border.
tags: [ai, retrieval]
---
```python
def chunk(tokens, size, overlap):
    if size < 1 or not 0 <= overlap < size:
        raise ValueError("need size >= 1 and 0 <= overlap < size")
    step = size - overlap
    out = []
    for start in range(0, len(tokens), step):
        out.append(tokens[start:start + size])
        if start + size >= len(tokens):
            break                       # this chunk reached the end
    return out
```

- Use it before embedding documents for retrieval, or to fit a long text into a model's context.
- Key rule: the window moves by `size - overlap`, and the overlap must be smaller than the size.
- Say: "The overlap keeps a sentence that crosses a border whole in at least one chunk."

<!-- more -->

## Details

```python
["".join(c) for c in chunk(list("abcdefgh"), 4, 1)]   # ['abcd', 'defg', 'gh']
["".join(c) for c in chunk(list("abcdefg"), 4, 1)]    # ['abcd', 'defg']
chunk([], 4, 1)                                       # []
chunk(["x"], 4, 1)                                    # [['x']]
```

Each chunk starts `step` tokens after the one before, so the last `overlap` tokens of one chunk are the first tokens of the next.

The `break` matters. Without it the second example would produce a third chunk `['g']`, which is already fully inside `'defg'`. That is a duplicate fragment that costs an embedding and pollutes search results.

Choices to mention:

- **Unit.** Characters are simple. Words are better. Model tokens are what the limits are really measured in. The skeleton works on any list.
- **Size.** Small chunks give precise retrieval and little context. Large chunks give more context and a blurrier embedding. A few hundred tokens with 10 to 20 percent overlap is a common start.
- **Boundaries.** Splitting on paragraphs or sentences first, then packing them up to the size, keeps the meaning together better than fixed windows.
- **Metadata.** Keep the source id and the start offset with each chunk, so an answer can cite where it came from.

## Common mistakes

- Allowing `overlap >= size`: the step is zero or negative, and `range` raises or returns nothing.
- Stopping the range at `len(tokens) - size`, which drops the tail of the text.
- Emitting a final chunk that is only a repeat of the previous chunk's end.
- Returning nothing for a text shorter than `size`. It should be one short chunk.
- Splitting a string by characters when the limit was given in words or tokens.

## See also

- [Slicing](#/kb/py-slicing)
- [Sliding window](#/kb/algo-sliding-window)
- [Embeddings, cosine similarity and top-k retrieval](#/kb/ai-embeddings-topk)
- [Fitting chat history into a token budget](#/kb/ai-context-budget)
