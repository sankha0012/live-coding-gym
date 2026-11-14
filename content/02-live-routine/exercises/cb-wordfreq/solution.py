from collections import Counter

def TopWord(sen):
    clean = "".join(ch.lower() if ch.isalnum() or ch == " " else " " for ch in sen)
    counts = Counter(clean.split())
    return min(counts, key=lambda w: (-counts[w], w))

print(TopWord(input()))
