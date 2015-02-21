import os

from lines.psline import PsLineDriver
from lines.execute.base import BaseCommand

class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = os.path.join(self.job.path, self.dir_name)
        driver.total_leads = 1

        for method in self.job.methods.itervalues():
            for bell in range(self.job.bells):
                driver.filename_suffix = ' - {}'.format(bell)
                driver.place_bells = bell
                lines = [{'bell': 0, 'weight': 1}, {'bell': bell}]
                driver.create_line(method, lines)
