def caesar(s, shift):
    out = []
    for c in s:
        if c.isascii() and c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            v = ord(c) - base + shift
            if v >= 26: v -= 26
            if v < 0: v += 26
            out.append(chr(v + base))
        else:
            out.append(c)
    return "".join(out)
