Write check_batch(values, ref_mean, ref_std, max_null_rate=0.05, z=3.0). Return a sorted list of alerts. Empty batch → ['empty']. 'null_rate' if the share of None/NaN exceeds max_null_rate. 'mean_shift' if the mean of the valid values differs from ref_mean by more than z · ref_std / √n_valid. If there are no valid values, you can't check the mean.

*Catch upstream data breakage before the model's output degrades.*
