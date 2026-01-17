from datetime import datetime, timedelta


def get_reporting_periods(latest_date: datetime) -> dict:
    """
    Returns start/end dates for:
    - current week (Mon-Sun)
    - last week
    - previous 4 weeks (excluding current week)
    """
    # Monday of current week
    week_start = latest_date - timedelta(days=latest_date.weekday())
    week_end = week_start + timedelta(days=6)

    last_week_start = week_start - timedelta(days=7)
    last_week_end = week_start - timedelta(days=1)

    four_weeks_start = week_start - timedelta(days=28)
    four_weeks_end = week_start - timedelta(days=1)

    return {
        "current": (week_start, week_end),
        "last_week": (last_week_start, last_week_end),
        "four_weeks": (four_weeks_start, four_weeks_end),
        "latest_date": latest_date,
    }