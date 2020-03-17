from ringing import Bell

from method_lines.configs import IntegerValueConfig


class Config(IntegerValueConfig):

    def read_data(self, file):
        bells = super().read_data(file)

        if not (0 <= bells <= Bell.MAX_BELLS):
            raise RuntimeError('Number of bells out of range')

        return bells
