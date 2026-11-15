import hashlib

def assign_arm(user_id: str, canary_percent: int = 5, salt: str = "canary") -> str:
    digest = hashlib.sha256(f"{salt}:{user_id}".encode()).hexdigest()
    bucket = int(digest, 16) % 100
    return "canary" if bucket < canary_percent else "stable"
