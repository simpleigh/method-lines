import os

from ringing import Change

from lines.psline import PsLineDriver
from lines.execute.base import BaseCommand

class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = os.path.join(self.job.path, self.dir_name)

        for method in self.job.methods.itervalues():
            lines = [{'bell': 0, 'weight': 1}]

            lh_change = method[method.length - 1]
            if lh_change == Change(self.job.bells, '2'):
                lines.append({'bell': 1})
            elif lh_change == Change(self.job.bells, '1'):
                lines.append({'bell': self.job.bells - 1})
            else:
                raise RuntimeError('Bad LH change')

            driver.create_line(method, lines)
