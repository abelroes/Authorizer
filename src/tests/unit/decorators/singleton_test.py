from uuid import uuid4
from decorators.singleton import singleton


@singleton
class SomeClassToTestSingleton:
    some_attribute: str = str(uuid4())


class SomeClassNotSingleton:
    some_attribute:  str = str(uuid4())


def test_if_singleton_works():
    foo = SomeClassToTestSingleton()
    bar = SomeClassToTestSingleton()

    assert foo is bar
    assert foo.some_attribute is bar.some_attribute


def test_if_singleton_differs_from_not_singleton():
    foo = SomeClassToTestSingleton()
    bar = SomeClassNotSingleton()

    assert foo is not bar
    assert foo.some_attribute is not bar.some_attribute
