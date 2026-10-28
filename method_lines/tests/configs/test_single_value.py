import pytest

from method_lines.configs.single_value import (
    Bells,
    Extents,
    IntegerValueConfig,
    SingleValueConfig,
)
from method_lines.tests.configs.helpers import find_fixture


class TestSingleValueConfig:
    def test_good_file_loaded_correctly(self):
        config = SingleValueConfig(find_fixture('single_value', 'good'))
        assert config.get_data() == 'test'

    def test_whitespace_padding_stripped(self):
        config = SingleValueConfig(find_fixture('single_value', 'padded'))
        assert config.get_data() == 'test'

    def test_raises_for_missing_file(self):
        config = SingleValueConfig(find_fixture('single_value', 'missing'))

        with pytest.raises(FileNotFoundError):
            config.get_data()


class TestIntegerValueConfig:
    def test_good_file_loaded_correctly(self):
        config = IntegerValueConfig(find_fixture('integer_value', 'good'))
        assert config.get_data() == 12

    def test_raises_for_non_integers(self):
        config = IntegerValueConfig(find_fixture('integer_value', 'bad'))

        with pytest.raises(ValueError):
            config.get_data()


class TestBells:
    def test_good_file_loaded_correctly(self):
        config = Bells(find_fixture('bells', 'good'))
        assert config.get_data() == 12

    def test_raises_for_high_value(self):
        config = Bells(find_fixture('bells', 'high'))

        with pytest.raises(RuntimeError):
            config.get_data()

    def test_raises_for_low_value(self):
        config = Bells(find_fixture('bells', 'low'))

        with pytest.raises(RuntimeError):
            config.get_data()


class TestExtents:
    def test_good_file_loaded_correctly(self):
        config = Extents(find_fixture('extents', 'good'))
        assert config.get_data() == 7

    def test_raises_for_low_value(self):
        config = Extents(find_fixture('extents', 'low'))

        with pytest.raises(RuntimeError):
            config.get_data()
