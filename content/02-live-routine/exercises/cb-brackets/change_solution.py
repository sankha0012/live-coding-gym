def Brackets(s):
    pairs = {")": "(", "]": "[", "}": "{", ">": "<"}
    stack = []
    for ch in s:
        if ch in "([{<":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return "false"
    return "true" if not stack else "false"

print(Brackets(input()))
