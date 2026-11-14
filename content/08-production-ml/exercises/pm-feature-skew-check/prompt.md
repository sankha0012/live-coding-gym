A model was trained on offline features but serves on online features. Write `find_skew(online: dict, offline: dict, tolerance: float = 1e-6) -> dict` that compares the two feature dicts for the same entity and returns a dict `{feature_name: reason}` for every skewed feature.

- A feature present only in `offline` has the reason `"missing_online"`. A feature present only in `online` has the reason `"missing_offline"`.
- For a feature in both, treat `None` and float `nan` as null. Both null is fine. Only one null is skew with the reason `"diff"`.
- Two numbers (`int` or `float`, not `bool`) are skewed when `abs(online - offline) > tolerance`. A difference of exactly `tolerance` is fine. Skew reason: `"diff"`.
- Any other values (strings, bools) are skewed when they are not equal. Reason: `"diff"`.
- The returned dict is sorted by feature name. No skew returns `{}`.
