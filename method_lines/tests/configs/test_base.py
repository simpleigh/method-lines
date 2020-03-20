import io
import os
import unittest
from unittest.mock import MagicMock

from method_lines.configs.base import BaseConfig
from method_lines.tests.configs.helpers import find_fixture


class TestConfig(BaseConfig):
    def _process_data(self, file):
        return 'test'


class BaseConfigTestCase(unittest.TestCase):
    def test_passes_the_file_to_derived_classes(self):
        filename = find_fixture('base', 'good')
        config = TestConfig(filename)
        config._process_data = MagicMock()

        config.get_data()

        self.assertIs(config._process_data.call_count, 1)

        file = config._process_data.call_args[0][0]
        self.assertIsInstance(file, io.TextIOBase)
        self.assertEqual(file.name, filename)

    def test_returns_the_processed_result_from_derived_classes(self):
        config = TestConfig(find_fixture('base', 'good'))
        self.assertEqual(config.get_data(), 'test')

    def test_only_processes_data_once(self):
        config = TestConfig(find_fixture('base', 'good'))
        config._process_data = MagicMock()

        self.assertIs(config._process_data.call_count, 0)

        config.get_data()

        self.assertIs(config._process_data.call_count, 1)

        config.get_data()

        self.assertIs(config._process_data.call_count, 1)

    def test_raises_if_file_not_found(self):
        config = BaseConfig(find_fixture('base', 'missing'))
        with self.assertRaises(FileNotFoundError):
            config.get_data()

    def test_raises_not_implemented_for_abstract_base(self):
        config = BaseConfig(find_fixture('base', 'good'))
        with self.assertRaises(NotImplementedError):
            config.get_data()
