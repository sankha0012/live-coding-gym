import hashlib

def assign_split(user_id, test_pct=20):
    bucket = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16) % 100
    return "test" if bucket < test_pct else "train"
