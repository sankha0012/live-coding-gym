def caesar(s: str, shift: int) -> str:
    out = []
    for c in s:
        if c.isalpha():
            out.append(chr((ord(c) - ord("a") + shift) % 26 + ord("a")))
        else:
            out.append(c)
    return "".join(out)
