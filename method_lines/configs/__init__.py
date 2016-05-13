# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from importlib import import_module
import os

from method_lines.utils import find_modules, get_last_module_part


class ConfigStore(object):
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

        return self._configs[name].data

    def has_config(self, name):
        return name in self._configs


class BaseConfig(object):

    def __init__(self, configs):
        self.configs = configs
        self.data = self.load_data()

    def get_config_filename(self):
        """
        Returns the path of the config file.
        """
        config_name = get_last_module_part(self.__module__)
        return os.path.join(self.configs.path, config_name + '.txt')

    def load_data(self):
        """
        Parses the config file and assembles a data value from it.

        Derived configs must override this method to return a value.
        """
        raise NotImplementedError
