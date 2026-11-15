A model's input feature can drift silently: no error, but the values change. Write `drift_alarm(reference, live, k=3.0)` where `reference` and `live` are lists of floats.

Compare the live window with the reference, with both measured in units of the reference standard deviation `rs` (population standard deviation, `statistics.pstdev`):

- add `"mean"` to the reasons when `abs(live_mean - ref_mean) > k * rs`
- add `"std"` to the reasons when `abs(live_std - rs) > k * rs`

Return a dict `{"alarm": bool, "reasons": list}`. `alarm` is true when `reasons` is not empty. Reasons come in the order `"mean"`, `"std"`.

Edge cases: if `reference` or `live` is empty, never raise. Return `{"alarm": False, "reasons": ["no_data"]}`. A reference with zero spread (`rs == 0`) still works: any difference in mean or std is then beyond the limit. A value exactly on the limit is not an alarm.
