def count_vowels(s):
    return sum(1 for w in s.lower().split() if any(c in "aeiou" for c in w))
