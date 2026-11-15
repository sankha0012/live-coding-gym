def is_palindrome(s: str) -> bool:
    letters = [c.lower() for c in s if c.isalpha()]
    return letters == letters[::-1]
