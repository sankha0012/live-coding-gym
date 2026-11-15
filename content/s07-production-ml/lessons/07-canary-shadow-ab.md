# Canary, shadow and A/B rollout

## What it is

Ways to release a new model without exposing every user at once. Shadow mode sends the new model a copy of live traffic and logs its answers, but nobody sees them. A canary sends a small share of real traffic, for example 5 percent, to the new model and grows it if the metrics hold. An A/B test splits users into groups for a planned comparison of a business metric. All three need a stable split, and all need a rollback. See [canary, shadow and A/B](#/kb/prod-canary-shadow-ab) and [A/B z-test](#/kb/ml-ab-test-z).

## How it breaks in production

The split itself is the first trap. Python's built-in `hash()` of a string changes between processes unless the seed is fixed, so one user lands in different groups on different servers. Random assignment per request has the same effect: the user sees model A, then B, and your metrics are mixed. Shadow mode has no user risk, but it doubles compute, and it cannot tell you how users react. A canary on 30 requests cannot show a small drop in conversion,. Teams also forget to set the rollback trigger in advance.

## The defence in code

```python
import hashlib

def bucket(user_id: str, salt: str = "model-v2") -> int:
    digest = hashlib.sha256(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100

def use_canary(user_id: str, percent: int = 5) -> bool:
    return bucket(user_id) < percent

def disagreement(old, new, tol=0.1) -> float:
    pairs = list(zip(old, new))
    return sum(abs(a - b) > tol for a, b in pairs) / len(pairs) if pairs else 0.0

users = [f"u{i}" for i in range(10000)]
print(sum(use_canary(u) for u in users) / len(users))     # close to 0.05
print(use_canary("u42") == use_canary("u42"))             # True on every run
print(disagreement([0.2, 0.8, 0.5], [0.25, 0.4, 0.5]))    # one of three differs by more than 0.1
```

The assignment depends only on the salt and the user id, so it is identical on every server and run. A new salt gives a new split. The disagreement rate is the headline number of a shadow run.

## What to say in the interview

"I release in stages: shadow first to compare outputs and latency with zero user risk, then a canary on a few percent of users with a stable hash bucket, then full traffic. I write the rollback conditions before the release, such as error rate or p99 above a limit for ten minutes, and keep the previous version ready to restore by configuration. For an A/B test I fix the sample size and metric up front, so I do not stop when the number looks good."
