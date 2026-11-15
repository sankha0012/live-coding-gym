def caesar(s, shift):
    out = []
    for c in s:
        if c.isascii() and c.isalpha():
            out.append(chr((ord(c.lower()) - 97 + shift) % 26 + 97))
        else:
            out.append(c)
    return "".join(out)
