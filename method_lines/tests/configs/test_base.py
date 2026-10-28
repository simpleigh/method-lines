import io
from unittest.mock import patch

import pytest

from method_lines.configs.base import BaseConfig
from method_lines.tests.configs.helpers import find_fixture


class ConfigUnderTest(BaseConfig):
    def _process_data(self, file):
        return 'test'


def test_passes_the_file_to_derived_classes():
    filename = find_fixture('base', 'good')
    with patch.object(ConfigUnderTest, '_process_data', autospec=True) as process_data:
        config = ConfigUnderTest(filename)

        config.get_data()

        assert process_data.call_count == 1

        file = process_data.call_args[0][1]
        assert isinstance(file, io.TextIOBase)
        assert file.name == filename


def test_returns_the_processed_result_from_derived_classes():
    config = ConfigUnderTest(find_fixture('base', 'good'))
    assert config.get_data() == 'test'


def test_only_processes_data_once():
    config = ConfigUnderTest(find_fixture('base', 'good'))
    with patch.object(ConfigUnderTest, '_process_data', autospec=True) as process_data:
        assert process_data.call_count == 0

        config.get_data()

        assert process_data.call_count == 1

        config.get_data()

        assert process_data.call_count == 1


def test_raises_if_file_not_found():
    config = BaseConfig(find_fixture('base', 'missing'))

    with pytest.raises(FileNotFoundError):
        config.get_data()


def test_raises_not_implemented_for_abstract_base():
    config = BaseConfig(find_fixture('base', 'good'))

    with pytest.raises(NotImplementedError):
        config.get_data()
