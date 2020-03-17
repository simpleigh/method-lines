from ringing import Bell

from method_lines.configs.base import BaseConfig


class SingleValueConfig(BaseConfig):
    """
    Config file containing a single value
    """

    def read_data(self, file):
        return file.read().strip()


class IntegerValueConfig(SingleValueConfig):
    """
    Config file containing a single integer value
    """

    def read_data(self, file):
        return int(super().read_data(file))


class Bells(IntegerValueConfig):

    def read_data(self, file):
        bells = super().read_data(file)

        if not (0 <= bells <= Bell.MAX_BELLS):
            raise RuntimeError('Number of bells out of range')

        return bells


class Extents(IntegerValueConfig):

    def read_data(self, file):
        extents = super().read_data(file)

        if not (0 <= extents):
            raise RuntimeError('Number of extents out of range')

        return extents
