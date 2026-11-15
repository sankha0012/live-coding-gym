feature_store = {"user-7": {"avg_basket": 42.0}}
cache = {}
fetches = 0


def get_features(user_id):
    global fetches
    if user_id not in cache:
        fetches += 1
        cache[user_id] = dict(feature_store[user_id])
    return cache[user_id]


print(get_features("user-7")["avg_basket"])
feature_store["user-7"]["avg_basket"] = 55.5
print(get_features("user-7")["avg_basket"])
print(feature_store["user-7"]["avg_basket"])
print(f"fetches={fetches} cached={len(cache)}")
