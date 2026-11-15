**Why this matters.** A validator is the trust boundary of the service. Values it wrongly accepts go straight into the model.

**How we get there.**
1. Run the tests. Four fail, among them the bool and the nan cases.
2. Reproduce: `validate_request({"age": True}, {"age": {"type": int}})`. It returns `({"age": True}, [])` and should report `bad_type:age`.
3. Reason: `isinstance(True, int)` is `True` because bool subclasses int. Reject bool before the type check.
4. Reproduce the second: `validate_request({"s": float("nan")}, {"s": {"type": float}})` passes, since every comparison with nan is false. Add an explicit `math.isnan` check that produces `out_of_range`, before the bound comparisons and whether or not bounds exist.
5. Keep range checks off `str` fields, as the starter already does.

**Check it.** All tests pass, and an int is still accepted for a float field and converted with `float()`.

**Watch out.** Checking only `value != value` for nan is fine, but `math.isnan` is clearer to explain.
