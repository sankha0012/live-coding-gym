from datetime import datetime


def check_staleness(trained_at: datetime, data_end: datetime, now: datetime,
                    max_model_age_days: float, max_data_age_days: float) -> dict:
    if trained_at > now or data_end > now:
        raise ValueError("timestamp is in the future")
    model_age = (now - trained_at).total_seconds() / 86400
    data_age = (now - data_end).total_seconds() / 86400
    return {
        "model_age_days": model_age,
        "data_age_days": data_age,
        "model_stale": model_age >= max_model_age_days,
        "data_stale": data_age >= max_data_age_days,
    }
