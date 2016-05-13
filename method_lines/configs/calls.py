# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import csv

from ringing import Change
import six

from method_lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        calls = {}
        with open(self.get_config_filename()) as file:
            reader = csv.reader(file, delimiter=b'\t' if six.PY2 else '\t')
            for row in reader:
                call, place_notation = row
                try:
                    calls[call] = Change(self.configs.bells, place_notation)
                except ValueError:
                    print('Could not parse call {0}'.format(call))
                    raise

        return calls
