The bin edges are hard-coded, so they say nothing about the reference data, and the new sample piles into the last bin. Change the code so the edges are computed from the reference sample `expected` (its quartiles), keeping the outer edges at 0.0 and 1.0 so every score still falls in a bin.

The output must be exactly:

```
expected share: [0.3, 0.2, 0.2, 0.3]
actual share: [0.0, 0.0, 0.0, 1.0]
psi: 6.283
drift: high
```
