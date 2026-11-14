def tag_rows(rows, tags=None):
    if tags is None:
        tags = []
    for row in rows:
        value = row["value"]
        if value is None:
            tags.append("missing")
        elif value < 0:
            tags.append("negative")
        else:
            tags.append("ok")
    return tags
