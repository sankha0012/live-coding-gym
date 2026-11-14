def chunk_words(text, size, overlap):
    words = text.split()
    if not words:
        return []
    step = size - overlap            # must be > 0
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
    return chunks
