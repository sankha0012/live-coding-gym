The first total, `naive`, counts replayed events twice. Change the code so that it also ignores repeated ids (count each id once) before summing, without touching the `dropped` line.

The output must be exactly:

```
naive: {'a': 15, 'b': 25}
deduped: {'a': 15, 'b': 25}
dropped: 2
```
