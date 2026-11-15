def word_count_top(text: str, n: int) -> list:
    counts = {}
    for w in text.lower().split():
        counts[w] = counts.get(w, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n or None]
