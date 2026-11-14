def tag_rows(rows, tags=[]):
    for row in rows:
        if row["value"] is None:
            tags.append("missing")
        if row["value"] < 0:
            tags.append("negative")
        else:
            tags.append("ok")
        return tags
