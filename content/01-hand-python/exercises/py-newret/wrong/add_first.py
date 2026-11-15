def new_or_returning(customers):
    seen, out = set(), []
    for c in customers:
        seen.add(c); out.append("returning" if c in seen else "new")
    return out
