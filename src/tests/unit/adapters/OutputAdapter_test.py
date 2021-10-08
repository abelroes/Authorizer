import pytest
import textwrap
from adapters.OutputAdapter import format_output


def test_format_output_passing_filled_list():
    list_to_pass = [
        {'dict1': '1'},
        {'dict2': 2},
        {'dict3': {
            'subDict': [1, 2, 3]
        }}
    ]
    expected_output = textwrap.dedent("""
        {"dict1": "1"}
        {"dict2": 2}
        {"dict3": {"subDict": [1, 2, 3]}}
        """).lstrip()
    assert format_output(list_to_pass) == expected_output


def test_format_output_passing_empty_list():
    list_to_pass = []
    expected_output = ""
    assert format_output(list_to_pass) == expected_output


def test_format_output_passing_none():
    list_to_pass = None
    with pytest.raises(TypeError):
        format_output(list_to_pass)
