def chunk_words(text, size, overlap):
    words=text.split()
    if not words: return []
    step=size-overlap
    return [" ".join(words[s:s+size]) for s in range(0, max(1, len(words)-size+1), step)]
