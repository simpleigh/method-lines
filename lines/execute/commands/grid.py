import os

from lines.psline import PsLineDriver
from lines.execute.base import BaseCommand

class Command(BaseCommand):

    dir_name = 'grid'

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = os.path.join(self.job.path, self.dir_name)
        driver.filename_suffix = ' - Grid'
        driver.suppress_rules = True
        driver.total_leads = 1

        for method in self.job.methods.itervalues():
            lines = []

            for bell in range(self.job.bells):
                if method.lead_head()[bell] == bell:
                    weight = 1
                else:
                    weight = 2
                lines.append({'bell': bell, 'weight': weight})

            driver.create_line(method, lines)
