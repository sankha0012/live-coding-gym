Write `save_and_load(model, path) -> object` that saves a fitted scikit-learn pipeline to `path` with `joblib` and returns a model loaded back from that file.

- `path` is a `str` or a `pathlib.Path`. Its folder already exists.
- If a file is already at `path`, it is overwritten.
- The returned model must be a new object read from the file with `joblib.load`, not the same object you were given. Use `joblib.dump` to write it. It must give identical predictions.
