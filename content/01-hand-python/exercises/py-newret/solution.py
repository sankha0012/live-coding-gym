def new_or_returning(customers):
    seen, out = set(), []
    for c in customers:
        out.append("returning" if c in seen else "new")
        seen.add(c)
    return out
