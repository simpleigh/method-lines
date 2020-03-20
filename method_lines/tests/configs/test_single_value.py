import unittest

from method_lines.configs.single_value import (
    Bells,
    Extents,
    IntegerValueConfig,
    SingleValueConfig,
)
from method_lines.tests.configs.helpers import find_fixture


class SingleValueConfigTestCase(unittest.TestCase):
    def test_good_file_loaded_correctly(self):
        config = SingleValueConfig(find_fixture('single_value', 'good'))
        self.assertEqual(config.get_data(), 'test')

    def test_whitespace_padding_stripped(self):
        config = SingleValueConfig(find_fixture('single_value', 'padded'))
        self.assertEqual(config.get_data(), 'test')

    def test_raises_for_missing_file(self):
        config = SingleValueConfig(find_fixture('single_value', 'missing'))
        with self.assertRaises(FileNotFoundError):
            config.get_data()


class IntegerValueConfigTestCase(unittest.TestCase):
    def test_good_file_loaded_correctly(self):
        config = IntegerValueConfig(find_fixture('integer_value', 'good'))
        self.assertIs(config.get_data(), 12)

    def test_raises_for_non_integers(self):
        config = IntegerValueConfig(find_fixture('integer_value', 'bad'))
        with self.assertRaises(ValueError):
            config.get_data()


class BellsTestCase(unittest.TestCase):
    def test_good_file_loaded_correctly(self):
        config = Bells(find_fixture('bells', 'good'))
        self.assertIs(config.get_data(), 12)

    def test_raises_for_high_value(self):
        config = Bells(find_fixture('bells', 'high'))
        with self.assertRaises(RuntimeError):
            config.get_data()

    def test_raises_for_low_value(self):
        config = Bells(find_fixture('bells', 'low'))
        with self.assertRaises(RuntimeError):
            config.get_data()


class ExtentsTestCase(unittest.TestCase):
    def test_good_file_loaded_correctly(self):
        config = Extents(find_fixture('extents', 'good'))
        self.assertIs(config.get_data(), 7)

    def test_raises_for_low_value(self):
        config = Extents(find_fixture('extents', 'low'))
        with self.assertRaises(RuntimeError):
            config.get_data()
