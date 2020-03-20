import unittest

from method_lines.configs.composition import Composition
from method_lines.tests.configs.helpers import find_fixture


class ConfigStoreMock:
    methods = ['Cambridge']
    calls = ['-']


class CompositionTestCase(unittest.TestCase):
    def test_good_file_loaded_without_error(self):
        config = Composition(
            find_fixture('composition', 'good'),
            ConfigStoreMock(),
        )
        self.assertIs(len(config.get_data()), 2)

    def test_values_loaded_correctly(self):
        config = Composition(
            find_fixture('composition', 'good'),
            ConfigStoreMock(),
        )
        self.assertEqual(config.get_data(), ['Cambridge', '-'])

    def test_whitespace_padding_stripped(self):
        config = Composition(
            find_fixture('composition', 'padded'),
            ConfigStoreMock(),
        )

        data = config.get_data()

        self.assertIs(len(data), 2)
        self.assertEqual(data, ['Cambridge', '-'])

    def test_raises_for_invalid_method(self):
        config = Composition(
            find_fixture('composition', 'method'),
            ConfigStoreMock(),
        )
        with self.assertRaises(RuntimeError):
            config.get_data()

    def test_raises_for_invalid_call(self):
        config = Composition(
            find_fixture('composition', 'method'),
            ConfigStoreMock(),
        )
        with self.assertRaises(RuntimeError):
            config.get_data()

    def test_only_loads_calls_if_needed(self):
        config_store = ConfigStoreMock()
        config_store.calls = None  # Will raise TypeError if accessed

        config = Composition(
            find_fixture('composition', 'plain'),
            config_store,
        )

        # Test passes if no error
        config.get_data()
