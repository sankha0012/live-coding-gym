Change: reject negative costs. `allow(cost)` must raise `ValueError` when `cost` is less than 0.

Right now a negative cost "removes" a negative number of tokens, so it adds tokens and can push the bucket above its capacity. After the change, `b.allow(-1)` raises `ValueError` and the bucket is left unchanged. A cost of `0` is still allowed and still returns `True`. All other behaviour stays the same.

Do this by hand in your own passing solution. It should take two lines.
