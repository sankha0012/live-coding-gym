from collections import Counter


def word_count_top(text: str, n: int) -> list:
    return Counter(text.lower().split()).most_common(n)
