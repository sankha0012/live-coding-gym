Write a Python 3.12 function split_rows(rows, key, test_fraction=0.2, salt="v1") using only the standard library.
- Input: a list of dicts and the name of the key that identifies the entity (for example "customer_id"). Output: a tuple (train, test) of lists.
- All rows with the same key value must go to the same side, so a customer never appears in both train and test (no leakage).
- The assignment must be deterministic and stable across runs, machines and Python processes. Do not use random without a seed and do not use the built-in hash() on strings, because it changes between processes. Use hashlib.sha256 of f"{salt}:{key_value}" and map the first 8 bytes (big-endian) to an integer and divide by 2**64 to get a number in [0, 1). A row goes to test if that number is below test_fraction.
- Keep the original row order inside each output list. Do not modify the input.
- Edge cases: an empty list returns two empty lists. test_fraction must be strictly between 0 and 1, otherwise raise ValueError. A row without the key raises ValueError.
Also write pytest tests for: no key shared between train and test, the same result on two calls, a changed salt giving a different split, an empty input, an invalid fraction, and a test share that is roughly right on 1000 keys. Then explain in a few sentences why a hash split is better than random shuffling for a nightly job.
