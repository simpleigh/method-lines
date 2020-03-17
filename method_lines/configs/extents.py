from method_lines.configs import IntegerValueConfig


class Config(IntegerValueConfig):

    def read_data(self, file):
        extents = super().read_data(file)

        if not (0 <= extents):
            raise RuntimeError('Number of extents out of range')

        return extents
