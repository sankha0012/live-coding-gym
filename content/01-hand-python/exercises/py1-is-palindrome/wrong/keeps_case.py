def is_palindrome(s: str) -> bool:
    letters = [c for c in s if c.isalpha()]
    return letters == letters[::-1]
