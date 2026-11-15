def check_staleness(trained_at, data_end, now, max_model_age_days, max_data_age_days):
    if trained_at>now or data_end>now: raise ValueError
    ma=(now-trained_at).total_seconds()/86400; da=(now-data_end).total_seconds()/86400
    return {"model_age_days":ma,"data_age_days":da,"model_stale":ma>max_model_age_days,"data_stale":da>max_model_age_days}
