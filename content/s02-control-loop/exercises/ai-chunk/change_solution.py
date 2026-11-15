def chunk_words(text, size, overlap, drop_short=False):
    words = text.split()
    if not words:
        return []
    step = size - overlap            # must be > 0
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
    if drop_short:
        chunks = [c for c in chunks if len(c.split()) == size]
    return chunks
