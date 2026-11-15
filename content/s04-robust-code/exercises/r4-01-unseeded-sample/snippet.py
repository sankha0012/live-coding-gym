import random


def pick_eval_users(user_ids, k, seed=None):
    rng = random.Random(seed)
    return rng.sample(user_ids, k)


users = [f"u{i:03d}" for i in range(500)]

a = pick_eval_users(users, 5)
b = pick_eval_users(users, 5)
c = pick_eval_users(users, 5, seed=42)
d = pick_eval_users(users, 5, seed=42)

print("unseeded runs identical:", a == b)
print("seeded runs identical:", c == d)
print("sizes:", len(a), len(c))
print("all drawn from pool:", set(a) <= set(users) and set(c) <= set(users))
