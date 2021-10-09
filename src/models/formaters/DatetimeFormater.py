from datetime import datetime


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def format_datetime_to_str(dt: datetime) -> str:
    (date, micro) = datetime.strftime(dt, TIMESTAMP_FORMAT).split('.')
    return "%s.%03dZ" % (date, int(micro[:-1]) / 1000)


def format_str_to_datetime(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, TIMESTAMP_FORMAT)
