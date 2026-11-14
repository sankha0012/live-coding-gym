import hashlib


def assign_arm(user_id: str, canary_percent: int = 5, salt: str = "canary-v1") -> str:
    bucket = int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 100
    return "canary" if bucket < canary_percent else "stable"
