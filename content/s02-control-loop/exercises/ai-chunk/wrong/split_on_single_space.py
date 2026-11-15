def chunk_words(text, size, overlap):
    words=text.split(" ")
    if not text.strip(): return []
    step=size-overlap; out=[]
    for s in range(0,len(words),step):
        out.append(" ".join(words[s:s+size]))
        if s+size>=len(words): break
    return out
