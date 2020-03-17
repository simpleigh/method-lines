import unittest
from unittest.mock import patch

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
        # Passes if no errors
        config()

    def test_good_file_simple_key(self):
        config = KeyValueConfig(find_fixture('key_value', 'good'))

        result = config()

        self.assertIn('Key1', result)
        self.assertEqual(result['Key1'], 'Value1')

    def test_good_file_complex_key(self):
        config = KeyValueConfig(find_fixture('key_value', 'good'))

        result = config()

        self.assertIn('Key 2', result)
        self.assertEqual(result['Key 2'], 'Value 2 which is longer')

    def test_blank_lines_skipped(self):
        config = KeyValueConfig(find_fixture('key_value', 'padded'))

        result = config()

        self.assertIs(len(result), 1)
        self.assertIn('Key', result)
        self.assertEqual(result['Key'], 'Value')


class MethodsTestCase(unittest.TestCase):
    def test_good_file_loaded_without_error(self):
        config = Methods(find_fixture('methods', 'good'), ConfigStoreMock())
        # Passes if no errors
        config()
