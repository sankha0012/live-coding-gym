def assign_arm(user_id: str, canary_percent: int = 5, salt: str = "canary-v1") -> str:
    bucket = hash(f"{salt}:{user_id}") % 100
    return "canary" if bucket < canary_percent else "stable"
