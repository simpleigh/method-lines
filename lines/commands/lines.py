from __future__ import absolute_import

import os

from ringing import Change

from lines.commands import BaseCommand
from lines.psline import PsLineDriver

class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = self.get_output_directory()

        for method in self.job.configs.methods.itervalues():
            lines = [{'bell': 0, 'weight': 1}]

            lh_change = method[method.length - 1]
            if lh_change == Change(self.job.configs.bells, '2'):
                lines.append({'bell': 1})
            elif lh_change == Change(self.job.configs.bells, '1'):
                lines.append({'bell': self.job.configs.bells - 1})
            else:
                raise RuntimeError('Bad LH change')

            driver.create_line(method, lines)
