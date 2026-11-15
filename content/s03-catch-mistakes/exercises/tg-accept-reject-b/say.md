Proposal 1, reject: changing the expected value to 0.5 makes the test pass by agreeing with the bug. With predictions [1, 1, 0, 1] and labels [1, 0, 0, 1] there are three predicted positives and two are right, so 2/3 is correct. Fix the code, not the test.

Proposal 2, accept: precision is true positives over predicted positives. The old code divided by all predictions. The new code fixes that and avoids division by zero, in the function you asked about.

Proposal 3, reject: 0.37 is a magic number picked to satisfy one test. It removes the configuration you asked for and will be wrong for other data.

Proposal 4, accept: the threshold is now configurable, the default is the old value, and the function is unchanged.

Proposal 5, reject: renaming everything and reformatting 60+ lines is unrelated to the request. It hides the real changes in the diff and may break callers. Ask for it separately if you want it.
