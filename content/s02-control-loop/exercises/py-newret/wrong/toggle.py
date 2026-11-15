def new_or_returning(customers):
    seen, out = set(), []
    for c in customers:
        if c in seen: out.append("returning"); seen.discard(c)
        else: out.append("new"); seen.add(c)
    return out
