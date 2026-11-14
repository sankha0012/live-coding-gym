def flatten(lists: list) -> list:
    return [x for inner in lists for x in inner]
