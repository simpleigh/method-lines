from __future__ import absolute_import

from lines.commands import BaseCommand
from lines.psline import PsLineDriver

class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = self.get_output_directory()
        driver.suppress_rules = True
        driver.total_leads = 1

        for method in self.job.configs.methods.itervalues():
            for pair in range(0, self.job.configs.bells, 2):
                driver.filename_suffix = ' - {}'.format(pair)
                lines = []
                for bell in range(self.job.configs.bells):
                    if pair <= bell <= pair + 1:
                        weight = 2
                    else:
                        weight = 1
                    lines.append({'bell': bell, 'weight': weight})
                driver.create_line(method, lines)