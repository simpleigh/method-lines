from ringing import Bell

from method_lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        with open(self.get_config_filename()) as file:
            extents = int(file.read().strip())

        if not (0 <= extents):
            raise RuntimeError('Number of extents out of range')

        return extents
