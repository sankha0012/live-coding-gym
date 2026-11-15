**Why this matters.** A service should keep answering when the model is down, so we build a chain: model, then rule, then a constant. The trap is deciding what "no answer" means, because a real score can be `0`.

**How we get there.**
1. List the stages in order as name and function pairs, and loop over them, so we write the logic once.
2. Call the stage inside `try`. If it raises any `Exception`, `continue` to the next stage.
3. If it returned, test `value is not None`. Only `None` means "no answer". `if value` would wrongly reject `0` and `0.0`.
4. On the first real value, return it with the stage name. That ends the loop, so later stages are never called.
5. If the loop finishes, return `default, "default"`, as it is, even if it is `None`.

**Check it.** At most two calls are made, so the cost is constant. A model answering `0.0` must still beat the rule.

**Watch out.** A truthiness test turns a legitimate zero into a fallback, and forgetting the stage name hides which path produced the number.
