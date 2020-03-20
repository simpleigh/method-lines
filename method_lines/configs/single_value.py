from ringing import Bell

from method_lines.configs.base import BaseConfig


class SingleValueConfig(BaseConfig):
    """
    Config file containing a single value
    """

    def _process_data(self, file):
        return file.read().strip()


class IntegerValueConfig(SingleValueConfig):
    """
    Config file containing a single integer value
    """

    def _process_data(self, file):
        return int(super()._process_data(file))


class Bells(IntegerValueConfig):

    def _process_data(self, file):
        bells = super()._process_data(file)

        if not (1 <= bells <= Bell.MAX_BELLS):
            raise RuntimeError('Number of bells out of range')

        return bells


class Extents(IntegerValueConfig):

    def _process_data(self, file):
        extents = super()._process_data(file)

        if not (1 <= extents):
            raise RuntimeError('Number of extents out of range')

        return extents
