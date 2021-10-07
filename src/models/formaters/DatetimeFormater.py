from datetime import datetime


# TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S%Z"
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def format_datetime_to_str(dt: datetime) -> str:
    return datetime.strftime(dt, TIMESTAMP_FORMAT)


def format_str_to_datetime(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, TIMESTAMP_FORMAT)
