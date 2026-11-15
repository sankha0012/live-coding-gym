def is_palindrome(s: str) -> bool:
    letters = [c.lower() for c in s if c.isalpha()]
    return not letters or letters[0] == letters[-1]
