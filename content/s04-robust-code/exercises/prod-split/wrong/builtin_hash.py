import hashlib

def assign_split(user_id, test_pct=20):
    bucket = hash(str(user_id)) % 100
    return "test" if bucket < test_pct else "train"
