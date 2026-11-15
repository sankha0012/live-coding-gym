def Brackets(s):
    depth = 0
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth < 0:
                return "false"
    return "true" if depth == 0 else "false"

print(Brackets(input()))
