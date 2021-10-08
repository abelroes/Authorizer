import json
import pytest
from controllers.formaters.JSONFormater import convert_dict_to_json, convert_json_to_dict


def test_convert_json_to_dict_converts_value():
    json_str = '{"obj1":{"subKey":1}, "key":"value"}'
    expected_dict = {"obj1": {"subKey": 1}, "key": "value"}

    assert convert_json_to_dict(json_str) == expected_dict


def test_convert_json_to_dict_converts_empty_dict():
    json_str = '{}'
    expected_dict = {}

    assert convert_json_to_dict(json_str) == expected_dict


def test_convert_json_to_dict_converts_empty_value():
    json_str = ''

    with pytest.raises(json.decoder.JSONDecodeError):
        convert_json_to_dict(json_str)


def test_convert_json_to_dict_fails_with_invalid_json_string():
    json_str = '{"obj1":{"subKey":'

    with pytest.raises(json.decoder.JSONDecodeError):
        convert_json_to_dict(json_str)


def test_convert_json_to_dict_fails_with_None_json_string():
    json_str = None

    with pytest.raises(TypeError):
        convert_json_to_dict(json_str)


def test_convert_dict_to_json_converts_value():
    dict = {"obj1": {"subKey": 1}, "key": "value"}
    expected_json_str = '{"obj1": {"subKey": 1}, "key": "value"}'

    assert convert_dict_to_json(dict) == expected_json_str


def test_convert_dict_to_json_None_to_null():
    dict = None

    assert convert_dict_to_json(dict) == "null"
