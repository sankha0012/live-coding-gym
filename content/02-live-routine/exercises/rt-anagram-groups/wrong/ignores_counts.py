def anagram_groups(words):
    groups = {}
    for w in words:
        groups.setdefault("".join(sorted(set(w))), []).append(w)
    return sorted(groups.values(), key=lambda g: g[0])
