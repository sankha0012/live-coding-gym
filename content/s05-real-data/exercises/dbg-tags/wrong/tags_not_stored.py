def add_tag(order, tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

def top_restaurants(counts, n=3):
    return sorted(counts, key=lambda r: (-counts[r], r))[:n]
