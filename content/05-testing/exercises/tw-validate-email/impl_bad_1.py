def validate_email(s):
    if " " in s or s.count("@") < 1:
        return False
    local, domain = s.split("@", 1)
    if not local or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    return True
