import hashlib

def assign_arm(user_id: str, canary_percent: int = 5, salt: str = "canary-v1") -> str:
    digest = hashlib.sha256(f"{salt}:{user_id}".encode()).digest()
    bucket = digest[0] % 100
    return "canary" if bucket < canary_percent else "stable"
