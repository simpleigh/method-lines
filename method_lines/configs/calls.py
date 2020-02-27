# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import csv

from ringing import Change

from method_lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        calls = {}
        with open(self.get_config_filename()) as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                # Skip blank lines
                if not row:
                    continue

                call, place_notation = row
                try:
                    calls[call] = Change(self.configs.bells, place_notation)
                except ValueError:
                    print('Could not parse call {0}'.format(call))
                    raise

        return calls
