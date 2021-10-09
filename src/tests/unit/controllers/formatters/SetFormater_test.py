import pytest
from controllers.formaters.SetFormater import remove_none_from_set


def test_remove_none_from_set_with_filled_set_and_none_element():
    initial_set = {1, 2, None, 3}
    assert not remove_none_from_set(initial_set).issubset({None})


def test_remove_none_from_set_with_only_none_element():
    initial_set = {None}
    assert remove_none_from_set(initial_set) == set()


def test_remove_none_from_set_with_filled_set_without_none_element():
    initial_set = {1, 2, 3}
    assert not remove_none_from_set(initial_set).issubset({None})


def test_remove_none_from_set_with_none_element():
    with pytest.raises(TypeError):
        remove_none_from_set(None)
