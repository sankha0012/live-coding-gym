from datetime import datetime


def check_staleness(trained_at: datetime, data_end: datetime, now: datetime,
                    max_model_age_days: float, max_data_age_days: float) -> dict:
    pass
