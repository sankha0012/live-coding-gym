def anagram_groups(words: list[str]) -> list[list[str]]:
    groups = {}
    for w in words:
        groups.setdefault("".join(sorted(w)), []).append(w)
    return sorted(groups.values(), key=lambda g: g[0])
