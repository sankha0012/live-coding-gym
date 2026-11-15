from collections import Counter

def TopWord(sen):
    clean = "".join(ch if ch.isalnum() or ch == " " else " " for ch in sen)
    counts = Counter(clean.split())
    return min(counts, key=lambda w: (-counts[w], w)).lower()

print(TopWord(input()))
