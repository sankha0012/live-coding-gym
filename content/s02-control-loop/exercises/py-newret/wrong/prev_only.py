def new_or_returning(customers):
    out = []; prev = None
    for c in customers:
        out.append("returning" if c == prev else "new"); prev = c
    return out
