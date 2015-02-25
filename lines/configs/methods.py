import csv

from ringing import Method

from lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        methods = {}
        with open(self.get_config_filename(), 'rb') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                base_name, place_notation = row
                try:
                    methods[base_name] = Method(
                        place_notation,
                        self.configs.bells,
                        base_name
                    )
                except ValueError as e:
                    print('Could not parse method {}'.format(base_name))
                    raise

        return methods
