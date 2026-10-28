import pytest

from method_lines.configs.composition import Composition
from method_lines.tests.configs.helpers import find_fixture


class ConfigStoreMock:
    def __init__(self):
        self.methods: list[str] = ['Cambridge']
        self.calls: list[str] = ['-']


def test_good_file_loaded_without_error():
    config = Composition(
        find_fixture('composition', 'good'),
        ConfigStoreMock(),
    )

    assert len(config.get_data()) == 2


def test_values_loaded_correctly():
    config = Composition(
        find_fixture('composition', 'good'),
        ConfigStoreMock(),
    )

    assert config.get_data() == ['Cambridge', '-']


def test_whitespace_padding_stripped():
    config = Composition(
        find_fixture('composition', 'padded'),
        ConfigStoreMock(),
    )

    data = config.get_data()

    assert len(data) == 2
    assert data == ['Cambridge', '-']


def test_raises_for_invalid_method():
    config = Composition(
        find_fixture('composition', 'method'),
        ConfigStoreMock(),
    )

    with pytest.raises(RuntimeError):
        config.get_data()


def test_raises_for_invalid_call():
    config = Composition(
        find_fixture('composition', 'method'),
        ConfigStoreMock(),
    )

    with pytest.raises(RuntimeError):
        config.get_data()


def test_only_loads_calls_if_needed():
    config_store = ConfigStoreMock()
    config_store.calls = None  # Will raise TypeError if accessed

    config = Composition(
        find_fixture('composition', 'plain'),
        config_store,
    )

    # Test passes if no error
    config.get_data()
