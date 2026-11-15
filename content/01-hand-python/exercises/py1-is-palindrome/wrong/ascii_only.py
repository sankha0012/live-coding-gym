import string
def is_palindrome(s: str) -> bool:
    letters = [c.lower() for c in s if c in string.ascii_letters]
    return letters == letters[::-1]
