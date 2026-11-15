def add_tag(order, tag, tags=[]):
    tags.append(tag)
    order["tags"] = tags
    return tags

def top_restaurants(counts, n=3):
    """counts: {restaurant_id: delivered_orders}"""
    return sorted(counts, key=lambda r: counts[r])[:n]

a, b = {"id": 1}, {"id": 2}
add_tag(a, "vip")
print(add_tag(b, "new"))
