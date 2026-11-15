def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    out, cur, inq = [], "", False
    for ch in line:
        if ch == '"':
            inq = not inq
        elif ch == "," and not inq:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out
