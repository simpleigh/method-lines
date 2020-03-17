from ringing import Method

from method_lines.configs import KeyValueConfig


class Config(KeyValueConfig):

    def read_data(self, file):
        methods = super().read_data(file)
        for base_name, place_notation in methods.items():
            try:
                methods[base_name] = Method(
                    place_notation,
                    self.config_store.bells,
                    base_name
                )
            except ValueError:
                print('Could not parse method {0}'.format(base_name))
                raise

        return methods
