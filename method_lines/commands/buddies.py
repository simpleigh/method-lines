# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from method_lines.commands import BaseCommand
from method_lines.drivers import PsLine
from ringing import Bell


class Command(BaseCommand):

    def execute(self):

        driver = PsLine()
        driver.file_path = self.get_output_directory()
        driver.total_leads = 1

        for method in six.itervalues(self.composition.configs.methods):

            for pair in range(0, self.composition.configs.bells, 2):
                lines = []
                for bell in range(self.composition.configs.bells):
                    if pair <= bell <= pair + 1:
                        weight = 4
                    else:
                        weight = 1
                    lines.append({'bell': bell, 'weight': weight})

                pair_str = Bell(pair).to_char() + Bell(pair + 1).to_char()
                driver.create_line(
                    method,
                    lines,
                    file='{0} {1}'.format(method.name, pair_str),
                    title='{0} {1}'.format(method.name, pair_str),
                )
