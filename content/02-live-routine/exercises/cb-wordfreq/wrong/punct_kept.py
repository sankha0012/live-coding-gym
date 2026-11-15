from collections import Counter

def TopWord(sen):
    counts = Counter(sen.lower().split())
    return min(counts, key=lambda w: (-counts[w], w))

print(TopWord(input()))
