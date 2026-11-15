def caesar(s, shift):
    out = []
    for c in s:
        if c.isascii() and not c.isspace():
            base = ord("A") if c.isupper() else ord("a")
            out.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            out.append(c)
    return "".join(out)
