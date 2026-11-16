feature_store = {"user-7": {"avg_basket": 42.0}}
cache = {}
fetches = 0


def get_features(user_id, now=0):
    global fetches
    if user_id not in cache or now - cache[user_id]["at"] > 60:
        fetches += 1
        cache[user_id] = {"at": now, **feature_store[user_id]}
    return cache[user_id]


print(get_features("user-7")["avg_basket"])
feature_store["user-7"]["avg_basket"] = 55.5
print(get_features("user-7", now=100)["avg_basket"])
print(feature_store["user-7"]["avg_basket"])
print(f"fetches={fetches} cached={len(cache)}")
