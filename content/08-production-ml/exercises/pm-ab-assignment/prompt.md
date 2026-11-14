Write `assign(user_id: str, experiment: str, weights: dict) -> str` that puts a user into a variant of an experiment.

- `weights` maps variant name to a non-negative number, for example `{"control": 1, "new": 1}` or `{"control": 9, "new": 1}`. Variants are considered in the order of the dict.
- The same `(user_id, experiment)` must always give the same variant, in every process and on every run. Do not use `random` and do not use the built-in `hash()` of a string. Use `hashlib`.
- The assignment must depend on the experiment name too: a user who is in `new` for experiment A must not be forced into `new` for experiment B. Over many users, the two experiments must look independent.
- Over many users, each variant gets a share close to its weight divided by the total. A variant with weight 0 is never assigned.
- Raise `ValueError` if `weights` is empty, has a negative weight, or the weights sum to 0.
