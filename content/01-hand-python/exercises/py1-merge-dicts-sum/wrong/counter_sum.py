from collections import Counter
def merge_dicts_sum(dicts: list) -> dict:
    total = Counter()
    for d in dicts:
        total += Counter(d)
    return dict(total)
