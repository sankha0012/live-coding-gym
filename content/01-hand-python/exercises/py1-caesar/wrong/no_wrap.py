def caesar(s: str, shift: int) -> str:
    out = []
    for c in s:
        if c.isalpha():
            out.append(chr(ord(c) + shift))
        else:
            out.append(c)
    return "".join(out)
