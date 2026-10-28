import io
from unittest.mock import patch

import pytest
from ringing import Change, Method

from method_lines.configs.key_value import (
    Calls,
    KeyValueConfig,
    Methods,
)
from method_lines.tests.configs.helpers import find_fixture


class ConfigStoreMock:
    bells = 6


class TestKeyValueConfig:
    def test_good_file_loaded_without_error(self):
        config = KeyValueConfig(find_fixture('key_value', 'good'))
        assert len(config.get_data()) == 2

    def test_good_file_simple_key(self):
        config = KeyValueConfig(find_fixture('key_value', 'good'))

        data = config.get_data()

        assert 'Key1' in data
        assert data['Key1'] == 'Value1'

    def test_good_file_complex_key(self):
        config = KeyValueConfig(find_fixture('key_value', 'good'))

        data = config.get_data()

        assert 'Key 2' in data
        assert data['Key 2'] == 'Value 2 which is longer'

    def test_blank_lines_skipped(self):
        config = KeyValueConfig(find_fixture('key_value', 'padded'))

        data = config.get_data()

        assert len(data) == 1
        assert 'Key' in data
        assert data['Key'] == 'Value'


class TestMethods:
    def test_good_file_loaded_without_error(self):
        config = Methods(find_fixture('methods', 'good'), ConfigStoreMock())
        assert len(config.get_data()) == 3

    def test_all_values_are_methods(self):
        config = Methods(find_fixture('methods', 'good'), ConfigStoreMock())

        for base_name, method in config.get_data().items():
            assert isinstance(method, Method)
            assert method.name == base_name
            assert method.bells == 6

    def test_method_has_expected_data(self):
        config = Methods(find_fixture('methods', 'good'), ConfigStoreMock())

        cambridge = config.get_data()['Cambridge']

        assert cambridge.full_name() == 'Cambridge Surprise Minor'
        assert cambridge.format(
            external_places=True,
            cross_dash=True,
            symmetry=True,
        ) == '&-36-14-12-36-14-56,12'

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_raises_for_invalid_method(self, _):
        config = Methods(find_fixture('methods', 'bad'), ConfigStoreMock())
        with pytest.raises(ValueError):
            config.get_data()


class TestCalls:
    def test_good_file_loaded_without_error(self):
        config = Calls(find_fixture('calls', 'good'), ConfigStoreMock())
        assert len(config.get_data()) == 2

    def test_all_values_are_changes(self):
        config = Calls(find_fixture('calls', 'good'), ConfigStoreMock())

        for _, change in config.get_data().items():
            assert isinstance(change, Change)
            assert change.bells == 6

    def test_call_has_expected_data(self):
        config = Calls(find_fixture('calls', 'good'), ConfigStoreMock())

        bob = config.get_data()['-']

        assert str(bob) == '14'

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_raises_for_invalid_call(self, _):
        config = Calls(find_fixture('calls', 'bad'), ConfigStoreMock())
        with pytest.raises(ValueError):
            config.get_data()
