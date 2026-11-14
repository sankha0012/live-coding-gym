def count_vowels(s: str) -> int:
    return len({c for c in s.lower() if c in "aeiou"})
