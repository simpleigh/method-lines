# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from method_lines.commands import BaseCommand
from method_lines.drivers import PsLine


class Command(BaseCommand):

    def execute(self):

        driver = PsLine()
        driver.file_path = self.get_output_directory()
        driver.suppress_rules = True
        driver.total_leads = 1

        for method in six.itervalues(self.composition.configs.methods):
            lines = []

            for bell in range(self.composition.configs.bells):
                if method.lead_head()[bell] == bell:
                    weight = 1
                else:
                    weight = 2
                lines.append({'bell': bell, 'weight': weight})

            driver.create_line(
                method,
                lines,
                file='{0} - Grid'.format(method.name),
                title='{0} - Grid'.format(method.name),
            )
