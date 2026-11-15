The scaler is fit on all rows before the train/test split, which is data leakage: the test rows influence the mean and scale used for training, so the test score looks better than it really is.
