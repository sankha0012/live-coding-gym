def add_tag(order, tag, tags=[]):
    tags.append(tag)
    order["tags"] = tags
    return tags

def top_restaurants(counts, n=3):
    return sorted(counts, key=lambda r: (-counts[r], r))[:n]
