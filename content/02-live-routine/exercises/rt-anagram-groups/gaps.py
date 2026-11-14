def anagram_groups(words: list[str]) -> list[list[str]]:
    groups = {}
    for w in words:
        groups.setdefault("".join(____(w)), []).____(w)
    return sorted(groups.values(), key=lambda g: ____)
