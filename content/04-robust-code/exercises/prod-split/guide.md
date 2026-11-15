**Why this matters.** A train/test split must be the same tomorrow, on another laptop, and in production, or you will score a model on users it trained on. Storing a split table works but is heavy; a hash of the user id gives the same answer anywhere.

**How we get there.**
1. Turn the id into text with `str(user_id)`, so `42` and `'42'` land in the same place.
2. Encode it to bytes and hash with `hashlib.md5(...)`. A hash scrambles similar ids evenly, so buckets come out roughly uniform.
3. Take `.hexdigest()` and read it as a base-16 number with `int(..., 16)`.
4. Use `% 100` to get a bucket from 0 to 99.
5. If `bucket < test_pct` return `'test'`, else `'train'`. With 20, about 20 percent of users are test.

**Check it.** `test_pct=0` sends everyone to train, and 100 sends everyone to test. Cost is constant per user.

**Watch out.** Python's built-in `hash()` is salted per process for strings, so it changes between runs; that quietly breaks reproducibility, which is why we use md5.
