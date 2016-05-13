# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import csv

from ringing import Method
import six

from method_lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        methods = {}
        with open(self.get_config_filename()) as file:
            reader = csv.reader(file, delimiter=b'\t' if six.PY2 else '\t')
            for row in reader:
                base_name, place_notation = row
                try:
                    methods[base_name] = Method(
                        place_notation,
                        self.configs.bells,
                        base_name
                    )
                except ValueError:
                    print('Could not parse method {0}'.format(base_name))
                    raise

        return methods
