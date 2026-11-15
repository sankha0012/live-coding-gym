bucket = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16) % 100
