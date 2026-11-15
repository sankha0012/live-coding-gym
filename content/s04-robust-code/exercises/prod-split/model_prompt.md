Write assign_split(user_id, test_pct=20) in Python.
Use hashlib.md5 on str(user_id) (UTF-8), convert the hex digest to an int, take % 100 as the bucket.
Return "test" if bucket < test_pct else "train".
Don't use random or Python's built-in hash(), because hash() changes between processes.
Add asserts: same id gives the same answer twice, test_pct=0 gives "train", and about 20% of 2,000 ids land in "test".
