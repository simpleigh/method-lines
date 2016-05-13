# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from method_lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        composition = []
        with open(self.get_config_filename()) as file:
            for line in file:
                line = line.strip()

                # Check methods config SEPARATELY, BEFORE the calls config.
                # This means we don't need a calls config if our composition
                # only names methods (configs are loaded lazily as required).

                if line not in self.configs.methods:
                    if line not in self.configs.calls:
                        raise RuntimeError(
                            'Cannot find method or call "{0}"'.format(line)
                        )

                composition.append(line)

        return composition
