import os

from method_lines.configs.composition import Composition
from method_lines.configs.key_value import Calls, Methods
from method_lines.configs.single_value import Bells, Extents


KNOWN_CONFIGS = {
    'bells': Bells,
    'calls': Calls,
    'composition': Composition,
    'extents': Extents,
    'methods': Methods,
}


class ConfigStore:
    """
    Contains available configs for a composition.

    Lazily loads config information as it is required.
    """

    def __init__(self, path, known_configs=KNOWN_CONFIGS):
        self.path = path
        self.known_configs = known_configs
        self._configs = {}

    def __getattr__(self, name):
        self._check_config_name(name)

        if not self.has_config(name):
            raise RuntimeError('Cannot find "{0}" configuration'.format(name))

        if name not in self._configs:
            Config = self.known_configs[name]
            self._configs[name] = Config(
                filename=self.get_config_filename(name),
                config_store=self,
            )

        return self._configs[name].get_data()

    def get_config_filename(self, name):
        """
        Returns the path of a particular config file.
        """
        return os.path.join(self.path, name + '.txt')

    def has_config(self, name):
        self._check_config_name(name)
        return os.path.isfile(self.get_config_filename(name))

    def _check_config_name(self, name):
        if name not in self.known_configs:
            raise NotImplementedError(
                '"{0}" configuration unknown'.format(name)
            )
