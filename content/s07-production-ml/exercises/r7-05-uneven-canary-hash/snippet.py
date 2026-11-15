def in_canary(user_id, percent=20):
    return sum(ord(c) for c in user_id) % 100 < percent


users = [f"u{i}" for i in range(1000)]
canary = [u for u in users if in_canary(u)]
print(len(canary))
print(canary[:5])
print(in_canary("u0") == in_canary("u0"))
