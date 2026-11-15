Write assign_split(user_id, test_pct=20). Hash str(user_id) with hashlib.md5, turn the hex digest into an int, take it modulo 100. Return 'test' if that bucket is below test_pct, else 'train'. The same user must always land in the same split, on any machine.

*Reproducibility without storing a split table.*
