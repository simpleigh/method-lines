from ringing import Change

from method_lines.configs import KeyValueConfig


class Config(KeyValueConfig):

    def read_data(self, file):
        calls = super().read_data(file)
        for call, place_notation in calls.items():
            try:
                calls[call] = Change(self.config_store.bells, place_notation)
            except ValueError:
                print('Could not parse call {0}'.format(call))
                raise

        return calls
