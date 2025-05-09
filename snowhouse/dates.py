from datetime import datetime, timedelta


def fetch_dates():
    today = datetime.now()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

    start_date = "2022-01-01"
    end_date = last_day_of_previous_month.strftime("%Y-%m-%d")

    return start_date, end_date
