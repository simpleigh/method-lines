import io
import unittest
from unittest.mock import patch

from ringing import Change, Method

from method_lines.configs.key_value import (
    Calls,
    KeyValueConfig,
    Methods,
)
from method_lines.tests.configs.helpers import find_fixture


class ConfigStoreMock:
    bells = 6


class KeyValueConfigTestCase(unittest.TestCase):
    def test_good_file_loaded_without_error(self):
        config = KeyValueConfig(find_fixture('key_value', 'good'))
        self.assertIs(len(config.get_data()), 2)

    def test_good_file_simple_key(self):
        config = KeyValueConfig(find_fixture('key_value', 'good'))

        data = config.get_data()

        self.assertIn('Key1', data)
        self.assertEqual(data['Key1'], 'Value1')

    def test_good_file_complex_key(self):
        config = KeyValueConfig(find_fixture('key_value', 'good'))

        data = config.get_data()

        self.assertIn('Key 2', data)
        self.assertEqual(data['Key 2'], 'Value 2 which is longer')

    def test_blank_lines_skipped(self):
        config = KeyValueConfig(find_fixture('key_value', 'padded'))

        data = config.get_data()

        self.assertIs(len(data), 1)
        self.assertIn('Key', data)
        self.assertEqual(data['Key'], 'Value')


class MethodsTestCase(unittest.TestCase):
    def test_good_file_loaded_without_error(self):
        config = Methods(find_fixture('methods', 'good'), ConfigStoreMock())
        self.assertIs(len(config.get_data()), 3)

    def test_all_values_are_methods(self):
        config = Methods(find_fixture('methods', 'good'), ConfigStoreMock())

        for base_name, method in config.get_data().items():
            with self.subTest(base_name=base_name):
                self.assertIsInstance(method, Method)
                self.assertEqual(method.name, base_name)
                self.assertEqual(method.bells, 6)

    def test_method_has_expected_data(self):
        config = Methods(find_fixture('methods', 'good'), ConfigStoreMock())

        cambridge = config.get_data()['Cambridge']

        self.assertEqual(cambridge.full_name(), 'Cambridge Surprise Minor')
        self.assertEqual(
            cambridge.format(
                 external_places=True,
                 cross_dash=True,
                 symmetry=True,
            ),
            '&-36-14-12-36-14-56,12',
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_raises_for_invalid_method(self, _):
        config = Methods(find_fixture('methods', 'bad'), ConfigStoreMock())
        with self.assertRaises(ValueError):
            config.get_data()


class CallsTestCase(unittest.TestCase):
    def test_good_file_loaded_without_error(self):
        config = Calls(find_fixture('calls', 'good'), ConfigStoreMock())
        self.assertIs(len(config.get_data()), 2)

    def test_all_values_are_changes(self):
        config = Calls(find_fixture('calls', 'good'), ConfigStoreMock())

        for call, change in config.get_data().items():
            with self.subTest(call=call):
                self.assertIsInstance(change, Change)
                self.assertEqual(change.bells, 6)

    def test_call_has_expected_data(self):
        config = Calls(find_fixture('calls', 'good'), ConfigStoreMock())

        bob = config.get_data()['-']

        self.assertEqual(str(bob), '14')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_raises_for_invalid_call(self, _):
        config = Calls(find_fixture('calls', 'bad'), ConfigStoreMock())
        with self.assertRaises(ValueError):
            config.get_data()
