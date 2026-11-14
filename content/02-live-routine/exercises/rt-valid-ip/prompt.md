Write `is_valid_ip(s: str) -> bool` that returns True only for a valid IPv4 address in dotted quad form.

Rules:
- exactly 4 parts separated by single dots,
- each part is only the digits 0 to 9 (no spaces, no signs, not empty),
- each part is between 0 and 255,
- no leading zeros: `"0"` is fine, `"01"` is not.

Example: `is_valid_ip("192.168.0.1")` returns `True`, and `is_valid_ip("192.168.01.1")` returns `False`.
