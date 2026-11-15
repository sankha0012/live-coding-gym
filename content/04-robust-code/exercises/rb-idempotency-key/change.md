Change: allow a key to be run again. Add a method `forget(key)` to `IdempotentRunner`.

After `forget(key)`, the stored result (or stored exception) for that key is gone, so the next `run(key, payload)` calls `func(payload)` again, like a first call. Forgetting a key the runner has never seen does nothing and does not raise. Other keys are not affected.

Do this by hand in your own passing solution. It should take one or two lines.
