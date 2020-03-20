import os
import unittest
from unittest.mock import MagicMock

from method_lines.configs import ConfigStore
from method_lines.configs.single_value import Bells


class ConfigStoreTestCase(unittest.TestCase):

    path = os.path.join(
        os.path.dirname(__file__),
        'fixtures',
        'store',
    )

    def test_creates_config_object_on_access(self):
        mock_bells = MagicMock()
        store = ConfigStore(self.path, {'bells': mock_bells})

        self.assertIs(mock_bells.call_count, 0)

        store.bells

        mock_bells.assert_called_with(
            filename=os.path.join(self.path, 'bells.txt'),
            config_store=store,
        )

    def test_only_creates_config_once(self):
        mock_bells = MagicMock()
        store = ConfigStore(self.path, {'bells': mock_bells})

        self.assertIs(mock_bells.call_count, 0)

        store.bells

        self.assertIs(mock_bells.call_count, 1)

        store.bells

        self.assertIs(mock_bells.call_count, 1)

    def test_returns_result_of_calling_config_object(self):
        attrs = {'get_data.return_value': 'test'}
        mock_bells_instance = MagicMock(spec=Bells, **attrs)
        mock_bells = MagicMock(return_value=mock_bells_instance)
        store = ConfigStore(self.path, {'bells': mock_bells})

        self.assertEqual(store.bells, 'test')

        self.assertIs(mock_bells_instance.get_data.call_count, 1)

    def test_raises_if_config_unknown_on_access(self):
        store = ConfigStore(self.path)
        with self.assertRaises(NotImplementedError):
            store.unknown

    def test_raises_if_config_not_found_on_access(self):
        store = ConfigStore(self.path)
        with self.assertRaises(RuntimeError):
            store.composition

    def test_can_assemble_filename(self):
        store = ConfigStore(self.path)
        self.assertEqual(
            store.get_config_filename('myconfig'),
            os.path.join(self.path, 'myconfig.txt'),
        )

    def test_knows_when_a_config_file_exists(self):
        store = ConfigStore(self.path)
        self.assertTrue(store.has_config('bells'))

    def test_knows_when_a_config_file_is_missing(self):
        store = ConfigStore(self.path)
        self.assertFalse(store.has_config('composition'))

    def test_raises_when_checking_for_an_unknown_config_file(self):
        store = ConfigStore(self.path)
        with self.assertRaises(NotImplementedError):
            store.has_config('unknown')

    def test_returns_config_value_end_to_end(self):
        store = ConfigStore(self.path)
        self.assertIs(store.bells, 12)
