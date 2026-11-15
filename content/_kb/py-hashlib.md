---
title: Stable hashing with hashlib (and why not hash())
summary: Use hashlib to get the same hash for the same text in every run. Built-in hash() of a string changes per process.
tags: [python, hashing, determinism]
---
```python
import hashlib
hashlib.sha256(b"hello").hexdigest()
# '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
key = "user-42"
digest = hashlib.sha256(key.encode()).hexdigest()   # str -> bytes -> 64 hex chars
bucket = int(digest, 16) % 100                      # 79   same in every run, on every machine
hash(key) % 100                                     # different in each process: do not use
```

- `hashlib` needs bytes. Call `.encode()` on a string first.
- Built-in `hash()` of a `str` is randomised per process, so it is not stable between runs.
- `int(hexdigest, 16) % n` turns a hash into a stable bucket from 0 to n - 1.

<!-- more -->

## Details

Python salts the built-in `hash()` of strings and bytes with a random value chosen when the process starts. This is a security feature controlled by the `PYTHONHASHSEED` environment variable. Running the same line twice shows it:

```
$ python -c "print(hash('user-42') % 100)"
32
$ python -c "print(hash('user-42') % 100)"
66
```

So `hash()` is fine inside one process (dicts and sets use it) but wrong for anything that must agree across runs, machines or services: A/B assignment, sharding, cache keys, de-duplication ids.

A `hashlib` digest depends only on the input bytes:

```python
def bucket(key: str, buckets: int = 100) -> int:
    digest = hashlib.sha256(key.encode()).hexdigest()
    return int(digest, 16) % buckets

[bucket(k) for k in ["user-1", "user-2", "user-3"]]   # [79, 95, 9]
bucket("exp1:user-42")                                 # 30   add a prefix for an independent split
```

`hexdigest()` returns a hex string (64 characters for SHA-256). `digest()` returns raw bytes (32 bytes). For large data, feed it in pieces:

```python
h = hashlib.sha256()
h.update(b"hel")
h.update(b"lo")
h.hexdigest() == hashlib.sha256(b"hello").hexdigest()   # True
```

A tiny change in the input gives a completely different hash. `"a"` and `"A"` share nothing. Normalise the text first (strip, lower) if those should count as the same key.

To hash a dict, make the text stable first: `json.dumps(d, sort_keys=True).encode()`.

## Common mistakes

- Passing a `str`: `TypeError: Strings must be encoded before hashing`.
- Using `hash(user_id) % 100` for experiment buckets. Users change group on every restart.
- Forgetting `16` in `int(digest, 16)`, which raises `ValueError`.
- Hashing `str(some_dict)` or unsorted JSON, so equal data gives different hashes.

## See also

- [Canary, shadow and A/B assignment with stable hashing](#/kb/prod-canary-shadow-ab)
- [Determinism: seeds, ordering, time](#/kb/prod-determinism)
- [JSON: dumps, loads, sort_keys](#/kb/py-json)
- Official docs: https://docs.python.org/3/library/hashlib.html
