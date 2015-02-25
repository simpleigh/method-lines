from __future__ import absolute_import

import os

from lines.commands import BaseCommand
from lines.psline import PsLineDriver

class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = self.get_output_directory()
        driver.filename_suffix = ' - Grid'
        driver.suppress_rules = True
        driver.total_leads = 1

        for method in self.composition.configs.methods.itervalues():
            lines = []

            for bell in range(self.composition.configs.bells):
                if method.lead_head()[bell] == bell:
                    weight = 1
                else:
                    weight = 2
                lines.append({'bell': bell, 'weight': weight})

            driver.create_line(method, lines)
