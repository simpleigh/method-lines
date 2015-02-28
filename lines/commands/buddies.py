from __future__ import absolute_import

import six

from lines.commands import BaseCommand
from lines.psline import PsLineDriver

class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = self.get_output_directory()
        driver.suppress_rules = True
        driver.total_leads = 1

        for method in six.itervalues(self.composition.configs.methods):
            for pair in range(0, self.composition.configs.bells, 2):
                driver.filename_suffix = ' - {}'.format(pair)
                lines = []
                for bell in range(self.composition.configs.bells):
                    if pair <= bell <= pair + 1:
                        weight = 2
                    else:
                        weight = 1
                    lines.append({'bell': bell, 'weight': weight})
                driver.create_line(method, lines)
