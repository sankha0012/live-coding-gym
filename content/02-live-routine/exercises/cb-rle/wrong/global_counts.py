from collections import Counter

def RunLength(s):
    c = Counter(s)
    return "".join(f"{c[ch]}{ch}" for ch in dict.fromkeys(s))

print(RunLength(input()))
