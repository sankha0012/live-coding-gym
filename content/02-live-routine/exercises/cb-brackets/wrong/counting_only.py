def Brackets(s):
    ok = all(s.count(a) == s.count(b) for a, b in ("()", "[]", "{}"))
    return "true" if ok else "false"

print(Brackets(input()))
