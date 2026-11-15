import math

def validate(row, schema):
    clean, issues = {}, []
    for name, (typ, lo, hi, default) in schema.items():
        v = row.get(name)
        if not v or (isinstance(v, float) and math.isnan(v)):
            clean[name] = default
            issues.append("missing:" + name)
            continue
        try:
            v = float(v) if typ == "float" else int(v)
        except (TypeError, ValueError):
            clean[name] = default
            issues.append("bad_type:" + name)
            continue
        if v < lo or v > hi:
            v = min(max(v, lo), hi)
            issues.append("clipped:" + name)
        clean[name] = v
    for name in row:
        if name not in schema:
            issues.append("extra:" + name)
    return clean, sorted(issues)
