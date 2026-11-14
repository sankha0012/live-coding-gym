# Deployment strategies

## The problem it solves

A new model that wins offline can still fail in production: different data, a slow dependency, a bug in the wrapper code. Replacing the old model for everyone at once means every user sees the failure at once. Deployment strategies limit the damage and give you a fast way back.

## The four ideas

**Shadow.** The new model receives a copy of live traffic and makes predictions, but nobody sees them. You log both outputs and compare. There is zero user risk. Use it first, to check latency, errors and how often the two models disagree. The cost is double compute, and you cannot measure user reactions, because users never saw the output.

**Canary.** A small share of real traffic, for example 5 percent, goes to the new model. You watch errors, latency and business metrics. If they look fine, grow to 25, 50, 100 percent. If not, send everyone back. Users in the canary can be hurt, so keep it small at first.

**Blue-green.** You run two full environments. Blue serves traffic, green holds the new version. After checks pass, you flip the router to green in one step. Rollback is flipping back. It is simple and fast, but it needs double capacity and flips everyone at once.

**Rollback.** The ability to return to the last good version quickly. It is not a strategy by itself but the safety net under all of them. Keep the previous model version stored and loadable, and make the switch a config change, not a rebuild.

A common order: shadow, then canary, then full rollout, with rollback ready at every step.

## The smallest runnable example

A canary needs a stable split. The same user must always land in the same group, or their experience flips between models. Do not use Python's built-in `hash()` on strings, because it changes between processes. Use `hashlib`.

```python
import hashlib

def bucket(user_id: str, salt: str = "model-v2") -> int:
    digest = hashlib.sha256(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100

def use_canary(user_id: str, percent: int = 5) -> bool:
    return bucket(user_id) < percent

users = [f"u{i}" for i in range(1000)]
share = sum(use_canary(u) for u in users) / len(users)
print(share)
print(use_canary("u42") == use_canary("u42"))
```

The same id gives the same answer on every run and every server. Changing the salt gives a fresh split, which matters when you run a new experiment and do not want the same users in the canary every time.

A shadow comparison is just as short:

```python
def disagreement(old_preds, new_preds, tol=0.1):
    pairs = list(zip(old_preds, new_preds))
    if not pairs:
        return 0.0
    return sum(abs(a - b) > tol for a, b in pairs) / len(pairs)

print(disagreement([0.2, 0.8, 0.5], [0.25, 0.4, 0.5]))
```

## The three traps

**1. No rollback trigger decided in advance.** Teams watch a dashboard and argue about whether it is bad enough. Decide before the deploy: "if the error rate is above 1 percent or p99 is above 500 ms for 10 minutes, we roll back." Better still, automate it.

**2. A canary too small or too short to tell anything.** Five percent of a quiet hour may be 30 requests. That cannot show a small drop in conversion. Check how much traffic you need before the decision, and cover a full daily cycle when the behaviour changes by hour.

**3. Forgetting state and compatibility.** A new model may need a new feature that the feature store does not yet serve, or it may write predictions in a new format that downstream readers cannot parse. During a rollout both versions run at the same time, so both must work with the same inputs and outputs. Roll the data change out first, the model second. Remember that rolling back the model does not undo bad data it already wrote.

## Choosing quickly

| Situation | Choice |
| --- | --- |
| New model, unknown behaviour on live data | Shadow first |
| Want real user metrics with limited risk | Canary |
| Need instant switch and have spare capacity | Blue-green |
| Anything, always | Keep a tested rollback |

## Say it like this

"I would release in stages. First shadow mode, where the new model scores live traffic but users never see it, so I can compare outputs and latency with zero risk. Then a canary on about five percent of users, with a stable hash bucket so each user stays in one group. I decide the rollback conditions before the release, such as error rate or p99 latency over a limit, and I keep the previous version ready to restore with a config change. Blue-green is my choice when I need an instant switch and can afford double capacity."
