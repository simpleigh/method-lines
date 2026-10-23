import csv
import sys

from ringing import Change, Method

from method_lines.configs.base import BaseConfig


class KeyValueConfig(BaseConfig):
    """
    Config file containing a mapping from keys to values

    Keys are separated from values by a <Tab> character.
    Each mapping should appear on a separate line.
    """

    def _process_data(self, file):
        result = {}

        for row in csv.reader(file, delimiter='\t'):
            # Skip blank lines
            if not row:
                continue

            key, value = row
            result[key] = value

        return result


class Methods(KeyValueConfig):

    def _process_data(self, file):
        methods = super()._process_data(file)
        for base_name, place_notation in methods.items():
            try:
                methods[base_name] = Method(
                    place_notation,
                    self.config_store.bells,
                    base_name,
                )
            except ValueError:
                sys.stderr.write(f'Could not parse method {base_name}\n')
                raise

        return methods


class Calls(KeyValueConfig):

    def _process_data(self, file):
        calls = super()._process_data(file)
        for call, place_notation in calls.items():
            try:
                calls[call] = Change(
                    self.config_store.bells,
                    place_notation,
                )
            except ValueError:
                sys.stderr.write(f'Could not parse call {call}\n')
                raise

        return calls
