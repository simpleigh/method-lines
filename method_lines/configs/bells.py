# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ringing import Bell

from method_lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        with open(self.get_config_filename()) as file:
            bells = int(file.read().strip())

        if not (0 <= bells <= Bell.MAX_BELLS):
            raise RuntimeError('Number of bells out of range')

        return bells
