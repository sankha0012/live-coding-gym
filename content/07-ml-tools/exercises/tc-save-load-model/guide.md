**Why this matters.** Training happens once, serving happens later in another process. So the fitted model has to be written to disk and brought back exactly as it was.

**How we get there.**
1. Write the model with `joblib.dump(model, path)`. It works for a `str` or a `Path` and handles large numpy arrays well, which is why it is the usual tool for scikit-learn objects.
2. Overwriting needs no extra code, because `dump` replaces a file that already exists.
3. Read it back with `joblib.load(path)` and return that. It must be a new object built from the file.
4. Pass the whole fitted pipeline, not just the classifier. Then the imputer and scaler are saved with it, and serving cannot preprocess differently from training.

So the whole solution is two lines: dump, then `return joblib.load(path)`.

**Check it.** The loaded model gives the same predictions as the original. Time and file size grow with the size of the fitted arrays.

**Watch out.** Returning the same object, or a `deepcopy` of it, looks fine in memory but never proves the file works. Forgetting the `return` is the other easy miss.
