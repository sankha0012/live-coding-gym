def first_unique(s):
    for i, ch in enumerate(s):
        if (i == 0 or s[i - 1] != ch) and (i == len(s) - 1 or s[i + 1] != ch):
            return i
    return -1
