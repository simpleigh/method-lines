import csv
from importlib import import_module
import os

from method_lines.utils import find_modules, get_last_module_part


class ConfigStore:
    """
    Contains available configs for a composition.

    Lazily loads config information as it is required.
    """

    def __init__(self, path):
        self.path = path

        # Set up a dictionary with possible config names as keys
        self._configs = dict([
            [module, None]
            for module
            in find_modules(os.path.dirname(__file__))
            if os.path.isfile(os.path.join(path, module + '.txt'))
        ])

    def __getattr__(self, name):
        if name not in self._configs:
            raise RuntimeError('Cannot find "{0}" configuration'.format(name))

        if self._configs[name] is None:
            module = import_module('method_lines.configs.{0}'.format(name))
            self._configs[name] = module.Config(self)

        return self._configs[name]()

    def has_config(self, name):
        return name in self._configs


class BaseConfig:

    def __init__(self, config_store):
        self.data = None
        self.config_store = config_store

    def __call__(self):
        if self.data is None:
            with open(self.get_config_filename()) as file:
                self.data = self.read_data(file)

        return self.data

    def get_config_filename(self):
        """
        Returns the path of the config file.
        """
        config_name = get_last_module_part(self.__module__)
        return os.path.join(self.config_store.path, config_name + '.txt')

    def read_data(self, file):
        """
        Parses the config file and assembles a data value from it.

        Derived configs must override this method to return a value.
        """
        raise NotImplementedError


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


class KeyValueConfig(BaseConfig):
    """
    Config file containing a mapping from keys to values

    Keys are separated from values by a <Tab> character.
    Each mapping should appear on a separate line.
    """

    def read_data(self, file):
        result = {}

        for row in csv.reader(file, delimiter='\t'):
            # Skip blank lines
            if not row:
                continue

            key, value = row
            result[key] = value

        return result
