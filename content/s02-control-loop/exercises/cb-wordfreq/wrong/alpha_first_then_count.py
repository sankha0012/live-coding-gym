from collections import Counter

def TopWord(sen):
    clean = "".join(ch.lower() if ch.isalnum() or ch == " " else " " for ch in sen)
    counts = Counter(clean.split())
    top = max(counts.values())
    return sorted(w for w in counts if counts[w] == top)[-1]

print(TopWord(input()))
