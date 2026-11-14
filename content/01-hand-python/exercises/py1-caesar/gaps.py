def caesar(s: str, shift: int) -> str:
    out = []
    for c in s:
        if c.isascii() and c.isalpha():
            base = ord("A") if c.____() else ord("a")
            out.append(chr((ord(c) - base + shift) ____ 26 + base))
        else:
            out.append(c)
    return "".join(out)
