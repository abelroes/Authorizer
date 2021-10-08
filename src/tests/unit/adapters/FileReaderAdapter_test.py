import io
import json
import pytest
from adapters.FileReaderAdapter import read_file


def test_read_file_gets_file_content():
    file_content = json.dumps({"key": "Some content to be in file"})
    file = io.StringIO(file_content)

    file_reader_result = read_file(file)

    assert [json.loads(file_content)] == file_reader_result


def test_read_file_gets_empty_content():
    file_content = json.dumps(None)
    file = io.StringIO(file_content)

    file_reader_result = read_file(file)

    assert [json.loads(file_content)] == file_reader_result


def test_read_file_fails_opening_inexistent_file():
    file = None
    with pytest.raises(TypeError):
        read_file(file)
