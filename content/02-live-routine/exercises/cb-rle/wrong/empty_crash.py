def RunLength(s):
    out = []
    cur, count = s[0], 0
    for ch in s:
        if ch == cur:
            count += 1
        else:
            out.append(str(count) + cur)
            cur, count = ch, 1
    out.append(str(count) + cur)
    return "".join(out)

print(RunLength(input()))
