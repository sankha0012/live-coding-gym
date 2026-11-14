import random


def assign_arm(user_id: str, canary_percent: int = 5, salt: str = "canary-v1") -> str:
    return "canary" if random.random() * 100 < canary_percent else "stable"
