import csv

from ringing import Change

from lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        calls = {}
        with open(self.get_config_filename(), 'rb') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                call, place_notation = row
                try:
                    calls[call] = Change(self.configs.bells, place_notation)
                except ValueError as e:
                    print('Could not parse call {}'.format(name))
                    raise

        return calls
