import pytest
from datetime import datetime
from models.formaters.DatetimeFormater import format_datetime_to_str, format_str_to_datetime


def test_format_datetime_to_str():
    dt = datetime(2019, 2, 13, 10, 0, 0, 000)
    dt_str = "2019-02-13T10:00:00.000Z"

    assert format_datetime_to_str(dt) == dt_str


def test_format_datetime_to_str_with_none():
    with pytest.raises(TypeError):
        format_datetime_to_str(None)


def test_format_str_to_datetime():
    dt_str = "2019-02-13T10:00:00.000Z"
    dt = datetime(2019, 2, 13, 10, 0, 0, 000)

    assert format_str_to_datetime(dt_str) == dt


def test_format_str_to_datetime_with_empty_value():
    with pytest.raises(ValueError):
        format_str_to_datetime('')


def test_format_str_to_datetime_with_none():
    with pytest.raises(TypeError):
        format_str_to_datetime(None)
