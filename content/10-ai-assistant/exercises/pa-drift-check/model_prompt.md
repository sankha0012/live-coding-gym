Write a Python 3.12 function psi(reference, current, bins=10) that returns the Population Stability Index between two samples of one numeric feature. Use only numpy.
- Inputs: two lists of floats. Output: one float.
- Build the bin edges from the reference sample only, using quantiles, so each reference bin holds about the same share of data. Use the same edges for the current sample. Open the first and last bin to minus and plus infinity so no value falls outside.
- For each bin compute the share of reference values (p) and of current values (q). PSI is the sum of (q - p) * ln(q / p).
- Replace every share of 0 with a small epsilon (1e-6) before the log, so there is no division by zero and no log of zero.
- Ignore NaN values in both samples. If either sample is empty after that, raise ValueError with a clear message.
- If the quantile edges contain duplicates (ties or fewer distinct values than bins), drop the duplicate edges and use fewer bins instead of creating empty bins. A constant reference gives one bin and PSI 0.
- The function must be deterministic and must not modify its inputs.
Also write pytest tests for: identical samples (PSI is 0), a clearly shifted sample (PSI above 0.25), NaN values, an empty sample, and a constant feature. Then explain in four sentences how it works and what thresholds people use (0.1 and 0.25).
