Pass the whole pipeline to cross_val_score, and pass the StratifiedKFold object as cv. The scaler lives in the pipeline, so it is refit on every fold.
