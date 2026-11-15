def slugify(s):
    return "-" if not s else "-".join(s.lower().split())
