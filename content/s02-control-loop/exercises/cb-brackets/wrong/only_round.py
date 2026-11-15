def Brackets(s):
    stack = []
    for ch in s:
        if ch == "(":
            stack.append(ch)
        elif ch == ")":
            if not stack:
                return "false"
            stack.pop()
    return "true" if not stack else "false"

print(Brackets(input()))
